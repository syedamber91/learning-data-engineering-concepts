---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: single-node-engines-duckdb-polars-vs-distributed-systems
---

Related: [[duckdb]] · [[polars]] · [[pandas]] · [[spark]] · [[apache-arrow]] · [[single-node-processing]]

## Comparisons
There's a natural spectrum by dataset size. [[pandas]] handles small data but runs out of room on anything medium; [[polars]] is my pick for medium data that fits in memory; and [[spark]] is reserved for genuinely distributed workloads. The blunt way I'd put it: for a medium-sized dataset there are no feasible options — Pandas is too limited and Spark is overkill — which is exactly the gap [[polars]] and [[duckdb]] were built to fill. [[duckdb]] and [[polars]] aren't competitors so much as neighbours: via [[apache-arrow]] they share data zero-copy, and [[duckdb]] additionally acts as an embedded OLAP engine (SQLite-for-analytics) with vectorized push-based execution.

## Open questions
- The source frames the medium-data gap qualitatively — at what dataset size, concretely, does Polars stop fitting in memory and Spark become worth the overhead?
- If [[apache-arrow]] gives zero-copy sharing between [[duckdb]] and [[polars]], when would you choose one over the other for the same in-memory workload?
- How far do the hardware trends (128GB RAM, Gen5 NVMe, AVX-512) push the ceiling before distributed processing is genuinely required again?

## Synthesis
The story here is that modern hardware has quietly rehabilitated [[single-node-processing]]: with 128GB RAM, fast NVMe, and SIMD, one machine now covers workloads that used to demand a cluster. [[duckdb]] and [[polars]] are the engines built for this moment — interoperating zero-copy through [[apache-arrow]] and filling the medium-data gap where [[pandas]] is too limited and [[spark]] is overkill. My standing rule stands: don't run on a multi-node framework what you can process on a single machine.

## Related topics
- [[apache-arrow]] — DuckDB and Polars interoperate zero-copy through Arrow, sharing in-memory data without re-serialization to fill the medium-data gap.
- [[spark]] — Spark is the distributed system these single-node engines are weighed against — reserved for genuinely distributed workloads where Polars and DuckDB are too small.
- [[olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks]] — DuckDB is the embedded, vectorized, PAX-based OLAP engine profiled among the warehouse-scale engines — SQLite-for-analytics on one node.
