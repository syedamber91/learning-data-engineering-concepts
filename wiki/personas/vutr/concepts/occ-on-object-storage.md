---
persona: vutr
kind: concept
sources:
- raw/iceberg-hudi-delta-open-table-formats/how-do-delta-lake-iceberg-and-hudi.md
- raw/iceberg-hudi-delta-open-table-formats/how-do-iceberg-delta-lake-and-hudi.md
- raw/iceberg-hudi-delta-open-table-formats/5-insights-to-help-you-learn-any.md
- raw/iceberg-hudi-delta-open-table-formats/i-spent-8-hours-relearning-the-delta.md
- raw/iceberg-hudi-delta-open-table-formats/i-spent-5-hours-exploring-the-story.md
last_updated: '2026-07-15'
qc: passed
slug: occ-on-object-storage
topics:
- iceberg
---

Object storage gives a table format Durability essentially for free — S3 and GCS both advertise around eleven-nines durability — but it gives nothing for Atomicity: a single object write is atomic, but there is no native way to make writes to multiple objects (new data files plus a metadata update) succeed or fail together. Every atomicity and isolation guarantee Iceberg, Delta Lake, and Hudi offer is therefore something the *format* has to build, not something object storage hands over.

All three land on the identical strategy: **optimistic concurrency control (OCC)**. Each writer works entirely against its own isolated snapshot of the table — writing new data files (and, in Iceberg's case, new metadata files) that no reader can see yet — and only at the very end attempts a single atomic commit step. Exactly one writer can win that step; whoever loses must check whether their change actually conflicts with what the winner committed and, if not, retry against the new state. This is the same OCC-with-serializable-snapshot-isolation pattern this vault describes at the general database level in [[isolation-levels-and-mvcc]] (read committed → snapshot isolation → serializability, with serialized snapshot isolation as OCC's specific mechanism) — the table formats are simply a concrete production instance of that same ladder, landing on SSI rather than two-phase locking because holding locks across a slow object-storage round trip would be brutal for throughput.

Where the three formats genuinely diverge is *what the single atomic commit step actually is*:

- **Iceberg** pushes the requirement onto its catalog rather than onto raw object storage: the catalog (a transactional database — Hive Metastore, Glue, Nessie, Netflix's own Polaris) must support an atomic compare-and-swap of the table's metadata pointer — "if the pointer is still `v1.metadata.json`, swap it to `v2.metadata.json`." Two writers racing both start from the same old pointer; the first to swap wins, and the second's swap attempt simply fails outright, forcing it to reload and check for real conflicts before retrying as `v3`. See [[iceberg-metadata-layer]].
- **Delta Lake** commits by [[conditional-writes|conditional write]] directly against object storage: only one writer can successfully create the next sequential `_delta_log` JSON file via put-if-absent (natively on GCS/Azure; via an external DynamoDB lock pre-August-2024 on S3, native conditional writes after). See [[delta-lake]].
- **Hudi** commits by creating a `<instant>.<action>.completed` file — also a conditional-write-style operation — but additionally requires an explicit external lock (Zookeeper, DynamoDB, or another provider), held only for the duration of that final step, during which the writer checks the Timeline for conflicting commits. See [[hudi-timeline]].

The throughput consequence is sharpest in Delta Lake, where the notes are explicit: because the commit step is gated by object-storage write latency (tens to hundreds of milliseconds per put-if-absent call), Delta's write-transaction rate tops out at "several transactions per second." Hudi's 2024 answer to a related pressure — Non-Blocking Concurrency Control (NBCC) — lets writers skip contending over the commit lock at write time entirely, deferring conflict resolution to the read or compaction pass instead. The notes never state Iceberg's own equivalent commit throughput, so whether its catalog-backed pointer swap faces the same kind of ceiling under heavy write concurrency is left open.

*See also: [[conditional-writes]] · [[iceberg-metadata-layer]] · [[delta-lake]] · [[apache-iceberg]] · [[hudi-timeline]] · [[apache-hudi]] · [[isolation-levels-and-mvcc]]*
