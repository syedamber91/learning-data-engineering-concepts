---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
type: topic
tags: [ddia, oltp, olap, data-warehouse, business-intelligence]
sources:
  - raw/ch03.md
---
# Transaction Processing or Analytics?
"Transaction" is a fossil word from early business data processing, when each database write really was a sale, an order, or a salary payment; today it just means a logical unit of low-latency reads and writes — and, importantly, it implies nothing about [[ACID]] guarantees (transaction processing is contrasted with periodic batch jobs, not with weak consistency). Two access patterns grew out of this history. *Online transaction processing* (OLTP): an interactive application fetches a handful of records by key via an index, inserting or updating them from user input. *Online analytic processing* (OLAP): a business analyst scans millions of records but touches only a few columns of each, computing aggregates (counts, sums, averages) for business-intelligence reports — "total revenue per store in January," "which brand of baby food sells alongside brand X diapers." The two patterns diverge on every axis: OLTP reads few records by key while OLAP aggregates over many; OLTP takes random low-latency writes from users while OLAP ingests bulk ETL loads or event streams; OLTP serves end customers while OLAP serves internal analysts; OLTP stores the *latest state* while OLAP stores a *history of events*; OLTP datasets run gigabytes to terabytes while OLAP runs terabytes to petabytes. SQL happens to express both query styles, so one database initially served both — but from the late 1980s companies moved analytics onto a separate system, the data warehouse, whose internals this topic and [[Column-Oriented Storage]] explore.

## Subtopics
- [[Data Warehousing]] — a read-only copy of all the company's OLTP data, loaded via Extract–Transform–Load, so analysts can run expensive scans without endangering the transaction systems.
- [[Stars and Snowflakes - Schemas for Analytics]] — the star schema: a huge fact table of events ringed by dimension tables answering who/what/where/when/how/why; snowflaking normalizes the dimensions further.

## Key Takeaways
- The OLTP/OLAP split is about *access patterns*, not technology labels — small keyed lookups with random writes versus huge scans with bulk loads.
- OLTP systems are business-critical and latency-sensitive, so DBAs guard them from ad-hoc analyst queries; the warehouse exists to absorb those scans safely.
- The indexing structures of the chapter's first half suit OLTP well but answer analytic queries poorly — separate workloads justify separate storage engines.
- Warehouses are nearly universal in large enterprises and nearly absent in small ones, where the data still fits a single SQL database or a spreadsheet.
- Vendors increasingly specialize: even products offering both (Microsoft SQL Server, SAP HANA) run two engines behind one SQL facade; commercial warehouses (Teradata, Vertica, ParAccel/Amazon RedShift) now face open source SQL-on-[[Hadoop]] challengers (Hive, Spark SQL, Impala, Presto, Tajo, Drill), several shaped by Google's Dremel.

## Related
- chapter: [[Ch 03 - Storage and Retrieval]] · part: [[Part I - Foundations of Data Systems]]
- [[Data Structures That Power Your Database]] — the OLTP-side engines this topic contrasts against
- [[Column-Oriented Storage]] — how warehouses physically lay out those petabyte fact tables
- [[Batch and Stream Processing]] — the derived-data systems that later chapters build on this OLTP/analytics split
