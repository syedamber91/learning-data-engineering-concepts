---
persona: vutr
kind: entity
sources:
- raw/iceberg-hudi-delta-open-table-formats/i-spent-5-hours-exploring-the-story.md
- raw/iceberg-hudi-delta-open-table-formats/why-walmart-chose-apache-hudi-for.md
- raw/iceberg-hudi-delta-open-table-formats/how-do-iceberg-delta-lake-and-hudi.md
- raw/iceberg-hudi-delta-open-table-formats/how-do-delta-lake-iceberg-and-hudi.md
last_updated: '2026-07-15'
qc: passed
slug: hudi-timeline
topics:
- iceberg
---

The Timeline is Hudi's record of every action ever taken against a table — ingestion, compaction, cleaning, everything — physically stored as files inside the `.hoodie` directory at the table's root. Each entry follows the pattern `<instant_time>.<action>[.<state>]`. The **instant timestamp** is a globally unique, monotonically increasing value that fixes the order actions began, which is what lets Hudi provide instantaneous, point-in-time views of the table and retrieve data in the exact order it arrived.

**Actions** name what kind of operation the instant represents: `COMMIT` (an atomic write of a batch of records to base files), `DELTA_COMMIT` (an atomic write to a Merge-on-Read table, which may touch both log files and base files), `COMPACTION` (a background action reconciling log files into base files — appearing itself as a special kind of commit), `CLEAN` (a background action removing outdated file versions), `ROLLBACK` (reverting a failed or partial commit), and `SAVEPOINT` (marking specific file versions as protected from cleaning, for disaster recovery).

**States** track an instant's progress through a strict three-step lifecycle, each transition physically recorded by creating a new file on the Timeline: `REQUESTED` (scheduled, not yet started), `INFLIGHT` (currently executing — new data is written during this phase but is not yet visible to any reader), and `COMPLETED` (finished; by convention the completed-state file carries no state suffix at all). The creation of that final, suffix-less completed file *is* the atomic event that finalizes the transaction — it is Hudi's concrete instance of the general object-storage commit pattern in [[occ-on-object-storage]], and like Delta Lake's log commit it relies on the object store's [[conditional-writes|conditional write]] primitive. Hudi's added twist is that the writer must also hold an explicit lock (Zookeeper, DynamoDB, or another configured provider) for that final step specifically — not for the transaction's full lifetime — during which it checks the Timeline for any commits that completed concurrently and aborts on a genuine conflict.

To keep read latency from growing as a table accumulates history, Hudi splits the Timeline into an **active timeline**, which serves ordinary read requests and stays bounded, and an **archived timeline**, into which older instants are moved past a configurable threshold; archived events live under `.hoodie/archived` and are kept only for bookkeeping and debugging, not for regular table operations.

*See also: [[apache-hudi]] · [[hudi-index]] · [[iceberg-metadata-layer]] · [[occ-on-object-storage]] · [[conditional-writes]] · [[copy-on-write-vs-merge-on-read]]*
