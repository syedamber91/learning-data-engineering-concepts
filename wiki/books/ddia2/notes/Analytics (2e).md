---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Use Cases
type: subtopic
tags: [ddia2, lakehouse, iceberg, olap, ad-hoc-queries, tableau]
sources:
  - raw/ch11.md
---
# Analytics
> Analysts write SQL, a query engine reads from object storage, a table format tracks which files are the table, and a catalog tracks which tables exist. That stack has a name: the data lakehouse.

## The Idea
**Analytical queries often scan a large number of records, performing groupings and aggregations.** **It is possible to run such workloads in a batch processing system, alongside other batch workloads.** **Analysts write SQL queries executing atop a query engine, which reads from and writes to a distributed filesystem or object store.** **Table metadata — table-to-file mappings, names, types — is managed with table formats such as Apache Iceberg and catalogs such as Unity.** **This architecture is known as a data lakehouse.**

**As with ETL, improvements in SQL query interfaces mean many organizations now use batch frameworks such as Spark for analytics.**

## How It Works
Two query patterns:

**Pre-aggregation queries.** **Data is rolled up into OLAP cubes or data marts to speed up queries.** **Pre-aggregated data is queried in the warehouse or pushed to purpose-built real-time OLAP systems such as Apache Druid or Apache Pinot.** **Pre-aggregation normally takes place at a scheduled interval**, managed by workflow schedulers.

**Ad hoc queries.** **Users run these to answer specific business questions, investigate user behavior, debug operational issues, and much more.** **Response times are important here** — **analysts run queries iteratively as they get responses and learn more about the data they're investigating**, so **batch frameworks with fast query execution reduce waiting times.**

## Trade-offs & Pitfalls
- **SQL support enables batch frameworks to integrate with spreadsheets and visualization tools** — **Tableau, Power BI, Looker, Apache Superset.** **Tableau offers SparkSQL and Presto connectors; Apache Superset supports Trino, Hive, Spark SQL, Presto, and many other systems that ultimately execute batch jobs to query data.**
- **The two patterns pull in opposite directions**: pre-aggregation trades flexibility for speed on known questions; ad hoc querying trades speed for the ability to ask new ones. **Most organisations need both, which is why the lakehouse keeps raw data alongside the cubes.**

## Examples & Systems
Apache Iceberg (table format), Unity Catalog; Druid and Pinot for real-time OLAP; Tableau, Power BI, Looker, Apache Superset.

## Since the 1st Edition
**New as a subtopic.** The 1st edition covered analytics in its storage chapter and treated batch processing as a separate concern. **The 2nd edition makes the connection explicit** and introduces **the data lakehouse by name**, with its table-format and catalog layers — an architecture that did not exist in 2017.

## Related
- up: [[Batch Use Cases (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Cloud Data Warehouses (2e)]] — the query engine / storage format / table format / catalog unbundling
- [[Materialized Views and Data Cubes (2e)]] — the pre-aggregation machinery
- [[Data Storage for Analytics (2e)]] — the storage side
