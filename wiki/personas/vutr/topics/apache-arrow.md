---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: apache-arrow
---

Related: [[apache-arrow]] · [[arrow-ipc]] · [[arrow-flight]] · [[record-batch]] · [[simd-memory-alignment]] · [[zero-copy-data-sharing]]

## Comparisons
- [[apache-arrow]] is deliberately **not** a disk format: unlike Parquet or CSV, which specify how data sits on disk, Arrow specifies how data sits in memory. The two layers are complementary, not competing.
- Within [[arrow-ipc]], the Streaming format is for sequential access while the File format is for random access — the File format's 'ARROW1' magic string at both ends is what makes it memory-mappable, which the Streaming format is not.
- [[arrow-flight]] and [[arrow-ipc]] are both about moving Arrow data, but Flight targets the network (RPC) while IPC targets the boundary between processes/files. Both preserve the native Arrow format so no re-serialization is needed.
- [[zero-copy-data-sharing]] is the payoff that [[record-batch]] immutability and [[simd-memory-alignment]] make practical: safe concurrent reads plus aligned buffers mean data can be shared and vectorized without copying.

## Open questions
- The source lists Polars, Pandas, Spark, Snowflake, BigQuery, DuckDB, DataFusion, and ClickHouse as leveraging Arrow, but does not say *which* parts (in-memory engine, [[arrow-flight]] transport, or [[arrow-ipc]]) each one uses.
- It states [[record-batch]] and Arrow arrays are immutable for safe concurrent access, but not how mutation/updates are handled in practice on top of an immutable format.
- The alignment guidance (8 or 64 bytes, AVX-512) is given, but the source doesn't quantify the actual [[simd-memory-alignment]] speedup.
- [[zero-copy-data-sharing]] is credited with eliminating serialization cost, but the source doesn't detail the boundary cases where a copy is still unavoidable.

## Synthesis
The through-line here is that [[apache-arrow]] fixed a memory problem, not a disk problem: before it, every system paid CPU to serialize and deserialize at each boundary, and [[zero-copy-data-sharing]] made that tax largely disappear. The supporting machinery — immutable [[record-batch]] units for safe concurrency, [[simd-memory-alignment]] for vectorized speed, plus [[arrow-ipc]] and [[arrow-flight]] to move the format across files and networks unchanged — is why so much of the modern stack sits on it. Fairly speaking, as Vu puts it, the data engineering field would look different without Arrow.
