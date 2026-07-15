---
persona: vutr
kind: entity
sources:
- raw/iceberg-hudi-delta-open-table-formats/i-spent-8-hours-learning-apache-iceberg.md
- raw/iceberg-hudi-delta-open-table-formats/i-spent-7-hours-diving-deep-into.md
- raw/iceberg-hudi-delta-open-table-formats/why-do-we-need-open-table-formats.md
- raw/iceberg-hudi-delta-open-table-formats/i-spent-4-hours-learning-how-netflix.md
- raw/iceberg-hudi-delta-open-table-formats/how-do-doordash-evolve-realtime-processing.md
last_updated: '2026-07-15'
qc: passed
slug: apache-iceberg
topics:
- iceberg
---

Apache Iceberg was created at Netflix in 2017 by Ryan Blue and Dan Weeks specifically to fix what Hive could no longer tolerate at Netflix's scale: query correctness and the lack of stable atomic transactions on top of cloud object stores. Blue's own framing of the goal was blunt — "Iceberg tackled atomicity to make automation possible, even in cloud object stores." Beyond atomicity, the project also targeted performance (tracking the complete list of a table's data files at the file level instead of relying on directory listings for query planning) and simpler, less error-prone table operations and maintenance.

The architecture that resulted is the three-layer catalog/metadata/data hierarchy described in [[iceberg-metadata-layer]]: a catalog holding the single atomic pointer to the current metadata file, a metadata tree of manifest lists and manifest files carrying column statistics, and a data layer of Parquet (or ORC/Avro) files. Every write follows that tree bottom-up — write data, write a manifest, write a manifest list, write a new metadata file, then atomically swap the catalog's pointer — and every read walks it top-down, pruning first at the manifest-list level and then again at the manifest-file level before ever opening a data file.

Two features on top of that base architecture are specific enough to Iceberg to be worth naming directly:

- **Hidden partitioning and sort order** — covered in depth in [[iceberg-hidden-partitioning-and-sort-order]] — let Iceberg prune data by a column's transform (e.g., day-of-timestamp) without requiring users to know or filter on a separate physical partition column, and let historical partition schemes coexist without a full table rewrite when the scheme changes.
- **Row-level updates** are handled via the copy-on-write/merge-on-read split detailed in [[copy-on-write-vs-merge-on-read]]: copy-on-write (Iceberg's default) rewrites the affected data files outright; merge-on-read instead writes small delete files (positional or equality) that a reader merges against the base data at query time, with periodic compaction rewriting many small files into fewer, larger ones to keep that merge cheap. Compaction is a recurring background necessity in Iceberg generally: because every change is a new file, and no table format can rewrite files in place, an unchecked table only ever accumulates files, and more files always means slower reads (more opens, more footer/metadata overhead).

Iceberg's atomic commit is a specific instance of the pattern described in [[occ-on-object-storage]]: each writer works from an isolated snapshot, writes its data and metadata without disturbing readers, and only one writer can win the single atomic catalog-pointer swap — the loser must check for conflicts and retry against a new version.

Netflix's own operational history with Iceberg is a case study in its own right, covered in [[netflix-iceberg-ecosystem-and-migration]] (the Polaris catalog, cleanup/compaction/cross-region services, secure-table access, and the Hive-to-Iceberg migration tooling that moved roughly 1.5 million tables) and in [[iceberg-branching-and-wap-implementation]] (the tag/branch mechanism that Netflix's Write-Audit-Publish data-quality pattern depends on). DoorDash's own adoption story — choosing Iceberg over Delta Lake specifically for its more mature Flink integration, flexible schema/partition evolution, and active community — is covered in [[doordash-iceberg-realtime-migration]].

*See also: [[iceberg-metadata-layer]] · [[hudi-index]] · [[conditional-writes]] · [[hudi-timeline]] · [[open-table-formats]] · [[copy-on-write-vs-merge-on-read]] · [[netflix-iceberg-ecosystem-and-migration]] · [[iceberg-branching-and-wap-implementation]] · [[doordash-iceberg-realtime-migration]]*
