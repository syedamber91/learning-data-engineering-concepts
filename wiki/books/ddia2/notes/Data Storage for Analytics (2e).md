---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
type: topic
tags: [ddia2, analytics, data-warehouse, htap, olap]
sources:
  - raw/ch04.md
---
# Data Storage for Analytics
A data warehouse's data model is most commonly **relational**, because SQL is generally a good fit for analytical queries, and there are many graphical analysis tools that generate SQL, visualize results, and let analysts explore through operations such as drill-down and slicing and dicing.

**On the surface a data warehouse and a relational OLTP database look similar**, since both present a SQL query interface. But their internals can look quite different, because they are optimised for very different query patterns — and many database vendors now focus on supporting either transaction processing or analytics, not both.

## Subtopics
- [[Cloud Data Warehouses (2e)]] — cloud-native warehouses, and the unbundling of the open source stack into four separate components.
- [[Column-Oriented Storage (2e)]] — the central physical idea: store values from each column together.
- [[Query Execution - Compilation and Vectorization (2e)]] — two ways to make operators fast enough for millions of rows.
- [[Materialized Views and Data Cubes (2e)]] — precomputing results, and what you give up by doing so.

## Key Takeaways
- The chapter's analytics half is fundamentally about **reading less and computing faster**: columnar layout plus compression minimises bytes read from disk, and compilation or vectorization minimises CPU time spent on the bytes you do read.
- **HTAP is converging on two engines behind one interface.** Some databases — Microsoft SQL Server, SAP HANA, SingleStore — support transaction processing and data warehousing in the same product. But these hybrid transactional/analytical processing systems are **increasingly becoming two separate storage and query engines that happen to be accessible through a common SQL interface**. This restates, from the engine side, the point Chapter 1 made from the architecture side.
- Because analytics reads are aggregations over many rows and writes are bulk imports, the design constraints invert relative to OLTP: **large sequential scans matter, individual-row latency does not**.

## Since the 1st Edition
The 1st edition's equivalent material lived under [[Transaction Processing or Analytics]] and [[Data Warehousing]] in its storage chapter, mixing the *motivation* for separating analytics from the *engine techniques*. The 2nd edition moved the motivation to Chapter 1, leaving this topic purely technical — and then added two entirely new subtopics, [[Cloud Data Warehouses (2e)]] and [[Query Execution - Compilation and Vectorization (2e)]], reflecting a decade in which warehouse architecture was rebuilt on object storage and query engines were rewritten around modern CPUs.

## Related
- chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Storage and Indexing for OLTP (2e)]] — the other half of the chapter
- [[Data Warehousing (2e)]] — the architectural framing, in Chapter 1
- [[Stars and Snowflakes - Schemas for Analytics (2e)]] — the schema these engines store
