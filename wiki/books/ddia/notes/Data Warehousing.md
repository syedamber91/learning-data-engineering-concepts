---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
topic: Transaction Processing or Analytics?
type: subtopic
tags: [ddia, data-warehouse, etl, olap, oltp]
sources:
  - raw/ch03.md
---
# Data Warehousing
> A separate, read-only analytical copy of all the company's OLTP data, loaded via ETL and free to be optimized for scans instead of point lookups.

## The Idea
A large enterprise runs dozens of transaction-processing systems — storefront, point-of-sale, inventory, logistics, payroll — each mission-critical, latency-sensitive, and jealously guarded by its DBAs. Ad hoc analyst queries that scan huge swaths of data would wreck the performance of live transactions, so analysts get their own database: the **data warehouse**, a read-only copy of data from every OLTP system, queryable without endangering operations.

## How It Works
- **Extract–Transform–Load (ETL):** data is pulled from OLTP sources (periodic dumps or continuous update streams), reshaped into an analysis-friendly schema, cleaned, and loaded into the warehouse.
- The warehouse's data model is almost always relational — SQL suits aggregate-heavy analytic queries, and a rich ecosystem of BI/drill-down/slice-and-dice tooling generates SQL.
- **Same interface, different internals:** OLTP databases and warehouses both speak SQL, but their storage engines diverge sharply because access patterns diverge. Indexing structures that excel at OLTP (see [[Data Structures That Power Your Database]]) answer analytics poorly; the warehouse side motivated [[Column-Oriented Storage]].
- The OLTP/OLAP contrast in brief: OLTP reads a handful of records by key with low-latency random writes, serves end users, holds the current state, at GB–TB scale. OLAP aggregates over millions of records, ingests via bulk ETL-style loads or event streams, serves analysts, records event history, at TB–PB scale. ("Transaction" here means low-latency reads/writes, not necessarily [[ACID]] guarantees; the boundary between OLTP and OLAP is fuzzy in practice.)

## Trade-offs & Pitfalls
- Warehouses are a big-company phenomenon: small companies lack the system sprawl and data volume, so a plain SQL database (or a spreadsheet) suffices.
- Products claiming to serve both workloads (Microsoft SQL Server, SAP HANA) increasingly ship two separate storage/query engines behind one SQL facade — the workloads are too different to share internals.
- ETL introduces its own freshness lag and pipeline maintenance burden (a theme resumed in [[Keeping Systems in Sync]]).

## Examples & Systems
Commercial warehouse vendors: Teradata, Vertica, SAP HANA, ParAccel (Amazon RedShift is hosted ParAccel). Open source SQL-on-[[Hadoop]] challengers: Apache Hive, Spark SQL, Cloudera Impala, Facebook Presto, Apache Tajo, Apache Drill — several drawing on Google's Dremel design.

## Related
- up: [[Transaction Processing or Analytics]] · chapter: [[Ch 03 - Storage and Retrieval]]
- [[Stars and Snowflakes - Schemas for Analytics]] — the schema style inside the warehouse
- [[Column-Oriented Storage]] — the storage layout that makes warehouse queries fast
- [[MapReduce and Distributed Filesystems]] — the batch ecosystem behind SQL-on-Hadoop
- [[Keeping Systems in Sync]] — streaming alternatives to periodic ETL
- [[google-infrastructure]] — vutr's notes on BigQuery's own Dremel lineage, extended with the Storage API and BigLake/BigLake Managed Tables into a lakehouse-facing warehouse that reads external Parquet/Iceberg data as directly as its native tables.
- [[airbnb-data-infrastructure]] — vutr's notes trace this pattern into a real production platform: Airbnb's Minerva takes fact and dimension tables, denormalizes them into an analysis-friendly schema, and serves the result through a governed API
- [[data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa]] — vutr's notes trace the warehouse forward past this chapter's OLTP/OLAP split: schema-on-write structured data drove the two-tier lake-plus-warehouse pattern, which the lakehouse then tries to collapse back into one system with a transactional metadata layer over object storage.
- [[bigquery-internals]] — vutr's deep-dive into Dremel's own internals, the design this note's "several drawing on Google's Dremel design" line points at: the static-to-dynamic query plan, the disaggregated shuffle layer, and the Vortex storage engine that lets the same warehouse also ingest streaming data.
- [[dbt]] — vutr's notes trace this note's ETL pattern forward into the ELT reversal: cheap cloud storage and elastic in-warehouse SQL compute moved transformation from before load to after, and dbt is the tool vutr describes managing that in-warehouse SQL transformation logic (version control, testing, modularity) once the shift made it viable.
