---
persona: vutr
kind: concept
sources:
- raw/duckdb-polars-single-node-engines/i-made-110-in-duckdb.md
last_updated: '2026-07-15'
qc: passed
slug: push-based-vs-pull-based-dataflow
topics:
- single-node-engines-duckdb-polars-vs-distributed-systems
---

Beyond how many records move at once ([[vectorized-execution-engine]]), there's a separate question: which direction do they move in between operators? In the past, DuckDB's execution model operated in a pull-based fashion — an operator exposes a function that lets a parent fetch a result chunk from it, and parent operators keep pulling from their children through this interface until they reach a source node at the bottom of the plan tree.

Following DuckDB's own author, that approach works fine at first but runs into real problems: code duplication, and operators being unable to execute separately from the tree plan they belong to (the project tracked this as a concrete GitHub issue). To fix it, DuckDB changed its model to a push-based fashion, where child operators actively push their output data up to the parent instead of passively waiting to be called and asked to emit it.

This is presented as an internals detail rather than a fully resolved deep-dive — the source describes it as an introductory treatment, with a promise of a possible future deep dive into vectorization and push/pull dataflow specifically. It's still concrete enough to place other OLAP engines on the same axis: BigQuery and Databricks (Photon) are named as pull-based, while Snowflake is named as push-based — the same split that shows up independently in which engines use vectorized execution (BigQuery, Snowflake, ClickHouse, Databricks/Photon all do).

*See also: [[vectorized-execution-engine]] · [[duckdb-embedded-analytics-model]]*
