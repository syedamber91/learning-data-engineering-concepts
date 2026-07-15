---
persona: vutr
kind: concept
sources:
- raw/olap-cost-and-multi-engine-comparison/7-insights-to-help-you-learn-any.md
last_updated: '2026-07-15'
qc: passed
slug: olap-metadata-object-storage-vs-transactional-db
topics:
- olap-cost-and-multi-engine-comparison
---

Every OLAP table is, underneath, a collection of immutable files — which is exactly what makes concurrency and versioning tractable, since data once written is never modified in place, only ever superseded by new files. That leaves one unavoidable question every system must answer: what tells the engine *which* files currently make up a table's current version? vutr's notes name two structurally opposed answers, beyond the fundamental file-identification role, this same metadata also has to support transaction conflict checking, version control, query optimization, and governance.

The first approach keeps metadata as files in object storage: Apache Iceberg, Delta Lake, and Apache Hudi all write JSON or Avro metadata files that sit right next to the actual data in S3 or GCS, and every write creates a new metadata file enumerating exactly which data files compose the table's current version. The advantage is portability — because the metadata is just files following an open protocol, any engine that implements the protocol can read it, so you can query the same Iceberg table from Spark today and from Snowflake tomorrow with no coordination between them, since all the necessary information already lives in object storage rather than behind a proprietary API. The cost shows up at scale: once a table has grown to millions of files, the metadata files themselves become large enough to hurt read performance, and because that metadata is *also* sitting in object storage rather than in a fast local structure, even reading a single piece of it means a network round-trip.

The second approach keeps metadata in a transactional database instead — typically a specialized, high-speed key-value store or distributed RDBMS. Query time doesn't mean opening files to find the schema; it means asking a dedicated metadata service, which per vutr's notes is backed by something like FoundationDB for Snowflake or Google Spanner for BigQuery. DuckLake, the open table format built by MotherDuck (the company behind DuckDB), takes the same transactional-database approach rather than the file-based one. The advantage mirrors the first approach's disadvantage: metadata never explodes into millions of unwieldy files, because it was never files to begin with, and a real database gives sturdier transactional guarantees than raw object storage, with a database point-read being faster and simpler than fetching-and-parsing a metadata file over the network. The cost mirrors the first approach's advantage: the metadata is now locked inside a proprietary store, so it's harder for external tools to "understand" the data the way an Iceberg-reading tool can, and if that metadata database itself can't scale to the workload, every single operation funnels through it and it becomes the whole system's bottleneck. vutr notes DuckLake claims to have solved this scaling problem but says he had not, at the time of writing, looked into how.

*See also: [[cloud-warehouse-storage-pricing-dimensions]] · [[olap-data-skipping-zone-maps-partitioning-clustering]]*
