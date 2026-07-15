---
persona: vutr
kind: concept
sources:
- raw/uber-data-infrastructure-case-studies/how-did-uber-build-their-data-infrastructure.md
- raw/uber-data-infrastructure-case-studies/i-spent-5-hours-understanding-how.md
last_updated: '2026-07-15'
qc: passed
slug: uber-hudi-query-and-write-taxonomy
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Uber's motivating example for why it built Apache Hudi is concrete: a dataset of daily driver earnings, where a rider can tip hours after a trip completes — a driver earns $10 Monday night and gets a $1 tip Tuesday morning. Under pure batch processing, Uber can't know whether a given day's earnings record will change, so it has to conservatively assume "data was changed in the last X days" and reprocess all X partitions to reflect one tip. On the Uber Eats side, the same problem shows up as menu updates: on a given day Uber observed 408 million delta changes against 11 billion total entities — roughly 3.7% actually changed — yet a naive batch approach would reprocess the full 11 billion to catch that 3.7%, risking the freshness SLA. Hudi's premise is extracting only the update and applying it directly to the target table instead.

Structurally, Hudi tables use **two file formats**: columnar **base files** (e.g., Parquet) optimized for reading, and row-oriented **log files** (e.g., Avro) that capture changes on top of a base file, optimized for writing. A **Timeline** records every action performed on the table over time, giving both an instantaneous view of current state and efficient retrieval in arrival order. Each record carries a **primary key** — a record key plus the partition location — which lets Hudi guarantee no duplicate records across partitions, enables fast updates/deletes, and is backed by an index for quick lookups.

On the **read** side Hudi supports five query types: **Snapshot** (latest table state), **Time Travel** (a past snapshot), **Read Optimized** (like Snapshot but faster, because it reads only the columnar base files), **Incremental (Latest State)** (only new data written since a given point on the timeline — a "Hudi instant," a point-in-time marker for a single atomic action like a commit or compaction), and **Incremental (CDC)** (a variant of Incremental that emits database-like change-data-capture log streams). Uber uses Incremental (Latest State) for most of its reads and joins, across four patterns: incremental update from a single source table; consolidation of that incremental update with other raw tables via left outer join against a T-24hr incremental pull; consolidation with derived/lookup tables via left outer join restricted to only the affected partitions; and backfilling via Hudi's snapshot read across a start/end date boundary on one or more source tables.

On the **write** side, Hudi splits operations into Incremental (applying only the changes) and Batch (overwriting entire tables/partitions every few hours), then further into: **Upsert** (looks up the index to tag each record as new or existing, then packs it accordingly — no duplicates in the target); **Insert** (like Upsert but skips the index lookup, so it's faster but can produce duplicates); **Delete** (soft — keep the record key, null every other field — or hard — erase all evidence of the record); **Bulk Insert** (Insert's semantics plus a sort-based write algorithm, built to scale for initial data loads, since Insert/Upsert hold data in memory in a way that hurts first-load performance); **Insert Overwrite** (rewrites only the partitions present in the input); and **Insert Overwrite Table** (rewrites the whole table). Uber's write path further splits on table shape: for **partitioned tables**, upserts apply incremental updates, `insert_overwrite` handles backfilling by rewriting the affected partition, and non-incremental columns (fields whose updates don't drive incremental loading, e.g. a restaurant's city changing) are updated via targeted Spark SQL merge/update statements; for **non-partitioned tables**, upserts still apply incremental updates, but both incremental and non-incremental columns are updated via `insert_overwrite` against a full outer join between incremental rows and the target table.

*See also: [[uber-hudi-etl-pipeline-and-impact]] · [[marmaray]] · [[sparkle-etl-framework]] · [[uber-data-platform-evolution]]*
