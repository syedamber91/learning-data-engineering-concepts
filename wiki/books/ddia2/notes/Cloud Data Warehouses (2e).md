---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
topic: Data Storage for Analytics
type: subtopic
tags: [ddia2, bigquery, snowflake, iceberg, delta-lake, trino, data-catalog]
sources:
  - raw/ch04.md
---
# Cloud Data Warehouses
> The monolithic warehouse has come apart into four replaceable pieces: query engine, storage format, table format, and data catalog.

## The Idea
Established vendors — **Teradata, Vertica, SAP HANA** — offer on-premises deployments under commercial licence as well as cloud solutions. But as customers moved to the cloud, **cloud-only warehouses** such as **Google BigQuery, Amazon Redshift, and Snowflake** became widely adopted. Unlike traditional warehouses, they can exploit scalable cloud infrastructure: object storage and serverless computation platforms.

## How It Works
Cloud warehouses **integrate better with other cloud services** — many support automatic log ingestion and integrate easily with data processing frameworks such as Google Cloud Dataflow or AWS Kinesis. They are also **more elastic, because they decouple query computation from the storage layer**: data is persisted in object storage rather than on local disks, so storage capacity and query compute can be adjusted independently.

Open source warehouses — **Apache Hive, Trino, Apache Spark** — evolved with the cloud too. As analytics storage moved to **data lakes on object storage**, open source warehouses began to **break apart**. Four components previously integrated in a single system such as Hive are now often separate:

- **Query engine.** Engines such as **Trino, Apache DataFusion, and Presto** parse SQL, optimise it into execution plans, and execute against the data. Execution usually needs parallel, distributed processing tasks; some engines provide built-in task execution, others use third-party frameworks such as **Spark or Flink**.
- **Storage format.** Determines how a table's rows are encoded as bytes in a file, typically stored in object storage or a distributed filesystem, and readable not just by the query engine but by other applications using the data lake. Examples: **Parquet, ORC, Lance, Nimble**.
- **Table format.** Files in Parquet and similar formats are typically **immutable once written**, so supporting row inserts and deletions needs a table format such as **Apache Iceberg** or Databricks's **Delta** format. Table formats specify a file format defining which files constitute a table along with its schema, and offer advanced features: **time travel** (querying a table as it was at a previous point in time), garbage collection, and even transactions.
- **Data catalog.** Just as a table format defines which files make up a table, a catalog defines **which tables are in a database** — used to create, rename, and drop tables. Unlike storage and table formats, catalogs such as Snowflake's **Polaris** and Databricks's **Unity Catalog** usually run as a **standalone service queried over REST**; Apache Iceberg also offers a catalog, runnable inside a client or as a separate process. Query engines use catalog information when reading and writing tables.

## Trade-offs & Pitfalls
- **Decoupling the catalog is the quietly important one.** Traditionally catalogs and query engines were integrated; separating them lets **data discovery and data governance systems access a catalog's metadata** — which is exactly what the compliance pressures described in Chapter 1 require.
- The unbundling means each layer can be chosen independently, but it also means four things to operate and version rather than one product.

## Examples & Systems
BigQuery, Redshift, Snowflake (cloud-only warehouses); Trino, DataFusion, Presto (query engines); Parquet, ORC, Lance, Nimble (storage formats); Iceberg, Delta (table formats); Polaris, Unity Catalog (data catalogs); Dataflow and Kinesis for ingestion.

## Since the 1st Edition
Entirely new. In 2017 the 1st edition treated the data warehouse as a single product to be chosen; almost nothing in this subtopic — object-storage-backed warehouses, the four-way unbundling, table formats with time travel and transactions, or standalone REST catalogs — existed in the book. Together with [[Cloud Native System Architecture (2e)]], this is where the 2nd edition absorbs the lakehouse era.

## Related
- up: [[Data Storage for Analytics (2e)]] · chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Cloud Native System Architecture (2e)]] — storage/compute separation, stated generally
- [[Column-Oriented Storage (2e)]] — what those storage formats actually do
- [[Object Stores (2e)]] — the substrate underneath all of this
- [[Data Warehousing (2e)]] — the data lake this evolved from
