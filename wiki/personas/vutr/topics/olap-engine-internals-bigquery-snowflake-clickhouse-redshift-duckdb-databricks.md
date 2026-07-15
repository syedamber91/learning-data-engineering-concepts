---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
---

Related: [[bigquery]] · [[snowflake]] · [[clickhouse]] · [[redshift]] · [[duckdb]] · [[photon]] · [[google-napa]] · [[vectorized-vs-code-compilation]] · [[shared-nothing-vs-shared-disk]] · [[acid-in-olap]]

## Comparisons
On execution engines, the field divides cleanly. [[bigquery]], [[snowflake]], [[clickhouse]], [[duckdb]], and [[photon]] all run vectorized execution (batch per operator pass), while [[redshift]] instead specializes C++ code per query and caches it via Compilation-as-a-Service — see [[vectorized-vs-code-compilation]].

On storage layout, [[clickhouse]] is true DSM (each column stored separately), whereas [[bigquery]] and [[snowflake]] use a PAX-style layout (Snowflake's format predates Parquet). [[clickhouse]]'s MergeTree and [[google-napa]] both lean on LSM-trees.

On architecture, [[bigquery]], [[snowflake]], and [[photon]] are shared-disk, while [[clickhouse]], [[duckdb]], and [[redshift]] (non-RA3) are shared-nothing — though [[snowflake]] is shared-nothing inside its compute layer despite separating compute and storage (see [[shared-nothing-vs-shared-disk]]).

On operations, [[redshift]] stands alone as the only one explicitly using ML (XGBoost in AutoWLM) to predict query time. On transactions, [[snowflake]] and [[duckdb]] both bring ACID via MVCC, an oddity worth chewing on (see [[acid-in-olap]]).

## Open questions
- If ACID is unnecessary in the OLAP world, why are open table formats like Delta Lake and Apache Iceberg being built to make object storage more ACID? (see [[acid-in-olap]])
- Why does [[bigquery]] restrict itself to hash joins only, and what does that cost for certain workloads?
- [[redshift]] is the only OLAP system explicitly using ML (XGBoost in AutoWLM) for operations — why haven't the others followed?
- [[snowflake]] does not support partial retries and is not distributed across AZs by design — what are the availability implications of these choices?
- [[duckdb]] can only parallelize over row groups; how much does the 'at least as many row groups as CPU threads' rule constrain real workloads?

## Synthesis
Reading these OLAP internals side by side, the real fault lines are execution strategy and architecture, not branding: [[vectorized-vs-code-compilation]] separates the vectorized crowd ([[bigquery]], [[snowflake]], [[clickhouse]], [[duckdb]], [[photon]]) from [[redshift]]'s code specialization, while [[shared-nothing-vs-shared-disk]] cuts across the same names. What surprised me most was that these design choices are pragmatic and specific — [[bigquery]]'s dynamic Dremel plans, [[clickhouse]]'s sparse-index-per-granule DSM, [[redshift]]'s XGBoost AutoWLM — and that ACID keeps reappearing ([[acid-in-olap]]) even where we assumed analytics could ignore it. I used to think BigQuery was five times more advanced than Redshift before reading this.

## Related topics
- [[apache-arrow]] — Vectorized OLAP engines like DuckDB, ClickHouse, Snowflake, and BigQuery leverage Arrow's aligned, SIMD-friendly in-memory format.
- [[apache-pinot-druid-and-real-time-olap]] — Pinot and Druid are real-time OLAP engines built on the same columnar, immutable-segment internals as the warehouse-scale OLAP engines.
- [[lsm-tree-storage-engines]] — ClickHouse's MergeTree and Google Napa lean on LSM-trees, and BigQuery's Vortex WOS-to-ROS transition is the LSM pattern surfacing in OLAP.
- [[storage-models-nsm-dsm-pax-and-column-store]] — The engines split on storage layout — ClickHouse and Redshift are true DSM while BigQuery, Snowflake, and DuckDB use PAX — the exact taxonomy of the storage-models note.
- [[single-node-engines-duckdb-polars-vs-distributed-systems]] — DuckDB is the embedded, vectorized, PAX-based OLAP engine profiled among the warehouse-scale engines — SQLite-for-analytics on one node.
- [[google-infrastructure]] — extends this topic's BigQuery entry outward: the Storage API, BigLake, and BigLake Managed Tables are BigQuery reaching for the lakehouse on the same Colossus/Borg/Dremel foundation this topic already names, and Superluminal (BigQuery's Read API execution engine) turns out to be the same engine YouTube's Procella built first.
- [[olap-cost-and-multi-engine-comparison]] — that topic covers what these same engines cost to run (compute-unit pricing, storage pricing dimensions) and how they manage metadata, materialized views, and real-time freshness; its Redshift deep dive (managed storage, code generation, ML-driven self-tuning) is the one engine in this topic's roster this vault had not yet grounded in a dedicated raw source.
- [[clickhouse-internals]] — a full deep-dive on the ClickHouse entry this topic only sketches: MergeTree's part/granule/mark mechanics, Raft-based replication via ClickHouse Keeper, and ClickHouse's own production data-warehouse and Tinybird case studies.
- [[bigquery-internals]] — the grounded deep-dive behind this topic's one-paragraph [[bigquery]] and [[google-napa]] entities: Dremel's static-to-dynamic query plan history, its disaggregated shuffle layer, the Vortex storage engine, Big Metadata/CMETA, and the Capacitor file format, all sourced from vutr's own nine BigQuery posts.
- [[data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa]] — BigQuery and Snowflake, profiled here for their engine internals, are the same two systems Vu names as technically-lakehouse-but-spirit-violating: they already decouple compute (this topic's vectorized engines) from object-style storage behind a vendor-controlled metadata layer, which is exactly the translation-layer mechanism the lakehouse topic covers as something a self-built lakehouse must instead own.
- [[snowflake-internals]] — this topic's Snowflake entry (founders, PAX format, consistent hashing, FoundationDB, Snapshot Isolation) is a one-paragraph compression of the full internals deep-dive that topic covers: ephemeral storage caching, locality-aware scheduling, VW multi-tenancy economics, min-max pruning, and schema-less semi-structured columnarization.
