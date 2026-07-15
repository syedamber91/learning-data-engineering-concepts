---
persona: vutr
kind: concept
sources:
- raw/clickhouse-internals/i-spent-3-hours-learning-the-overview.md
- raw/clickhouse-internals/clickhouse-real-time-insight-in-15.md
last_updated: '2026-07-15'
qc: passed
slug: clickhouse-vectorized-parallel-execution
topics:
- clickhouse-internals
---

ClickHouse's query processing layer parses incoming queries and builds/optimizes logical and physical query plans. Its execution model is **vectorized** — the same family as DuckDB, BigQuery, or Snowflake — combined with **opportunistic code compilation**. Vu doesn't spell out the compilation mechanism beyond naming it, but the vectorized side is described concretely: instead of operators producing, passing, and consuming one row at a time, they operate on batches of rows ("data chunks") to minimize the overhead of virtual function calls per row.

Parallelism is applied at three distinct levels simultaneously, which the source frames as ClickHouse fully exploiting the hardware it's given:

- **Table shards** — if a table is sharded across multiple nodes, multiple nodes can scan their shards at the same time; this is how query processing scales out (more nodes) and, per node, up (more cores).
- **Data chunks** — on a single node, the query engine runs operators simultaneously across multiple threads, each operator consuming/producing chunks of rows rather than single rows (the vectorization described above).
- **Data elements** — within a single CPU core, multiple data elements inside a chunk are processed at once using SIMD instructions.

The same three-level framing recurs in the Tinybird-focused source, which restates it more briefly as parallelizing "across multiple levels, from distributing data across multiple nodes to processing batches of data in parallel using SIMD" — the two sources describe the same design from two different angles (an architectural walkthrough versus a practical "why is this fast" explanation).

*See also: [[mergetree-storage-engine]] · [[clickhouse-table-engines-and-integration-layer]] · [[clickhouse]]*
