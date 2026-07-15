---
persona: vutr
kind: concept
sources:
- raw/clickhouse-internals/i-spent-8-hours-learning-the-clickhouse.md
last_updated: '2026-07-15'
qc: passed
slug: mergetree-merge-and-mutation
topics:
- clickhouse-internals
---

Because every insertion in MergeTree produces a new part, a table can accumulate many small parts over time; reads then have to open and close each one, hurting performance, and if merging weren't handled carefully, data could effectively be written twice — once on insert and again on merge. A background process exists purely to keep the part count manageable: it wakes periodically to check whether any parts should be merged, goes back to sleep if there's nothing to do, and otherwise applies heuristics based on part sizes, currently-running merges, and the total number of parts to pick which parts to combine. Parts can only merge with others holding adjacent block numbers, and a merge produces a new part one level higher than its inputs, with the original parts deleted once no query still references them (see [[mergetree-storage-engine]]).

MergeTree is optimized for append-only workloads and assumes updates and deletes are rare, so it offers two distinct paths for handling them rather than one. The first, used for `UPDATE`/`DELETE` DML, is a **mutation task**: ClickHouse finds the affected parts and rewrites them under an incremented version number. Mutations run asynchronously by default so multiple mutations can be batched into a single rewrite, amortizing the cost — but a mutation touching even a single row still requires rewriting the entire part, making it an expensive operation for high-frequency row-level changes. The second path, **lightweight deletes**, avoids rewriting parts at all: a delete just flips a bit in an internal bitmap column marking the row as deleted, and queries consult that bitmap to skip deleted rows from their results; the rows are only physically removed later, during a regular merge, at an unspecified time. Lightweight deletes trade a slightly slower query (checking the bitmap) for a much faster delete compared to a full mutation.

For workloads with genuinely heavy mutation volume, the source points to a specialized engine instead of either general path: **ReplacingMergeTree** treats a mutation as an insertion and keeps only the most recently inserted version of a record — identified by matching primary-key values and disambiguated by the created timestamp of the associated part — deleting older versions during the normal merge process.

*See also: [[mergetree-storage-engine]] · [[clickhouse-insert-process-and-idempotency]] · [[sparse-index-and-read-path]]*
