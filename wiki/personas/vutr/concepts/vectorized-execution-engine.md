---
persona: vutr
kind: concept
sources:
- raw/duckdb-polars-single-node-engines/i-made-110-in-duckdb.md
- raw/duckdb-polars-single-node-engines/why-single-node-engine-like-duckdb.md
last_updated: '2026-07-15'
qc: passed
slug: vectorized-execution-engine
topics:
- single-node-engines-duckdb-polars-vs-distributed-systems
---

"Vectorization" here has nothing to do with a vector database — it's about how many records get processed at a time. Traditional systems like PostgreSQL, MySQL, or SQLite process each row sequentially behind the scenes. DuckDB instead processes data in a vectorized style: it operates on a "batch of values" at once rather than one row at a time.

This isn't a DuckDB invention. The approach is inspired directly by the 2005 paper *MonetDB/X100: Hyper-Pipelining Query Execution* (Boncz, Zukowski, Nes). That paper's argument is that the "volcano" processing model — where each parent operator requests a single record at a time from its child — doesn't leverage the full power of modern CPUs. Batching records into a vector and processing that vector at once enhances performance significantly, and the paper has had a very important impact on the design of many OLAP databases since. BigQuery, Databricks (via its Photon engine), and Snowflake all apply vectorized execution engines — this is not a niche technique, it's close to the default for modern OLAP internals.

Vectorization is also one of the three concrete mechanisms behind why single-node engines are fast on small-to-medium datasets in the first place: alongside no cluster cold-start overhead and mostly-local data exchange, modern CPUs' SIMD instruction sets (like AVX-512) let a single core perform the same operation on multiple data points simultaneously — for example, adding 16 pairs of numbers at once instead of pair by pair. Software that exploits these instructions — vectorized execution — can achieve far better performance, and both DuckDB and Polars are built to optimize performance via vectorized execution plus SIMD.

One deliberate distinction worth holding onto: the *vectorized execution engine* (how many records are processed per operator step) and the *Vector* in-memory storage format DuckDB uses internally are two different concepts, even though they share a name — see [[duckdb-vector-formats]] for the latter.

*See also: [[duckdb-vector-formats]] · [[push-based-vs-pull-based-dataflow]] · [[duckdb-embedded-analytics-model]]*
