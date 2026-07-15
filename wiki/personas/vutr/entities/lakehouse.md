---
persona: vutr
kind: entity
sources:
- raw/lakehouse-architecture-and-practical-builds/do-we-need-the-lakehouse-architecture.md
- raw/lakehouse-architecture-and-practical-builds/the-6-questions-you-must-answer-when.md
- raw/lakehouse-architecture-and-practical-builds/data-architecture-101.md
- raw/lakehouse-architecture-and-practical-builds/the-data-lake-warehouse-and-lakehouse.md
- raw/lakehouse-architecture-and-practical-builds/build-a-lakehouse-on-a-laptop-with.md
- raw/lakehouse-architecture-and-practical-builds/bauplan-operate-your-lakehouse-with.md
last_updated: '2026-07-15'
qc: passed
slug: lakehouse
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

Vu's lakehouse notes are built directly on Databricks' 2020 CIDR paper, "Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics." Databricks' framing question was: is it possible to turn data lakes based on open formats like Parquet into high-performance systems that provide both the management features of a warehouse and fast, direct I/O for advanced analytics? Their answer, the lakehouse, is a data management system built on low-cost object storage that adds traditional analytical-DBMS features on top: ACID transactions, versioning, caching, and query optimization. Vu's own restating across multiple posts is consistent: the lakehouse combines the low cost and openness of the [[data-lake]] with the management features of the [[data-warehouse]], resolving the two-tier lake-plus-warehouse architecture's problems — reliability (costly ETL between two systems), data staleness (the warehouse always lags the lake), poor support for advanced analytics (ML frameworks reading via ODBC/JDBC, or needing exports, rather than the lake's native file formats), and total cost of ownership (paying for storage twice).

**The mechanism: a metadata layer over object storage.** The key technical move, per Vu, is adding a transactional metadata layer on top of files sitting in low-cost object storage — a layer that tracks which objects belong to which table and layers on ACID transactions, versioning, and time travel without giving up the storage layer's low cost. Candidates for this metadata layer are Delta Lake (Databricks, 2016), Apache Iceberg (started at Netflix), and Apache Hudi (started at Uber, focused on streaming ingest). Because the metadata layer is what a query engine consults before touching data files, and ML frameworks like TensorFlow and Spark MLlib can already read the underlying Parquet, the "easiest way to integrate them with a Lakehouse" is simply to query the metadata layer for which files belong to a table and hand that list to the ML library — see [[lakehouse-metadata-layer-as-translator]] for the deeper mechanics and its own scaling problem.

**Query performance is the hard part.** Vu is explicit that a metadata layer alone doesn't buy warehouse-grade SQL performance — the engine still runs directly on raw data, so Databricks layers on caching, auxiliary statistics, and physical data-layout optimization to close the gap; see [[lakehouse-query-performance-techniques]].

**Where BigQuery and Snowflake fit — and don't.** Vu returns to this point in three separate posts: technically, BigQuery and Snowflake already decouple compute from storage (S3 for Snowflake, Colossus for BigQuery) behind a metadata/translation layer, which makes them lakehouse implementations by the letter of the definition. But they violate what Vu calls the "spirit of the lakehouse manifesto," because the vendor controls the storage layer and decides which query engines you may bring — the opposite of the lakehouse's promised interoperability. He does note the industry is closing this gap from both directions: BigQuery and Snowflake increasingly let you query data stored in your own object storage via Iceberg or Delta Lake, and open table formats increasingly let you attach BigQuery/Snowflake as just one of several possible query engines.

**Building one yourself is expensive.** In "The 6 questions you must answer when building a Lakehouse from scratch," Vu inverts the vendor's pitch: a self-built lakehouse hands you the giant object-storage system plus your choice of query engines, but that freedom comes with six hard decisions you'd otherwise get for free from a vendor — see [[lakehouse-build-decision-framework]]. His verdict, after walking through all six, is that self-managing every layer is highly resource-intensive, especially for a small team with no lakehouse experience; he recommends handing some components to a vendor (e.g., a managed Iceberg implementation, managed Spark/Flink) unless the organization genuinely needs full openness and has the resources of a very large company to support it — see [[every-decision-has-a-tradeoff]].

**Practical instances Vu actually built.** He built a laptop-scale lakehouse (MinIO + [[project-nessie]] + [[trino]] + dbt + Airflow, transforming AdventureWorks CSVs into a `curated` schema of Iceberg tables) to get hands-on with the stack, and separately covered [[bauplan]], a FaaS platform that positions itself as a way to *operate* a lakehouse (Iceberg + Nessie storage, serverless compute) with none of that infrastructure to manage.

*See also: [[data-lake]] · [[data-warehouse]] · [[kappa-architecture]] · [[lambda-architecture]] · [[data-mesh]] · [[medallion-architecture]] · [[trino]] · [[project-nessie]] · [[bauplan]]*

## Related in the other wiki
- [[ACID]] — DDIA's account of the transaction safety properties (atomicity, consistency, isolation, durability) that the lakehouse's metadata layer (Delta Lake, Iceberg, Hudi) is specifically built to bolt onto otherwise-plain object storage files.
