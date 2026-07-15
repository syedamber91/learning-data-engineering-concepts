---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9.md
last_updated: '2026-07-15'
qc: passed
slug: safe-writes-and-schema-evolution-in-serving
topics:
- data-pipeline-design-framework
---

Vu Trinh groups three questions under "can the serving layer guarantee safe writes": atomicity, idempotency, and schema evolution — because a serving layer isn't just something you read from, it's something transformation jobs write into, and all three failure modes live at that write boundary.

**Atomicity** — an operation completes fully or has no effect — is free on most OLAP databases (BigQuery, Databricks, Snowflake are ACID-compliant by design). He shows where it isn't free with a concrete failure: uploading three CSV files to object storage is atomic per object, but not across all three, so if only one of three uploads succeeds, a data scientist reading that path gets a silently incomplete result — the storage layer has no way to signal that the set was supposed to be complete.

**Idempotency**, at the serving layer specifically, is about what happens when the *same logical write* arrives twice — a pipeline republishes today's partition after fixing a bug, and the serving layer has to decide whether the table ends up correct or duplicated. He lists four concrete absorption strategies: MERGE/upsert semantics (match on key, replace — repeated writes converge on one final state); overwrite-by-partition (a partition is the unit of truth, so writing it twice just replaces it twice); deduplication-on-write (the serving layer filters duplicates by key before persisting); and append-only-with-dedup-on-read (the table accepts everything and consumers deduplicate at read time via a "latest version" view) — which he flags as workable only when the serving layer purely can't do better, since it pushes complexity onto every consumer and makes the table less trustworthy.

**Schema evolution** covers what happens when fields get added, removed, or promoted (INT → BIGINT). He names five distinct strategies rather than one: table formats with native evolution (Delta, Iceberg, Hudi — schema changes are metadata operations with no data rewrite, and the format tracks which schema version each file was written under); additive-only evolution (only ever add nullable columns, never rename/drop/retype — restrictive but safe when many downstream systems depend on the table); versioned tables/snapshots (publish `user_v2`, `user_v3` and migrate consumers over time — heavier, but appropriate when a change is too risky to apply in place); schema registries (Confluent, AWS Glue — for streaming, producers register schemas and consumers fetch them, with compatibility rules enforced at publish time so an incompatible change is rejected before it ships); and verifying schema changes at build/CI time against a simulated new schema, to catch breakage before it reaches a production dashboard.

*See also: [[idempotency]] · [[physical-layout-partitioning-clustering-and-compaction]] · [[stale-or-incorrect-data-handling]]*
