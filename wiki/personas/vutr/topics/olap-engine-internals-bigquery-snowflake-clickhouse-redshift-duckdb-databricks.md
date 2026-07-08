---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
---

Related: [[bigquery]] · [[snowflake]] · [[clickhouse]] · [[redshift]] · [[duckdb]] · [[databricks-photon]] · [[google-napa]] · [[vectorized-vs-code-compilation]] · [[shared-nothing-vs-shared-disk]] · [[acid-in-olap]]

## Comparisons
On execution engines, the field divides cleanly. [[bigquery]], [[snowflake]], [[clickhouse]], [[duckdb]], and [[databricks-photon]] all run vectorized execution (batch per operator pass), while [[redshift]] instead specializes C++ code per query and caches it via Compilation-as-a-Service — see [[vectorized-vs-code-compilation]].

On storage layout, [[clickhouse]] is true DSM (each column stored separately), whereas [[bigquery]] and [[snowflake]] use a PAX-style layout (Snowflake's format predates Parquet). [[clickhouse]]'s MergeTree and [[google-napa]] both lean on LSM-trees.

On architecture, [[bigquery]], [[snowflake]], and [[databricks-photon]] are shared-disk, while [[clickhouse]], [[duckdb]], and [[redshift]] (non-RA3) are shared-nothing — though [[snowflake]] is shared-nothing inside its compute layer despite separating compute and storage (see [[shared-nothing-vs-shared-disk]]).

On operations, [[redshift]] stands alone as the only one explicitly using ML (XGBoost in AutoWLM) to predict query time. On transactions, [[snowflake]] and [[duckdb]] both bring ACID via MVCC, an oddity worth chewing on (see [[acid-in-olap]]).

## Open questions
- If ACID is unnecessary in the OLAP world, why are open table formats like Delta Lake and Apache Iceberg being built to make object storage more ACID? (see [[acid-in-olap]])
- Why does [[bigquery]] restrict itself to hash joins only, and what does that cost for certain workloads?
- [[redshift]] is the only OLAP system explicitly using ML (XGBoost in AutoWLM) for operations — why haven't the others followed?
- [[snowflake]] does not support partial retries and is not distributed across AZs by design — what are the availability implications of these choices?
- [[duckdb]] can only parallelize over row groups; how much does the 'at least as many row groups as CPU threads' rule constrain real workloads?

## Synthesis
Reading these OLAP internals side by side, the real fault lines are execution strategy and architecture, not branding: [[vectorized-vs-code-compilation]] separates the vectorized crowd ([[bigquery]], [[snowflake]], [[clickhouse]], [[duckdb]], [[databricks-photon]]) from [[redshift]]'s code specialization, while [[shared-nothing-vs-shared-disk]] cuts across the same names. What surprised me most was that these design choices are pragmatic and specific — [[bigquery]]'s dynamic Dremel plans, [[clickhouse]]'s sparse-index-per-granule DSM, [[redshift]]'s XGBoost AutoWLM — and that ACID keeps reappearing ([[acid-in-olap]]) even where we assumed analytics could ignore it. I used to think BigQuery was five times more advanced than Redshift before reading this.
