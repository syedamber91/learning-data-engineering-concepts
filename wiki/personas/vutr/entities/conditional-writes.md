---
persona: vutr
kind: entity
sources:
- raw/iceberg-hudi-delta-open-table-formats/i-spent-5-hours-to-understand-more.md
- raw/iceberg-hudi-delta-open-table-formats/i-spent-8-hours-relearning-the-delta.md
- raw/iceberg-hudi-delta-open-table-formats/how-do-iceberg-delta-lake-and-hudi.md
last_updated: '2026-07-15'
qc: passed
slug: conditional-writes
topics:
- iceberg
---

A conditional write is a single-object operation that succeeds or fails based on the object's *existing* state at write time — the canonical form is put-if-absent: "only write this object if no object with this key already exists." It is the object-storage primitive that lets multiple independent writers race to claim a name, with the store itself guaranteeing that exactly one of them wins.

Google Cloud Storage and Azure Blob Storage have offered atomic put-if-absent natively for a long time, and Delta Lake uses it directly to serialize commits into `_delta_log` (see [[delta-lake]]): the next sequential JSON log file can only ever be created once, by whichever writer's put-if-absent call lands first. Amazon S3 did not support this operation until August 2024. Before that, Delta Lake on S3 had to fake the same guarantee with an external coordination service — clients acquired a table lock via DynamoDB before writing a log record, purely to serialize who could claim the next log ID. Once AWS added native conditional writes to S3 in August 2024, that external locking dependency became unnecessary. On distributed filesystems like HDFS, the same effect is achieved differently — via atomic rename of a temporary file to its final name, which likewise fails if the target already exists.

Conditional writes are the mechanical answer to a gap the notes state directly: object storage gives Durability essentially for free (S3 and GCS both advertise eleven-nines durability), but it does not support atomic transactions across multiple objects. A table format's metadata commit is exactly that kind of multi-object problem in disguise — new data files plus a metadata update all need to become visible together, or not at all — and conditional writes are the one primitive strong enough to pin down "exactly one writer wins" without a full external transaction manager. See [[occ-on-object-storage]] for how each of the three formats builds its own atomic commit on top of this same underlying idea: Delta Lake uses conditional writes directly on its log file; Hudi layers an explicit lock on top of a conditional-write-style completed-file creation; Iceberg instead pushes the atomicity requirement onto its catalog (a transactional database, external to raw object storage), which must itself support an atomic compare-and-swap on the table's metadata pointer.

*See also: [[delta-lake]] · [[apache-hudi]] · [[apache-iceberg]] · [[iceberg-metadata-layer]] · [[occ-on-object-storage]] · [[hudi-timeline]]*
