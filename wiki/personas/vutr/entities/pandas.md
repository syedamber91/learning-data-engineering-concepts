---
persona: vutr
kind: entity
sources:
- raw/duckdb-polars-single-node-engines/why-single-node-engine-like-duckdb.md
last_updated: '2026-07-15'
qc: passed
slug: pandas
topics:
- single-node-engines-duckdb-polars-vs-distributed-systems
---

Pandas (first released in 2008) sits at one end of the spectrum this topic maps out: alongside NumPy, it's named as the pre-single-node-engine option for processing data on a single machine, but one that can only handle small datasets — a limit the source attributes specifically to Python's global interpreter lock (GIL). Before DuckDB and Polars existed, that left a real market gap for anything medium-sized, since the only other option was cluster-based processing with Spark or a cloud data warehouse, which the source treats as overkill for that size of data ([[single-node-engine-market-gap]]).

Pandas is also the reference point for a familiar interface: Spark's DataFrame abstraction (introduced 2015) resonated with practitioners specifically because they were already used to that shape of API from Pandas ([[spark-in-memory-model-and-overhead]]). Separately, DuckDB's own author frames DuckDB as a tool that can potentially replace Pandas, backed by rich SQL and an extensive function library ([[duckdb-embedded-analytics-model]]).

*See also: [[duckdb]] · [[polars]] · [[single-node-engine-market-gap]]*
