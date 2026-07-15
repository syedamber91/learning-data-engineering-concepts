---
persona: vutr
kind: concept
sources:
- raw/clickhouse-internals/i-spent-8-hours-learning-the-clickhouse.md
- raw/clickhouse-internals/how-clickhouse-built-their-internal.md
last_updated: '2026-07-15'
qc: passed
slug: clickhouse-insert-process-and-idempotency
topics:
- clickhouse-internals
---

MergeTree supports two insert modes. In **synchronous mode**, each `INSERT` statement creates a new part directly — clients are expected to batch data before sending to avoid triggering excessive merges, but that batching requirement introduces latency that doesn't suit real-time use cases. In **asynchronous mode**, ClickHouse instead buffers rows from multiple `INSERT` operations and only forms a new part once the buffer exceeds a size threshold or a timeout expires.

Vu traces the actual insert path by building ClickHouse from source and following the code. After a table is registered (name, schema, engine, primary key, and other parameters), an `INSERT` goes through: SQL parsing → a sink that consumes a chunk of the inserted data and forms an in-memory block (sized via `min_insert_block_size_rows`, default ~1,048,449 rows, and `min_insert_block_size_bytes`, default 256 MB) → if the table is partitioned, ClickHouse determines which parts of the block belong to which partition → the block-writing process begins: column names/types are extracted, partition min/max values are computed if applicable, the part name and a temporary directory name (`tmp_insert_` + part name) are generated → the block's rows are sorted in memory by the sort/primary-key columns → a transaction begins, the temporary directory is created, and a "Wide" writer is initiated to write one file per column → each column is written to the page cache, compressed (LZ4 by default), and flushed to disk, with the mark file and primary index written at the same step → metadata files (`count.txt`, `column.txt`, `default_compression_codec.txt`, `checksums.txt`) are written → ClickHouse checks conditions (multi-table transaction use, overlapping/duplicate/empty parts) before renaming the temp directory to the part's real name → the transaction commits, and the loop repeats for any remaining data.

Two failure-adjacent concerns are handled explicitly. **Idempotent insert**: because a connection can time out mid-insertion, leaving the client unsure whether the write succeeded, the straightforward fix is to resend the data — so the ClickHouse server maintains a hash table of recently inserted parts and skips re-inserting a part already present in that table, making retried inserts safe. **Consistency**: by default ClickHouse offers only eventual consistency, which can bite a batch pipeline — a downstream step might read a staging table after only 3 of 4 nodes have received a write, seeing incomplete data. Setting `insert_quorum=n` (n = the cluster's total replica count) forces an insert to wait until data is replicated to all replicas before returning success, trading higher latency for guaranteed completeness — a trade-off the source calls acceptable for batch processing specifically.

ClickHouse's own internal data warehouse is the concrete case that motivated both mechanisms in production: because Airflow jobs/DAGs can retry the same data interval multiple times, tables there use the **ReplicatedReplacingMergeTree** engine, which resolves duplicates by keeping only the latest record per key — combined with hourly incremental/snapshot loads, this makes the DAG-retry-driven pipeline idempotent without manual dedup logic, and `insert_quorum` is the tool named for the partial-replica-read problem in that same warehouse.

*See also: [[mergetree-storage-engine]] · [[mergetree-merge-and-mutation]] · [[clickhouse-internal-data-warehouse-case-study]]*
