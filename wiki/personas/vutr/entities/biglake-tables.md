---
persona: vutr
kind: entity
sources:
- raw/google-infrastructure/i-spent-5-hours-learning-how-google.md
last_updated: '2026-07-15'
qc: passed
slug: biglake-tables
topics:
- google-infrastructure
---

Before BigLake, BigQuery could query object-storage data only through read-only external tables. As customers pushed for a lakehouse pattern, Google introduced BigLake tables in 2022 to make external open-source data-lake tables (Parquet, Apache Iceberg) a first-class concern inside BigQuery, with three explicit goals: the same enterprise data-management capabilities regardless of where the data physically lives, availability of those capabilities to other engines like Spark and Presto/Trino, and one platform spanning BigQuery-managed storage and object storage alike. The mechanism rests on two ideas — BigLake uses BigQuery's internal catalog, not the open format's own metadata files, as the source of truth for a table, and it exposes BigLake tables to any engine through the Read/Write [[bigquery-storage-api|Storage API]] rather than a format-specific reader.

The access model is the more consequential design choice. Normally, an engine reading object storage forwards the user's own credentials to the object store for authorization — but that breaks BigQuery's governance model in two ways: it gives users direct access to raw data, bypassing BigQuery's own data masking and row-level security, and it doesn't give BigLake the storage access it separately needs for background work like metadata cache refresh or reclustering. Instead, BigLake uses a delegated access model: each table is associated with a connection object carrying a read-only service-account credential to the object store, and that one connection object can be shared across many tables (typically one per data lake). The Read API becomes the enforced security trust boundary — fine-grained access controls (column security, data masking, row-level filtering) are applied there, before data ever reaches the query engine, so the query engine itself is granted zero trust.

BigLake tables also get a performance layer on top: Google's internal BigMetadata system (the same metadata-management layer BigQuery uses for its own native tables) caches file names, partitioning information, and physical file metadata — size, row counts, per-file column statistics — in a columnar cache, tracked at finer granularity than systems like Hive Metastore, which gives BigQuery or an external engine like Spark more surface for building optimized query plans. Importantly, BigLake tables still defer to the open table format's own metadata mechanism (e.g. Iceberg's metadata-in-object-storage) as ground truth; BigMetadata only caches and centralizes what it reads from there, cutting down on excessive file-listing calls rather than replacing the format's bookkeeping. That's the contrast with [[biglake-managed-tables]], where Google's metadata layer stops being a cache and becomes the source of truth outright.

*See also: [[biglake-managed-tables]] · [[bigquery-storage-api]] · [[colossus-and-borg-as-shared-substrate]]*
