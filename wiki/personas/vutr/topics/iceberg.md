---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: iceberg
---

Related: [[apache-iceberg]] · [[delta-lake]] · [[apache-hudi]] · [[hudi-index]] · [[hudi-timeline]] · [[iceberg-metadata-layer]] · [[copy-on-write-vs-merge-on-read]] · [[conditional-writes]] · [[open-table-formats]] · [[occ-on-object-storage]] · [[evaluate-before-adopting]]

## Comparisons
The three formats diverge most at the commit path. [[apache-iceberg]] does an atomic pointer swap in the catalog; [[delta-lake]] uses a put-if-absent write to `_delta_log`; [[apache-hudi]] creates a `.completed` file. All three rest on [[conditional-writes]] because object storage gives Durability for free but no multi-object atomic transaction — see [[occ-on-object-storage]].

- **Throughput:** [[delta-lake]]'s put-if-absent OCC caps at several transactions per second, a ceiling [[apache-hudi]] attacked with NBCC in v1.0 (2024).
- **Update model:** [[copy-on-write-vs-merge-on-read]] frames the read/write trade-off; [[delta-lake]] added deletion vectors as an alternative to full CoW rewrites, and [[apache-hudi]] leans on [[hudi-index]] to route updates to file groups.
- **Ecosystem fit:** DoorDash chose [[apache-iceberg]] over [[delta-lake]] because Delta is more Spark-centric while Iceberg has more mature Flink support.
- **Benchmarks (Walmart):** [[apache-hudi]]+Spark 3.x was most performant for batch (>5x faster than legacy); [[delta-lake]] was 27% faster than Hudi for streaming ingestion but Hudi compaction was faster, and Delta outperformed on ~40% of queries thanks to Z-ordering.
- **Scale story:** Netflix migrated ~1.5M Hive tables to [[apache-iceberg]] (from 600,000 Hive tables and 250M partitions) and built Polaris, a custom Iceberg metastore on CockroachDB, after Hive Metastore on RDS MySQL hit limits.

## Open questions
- Given [[delta-lake]]'s several-transactions-per-second OCC ceiling and Hudi's NBCC answer, does [[apache-iceberg]]'s atomic pointer swap face the same throughput wall, and how does it cope at high write concurrency?
- The Walmart benchmark splits by workload (Hudi wins batch, Delta wins streaming ingestion but Hudi compaction is faster) — under what concrete conditions does one format's advantage actually flip in production?
- If [[hudi-index]] is the feature that sets Hudi apart, why hasn't it translated into the wide adoption Iceberg and Delta enjoy?
- The source asserts you should run an MVP evaluation ([[evaluate-before-adopting]]) against real requirements — but which requirements are the decisive ones (engine fit, update pattern, transaction rate), and how do you weigh them?

## Synthesis
Under the hood these are all the same bet: put a separate, database-free metadata layer on object storage ([[open-table-formats]]) and get ACID from [[conditional-writes]], since Durability is free but multi-object atomicity is not ([[occ-on-object-storage]]). Where they split is the commit mechanism and update model — [[apache-iceberg]]'s pointer swap and centralizing statistics, [[delta-lake]]'s put-if-absent plus deletion vectors and Z-ordering, and [[apache-hudi]]'s [[hudi-index]] and [[hudi-timeline]] built for incremental processing. The right choice is workload- and engine-specific, which is exactly why [[evaluate-before-adopting]] matters: run an MVP against your real requirements rather than following the hype.

## Related topics
- [[amazon-s3-gfs-hdfs-and-distributed-file-systems]] — Iceberg's open table formats sit directly on object storage, deriving free Durability from S3 while needing conditional writes because S3 gives no multi-object atomicity.
- [[big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter]] — Netflix migrated ~1.5M Hive tables to Iceberg and DoorDash chose Iceberg over Delta for Flink maturity, making Iceberg the table-format winner in these studies.
- [[data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa]] — Open table formats like Iceberg bolt ACID onto cheap object storage, which is exactly the mechanism that makes the lakehouse reconcile lake and warehouse.
- [[history-of-data-engineering]] — Open table formats like Iceberg are the present-day chapter of the history, reviving a clean-table-abstraction goal from 15+ years earlier.
- [[parquet]] — Iceberg is a table format layered over Parquet data files, centralizing the min/max statistics that the Parquet footer already carries.
