---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
topic: Data Storage for Analytics
type: subtopic
tags: [ddia2, columnar, parquet, bitmap-encoding, run-length-encoding, sort-order]
sources:
  - raw/ch04.md
---
# Column-Oriented Storage
> Fact tables are over a hundred columns wide and a typical query touches four or five. Store columns together, and you read only what you need.

## The Idea
Warehouses conventionally use a big **fact table** with foreign keys into dimension tables. With trillions of rows and petabytes of data in fact tables, storing and querying them efficiently is challenging; dimension tables are much smaller (millions of rows) and more manageable, so the focus is on facts.

Although fact tables are often over a hundred columns wide, **a typical warehouse query accesses only four or five at a time** — `SELECT *` is rarely needed for analytics. The book's example query analyses whether people buy fresh fruit or candy depending on the day of the week; it touches a large number of rows (every fruit or candy purchase in 2024) but only three columns of `fact_sales`: `date_key`, `product_sk`, and `quantity`.

In most OLTP databases storage is **row-oriented**: all values from one row sit next to each other, and document databases are similar, storing a whole document as a contiguous byte sequence. With indexes on `date_key` or `product_sk`, a row-oriented engine still has to load all matching rows — each with over 100 attributes — from disk into memory, parse them, and filter. That takes a long time.

**The columnar idea is simple: instead of storing all values from one row together, store all values from each column together.** A query then reads and parses only the columns it uses.

## How It Works
- The layout **relies on each column storing rows in the same order**. To reassemble a row, take the 23rd entry from each column and put them together.
- In practice engines don't store an entire column (perhaps trillions of rows) in one go. They **break the table into blocks of thousands or millions of rows**, and within each block store each column's values separately. Since many queries are restricted to a date range, it's common to make each block contain rows for a particular timestamp range, so a query loads only the needed columns from the blocks overlapping that range.
- Columnar storage is used in **almost all analytical databases** today, from cloud warehouses like **Snowflake** to single-node embedded engines like **DuckDB** and product-analytics systems like **Pinot** and **Druid**. It appears in storage formats — **Parquet, ORC, Lance, Nimble** — and in-memory analytics formats such as **Apache Arrow** and Pandas/NumPy. Some time-series databases, **InfluxDB IOx** and **TimescaleDB**, are also column-oriented.
- **It isn't only for relational data.** Parquet is a columnar format supporting a document data model, based on Google's **Dremel**, using a technique called **shredding** or **striping**.

**Column compression.** Beyond loading only needed columns, compressing further reduces disk throughput and network bandwidth demands — and columnar layout lends itself well to compression, because a single column's values repeat a lot. A technique particularly effective in warehouses is **bitmap encoding**: the number of distinct values in a column is often small compared to the number of rows (a retailer may have billions of transactions but only 100,000 distinct products), so a column with n distinct values becomes n bitmaps, one per value, with one bit per row set to 1 if that row has that value. Those bitmaps are typically **sparse** (mostly 0s), so they can additionally be **run-length encoded** — counting consecutive 0s or 1s and storing the counts. **Roaring bitmaps** switch between the two representations, using whichever is more compact, making column encoding remarkably efficient.

Bitmap indexes suit warehouse queries directly. `WHERE product_sk IN (31, 68, 69)` loads three bitmaps and computes their **bitwise OR**, very efficiently. `WHERE product_sk = 30 AND store_sk = 3` loads two bitmaps and computes the **bitwise AND** — which works precisely because columns store rows in the same order, so the kth bit of one column's bitmap is the same row as the kth bit of another's. Bitmaps can even answer graph queries, such as finding all users followed by user X who also follow user Y.

**Sort order in column storage.** Row order doesn't inherently matter; the easiest is insertion order, since inserting then just appends to each column. But you can **impose an order and use it as an indexing mechanism**, as with SSTables. Sorting each column independently would be nonsense — you'd lose which items belong to the same row — so **data must be sorted an entire row at a time, even though it is stored by column**. The administrator chooses the sort columns from knowledge of common queries: if queries often target date ranges such as the last month, make `date_key` the first sort key so a query scans only last month's rows. A second column orders rows tied on the first — with `date_key` first, `product_sk` second groups all sales of the same product on the same day together, helping queries that group or filter by product within a date range.

Sorted order also **helps compression**. If the primary sort column has few distinct values, after sorting it has long runs of repeated values, and simple run-length encoding could compress it to a few kilobytes **even if the table has billions of rows**. The effect is strongest on the first sort key; second and third sort keys are more jumbled with shorter runs, and columns further down the priority appear essentially random and probably won't compress well. Having the first few columns sorted is still a win overall.

## Trade-offs & Pitfalls
- **Don't confuse column-oriented with wide-column.** The wide-column (column-family) data model lets a row have thousands of columns with no requirement that all rows share columns — but **wide-column databases are row-oriented**, storing all values of a row together. Bigtable, Accumulo, and HBase use that model.
- **Writing to column-oriented storage** is the awkward case. Warehouse writes tend to be bulk imports via ETL. Writing an individual row into the middle of a sorted table would be very inefficient, since you'd rewrite all compressed columns from the insertion point onward — but a **bulk write of many rows amortises that cost**. A **log-structured approach** is often used: all writes first go to a row-oriented, sorted, in-memory store, and when enough accumulate they are merged with the column-encoded files on disk and written to new files in bulk. Old files stay immutable and new files are written in one go, so **object storage suits these files well**. Queries examine both the on-disk column data and the recent in-memory writes and combine them; the query engine hides this from the user, so from an analyst's point of view inserts, updates, and deletes are immediately reflected. Snowflake, Vertica, Pinot, Druid, and many others work this way.

## Examples & Systems
Snowflake, DuckDB, Pinot, Druid, InfluxDB IOx, TimescaleDB; Parquet, ORC, Lance, Nimble, Arrow; roaring bitmaps; Dremel-style shredding for nested data.

## Since the 1st Edition
Consolidates four 1st-edition subtopics — [[Column-Oriented Storage]], [[Column Compression]], [[Sort Order in Column Storage]], and [[Writing to Column-Oriented Storage]] — into one. The core mechanisms (columnar layout, bitmap and run-length encoding, sorted order aiding compression, LSM-style bulk writes) are unchanged. **New:** roaring bitmaps; blocks of rows as the actual storage unit, aligned to timestamp ranges; the much wider system roster (DuckDB, Pinot, Druid, Lance, Nimble, Arrow, InfluxDB IOx, TimescaleDB); Parquet's Dremel-based support for nested documents; and object storage as the destination for merged column files. The 1st edition's separate treatment of Vertica's multiple sort orders on replicas is dropped.

## Related
- up: [[Data Storage for Analytics (2e)]] · chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Query Execution - Compilation and Vectorization (2e)]] — how these bitmaps get processed fast
- [[Stars and Snowflakes - Schemas for Analytics (2e)]] — the fact tables being stored
- [[Full-Text Search (2e)]] — postings lists as sparse bitmaps, the same trick
- 1st edition: [[Column-Oriented Storage]], [[Column Compression]], [[Sort Order in Column Storage]], [[Writing to Column-Oriented Storage]] — the four notes this merges
