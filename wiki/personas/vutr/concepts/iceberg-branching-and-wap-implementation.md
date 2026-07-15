---
persona: vutr
kind: concept
sources:
- raw/iceberg-hudi-delta-open-table-formats/how-does-netflix-ensure-the-data.md
last_updated: '2026-07-15'
qc: passed
slug: iceberg-branching-and-wap-implementation
topics:
- iceberg
---

Every write to an Iceberg table already produces a new snapshot — a new manifest list plus a pointer to it — and Iceberg keeps every snapshot it has ever created, addressable by ID or timestamp. **Tags** and **branches** are named references built on top of that existing snapshot history, not a separate mechanism: a tag is a read-only name pinned to one specific snapshot, while a branch is an updatable named lineage — its own sequence of snapshots with a "head" pointing at the most recent one — that can itself be configured with a maximum snapshot age (time-to-live) and a minimum snapshot count. The table's ordinary current state is simply its `main` branch. Because Iceberg stores this history as a tree structure much like git — only the files that actually changed get rewritten for a new snapshot, with the rest of the data and metadata reused — the git-commit analogy the notes lean on isn't just a teaching device; the underlying data structure genuinely works the same way.

Branching in Iceberg comes in two distinct flavors, and the notes are explicit that the choice between them is a scale decision, not a matter of one being strictly better:

- **Table-level branching** (native to Iceberg) creates an isolated branch on one specific table. It captures per-table changes cleanly but becomes overhead-heavy if you need to reproduce a whole production environment — many tables, each needing its own branch — for a staging or testing pass.
- **Catalog-level branching** (via Project Nessie as the catalog) takes a snapshot of the *entire* catalog at once, letting a user replicate a full multi-table production environment in one operation. This is more powerful at scale, but the notes describe it as potentially "too much" machinery for a small-scale use case that only needs one or two tables isolated.

**Write-Audit-Publish (WAP)** is the concrete pattern this branching mechanism was built to support, and Netflix uses it to guard the quality of thousands of Iceberg tables before Netflix's internal downstream consumers ever see new data: (1) create a branch on the table; (2) point writes at that branch instead of `main` — the Iceberg-Spark extensions include configuration specifically to stage writes to a predefined branch rather than the table's live state; (3) run the internal data auditor against the data sitting in that branch, which is otherwise fully hidden from ordinary readers; (4) if the audit passes, fast-forward the branch's changes onto `main` — the same operation, and the same mental model, as merging a git pull request. Because the "hidden" and "published" states of the data are the same physical files with only the visibility pointer changed, auditing this way costs an extra read-and-check pass, not a second write-and-storage pass — which is the specific reason WAP needs Iceberg's snapshot/branching mechanics rather than being achievable with any table format that merely stores files. See [[write-audit-publish-pattern]] for more on the Write-Audit-Publish pattern itself.

*See also: [[apache-iceberg]] · [[iceberg-metadata-layer]] · [[netflix-iceberg-ecosystem-and-migration]] · [[occ-on-object-storage]]*
