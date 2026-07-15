---
persona: vutr
kind: concept
sources:
- raw/bigquery-internals/i-spent-3-hours-trying-to-figure.md
last_updated: '2026-07-15'
qc: passed
slug: immutable-storage-sets-and-dml
topics:
- bigquery-internals
---

BigQuery's data files on Colossus are immutable — once written, a file is never modified again — and Vu treats that single fact as the key to how INSERT, UPDATE, and DELETE all actually execute. Immutability is what lets BigQuery hand a copy of a data file to a hundred workers without worrying that one of them will see a modification another is mid-write on, and it's what makes maintaining min-max metadata for filtering cheap — a mutable file would force a min-max recalculation on every edit. It's also what makes features like Data Snapshot, Time Travel, and Data Cloning tractable: every modification produces whole new files rather than editing existing ones (Snowflake, Databricks, and Redshift share this same immutable-storage foundation, per Vu's note).

BigQuery doesn't treat an individual file as the atomic unit of a table's data — it groups files into a **storage set**, created in response to a load job, a streaming job, or a DML query. Because a transaction always creates a new set of files (immutability leaves no other option), storage sets are themselves immutable. A storage set exists to buy ACID guarantees on top of immutable files: atomic (all its files land or none do), consistent (once committed, visible everywhere), isolated (transactions run independently of each other), and durable (survives after commit). Its lifecycle is a strict progression: `PENDING` while files are still being written (invisible to users the whole time), `COMMITTED` once writing finishes (only now does its data become visible), and `GARBAGE` once nothing references it any longer, marking it for collection. Storage sets also carry size information, which is what powers BigQuery's dry-run estimate of bytes a query would scan without running it.

With that machinery in place, the three DML operations become variations on "create new files, retire old storage sets." **INSERT** simply writes the new rows into a fresh set of files belonging to a new storage set, recorded in table metadata (committed timestamp, member files, owning table). **DELETE** is more involved precisely because files can't be edited: to remove a row with `id = ABC` living in file `Z` (itself part of storage set 1 alongside files `X` and `Y`), BigQuery writes a new file `Z2` — identical to `Z` except for the deleted row — as part of a new storage set 2, which points at `X`, `Y`, and `Z2` (not `Z`); storage set 1 is then marked `GARBAGE`. **UPDATE** is implemented as the combination of INSERT and DELETE: rather than editing a record, the system writes a new file holding the record's latest version and deletes the file holding the old one.

Constantly creating small storage sets and files this way causes **storage fragmentation** over time — Vu's example: writing 200KB every two minutes accumulates to 4TB after a month, but as many small files and storage sets, which slows queries down because BigQuery has to operate on all of that file-level metadata. A background storage optimizer periodically rewrites and compacts these many small files into larger ones to counter the fragmentation, running automatically without user involvement.

BigQuery's **time travel** — recovering a table's state at any point within a configurable 2-to-7-day window — rides directly on this same mechanism: because BigQuery tracks the timestamp of every storage-set transition, reverting to (or querying as of) an earlier point in time is a matter of resolving which storage sets were live at that timestamp, useful both for undoing an accidental delete and for inspecting data before a transformation was applied.

*See also: [[partitioning-and-clustering-bigquery]] · [[vortex-storage-engine]]*
