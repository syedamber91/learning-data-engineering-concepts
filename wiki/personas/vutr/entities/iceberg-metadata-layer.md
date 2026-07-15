---
persona: vutr
kind: entity
sources:
- raw/iceberg-hudi-delta-open-table-formats/i-spent-8-hours-learning-apache-iceberg.md
- raw/iceberg-hudi-delta-open-table-formats/i-spent-7-hours-diving-deep-into.md
- raw/iceberg-hudi-delta-open-table-formats/how-do-iceberg-delta-lake-and-hudi.md
- raw/iceberg-hudi-delta-open-table-formats/how-do-delta-lake-iceberg-and-hudi.md
- raw/iceberg-hudi-delta-open-table-formats/how-does-netflix-ensure-the-data.md
last_updated: '2026-07-15'
qc: passed
slug: iceberg-metadata-layer
topics:
- iceberg
---

Iceberg tracks a table's state as a three-layer, bottom-up hierarchy — data layer, metadata layer, catalog layer — where each layer tracks the layer below it, and the whole point of climbing it is to know exactly which files to open without ever listing a directory.

At the bottom, the **data layer** is just the actual data files (usually Parquet, though Iceberg also supports ORC and Avro) plus, when merge-on-read is in play, delete files that mark which rows in those data files no longer count.

Above it, the **metadata layer** is itself a small tree, read top-down at query time and written bottom-up at commit time:

- **Manifest files** (Avro) each list a subset of the table's data files. For every data file a manifest tracks, it stores column-level statistics computed during the write — minimum/maximum values, null counts — plus the file format. Because a single manifest file holds these stats for many data files at once, a reader opens one manifest file instead of every data file's own Parquet footer to decide what to skip.
- **Manifest lists** (Avro) are per-snapshot: each one is an array of structs, one per manifest file that makes up that snapshot, recording the manifest's location, which partition it belongs to, and the upper/lower bounds of the partition column values across the data files that manifest tracks. This is what lets a query planner discard whole manifest files — and therefore whole groups of data files — before ever opening one.
- **Table metadata files** (`metadata.json`) sit at the root of the tree for a given table version. Each one is a JSON document holding the table's current schema, its full history of snapshots (each with a sequence number and timestamp), the partitioning scheme, the sort order, and a pointer to the current manifest list.

At the top, the **catalog layer** is the single source of truth for where a table's *current* metadata file actually is: it maps a table identifier to a location, nothing more. Many backends can serve as the catalog — Hive Metastore, AWS Glue, Nessie, or Netflix's own Polaris — but whichever one is used, it must support one thing non-negotiably: atomically swapping that pointer. The write is only "done," and only visible to any reader, once the catalog's pointer has moved from the old metadata file's path to the new one; everything written before that swap (data files, manifests, the new metadata file itself) sits in object storage but is invisible and, if the swap never happens, becomes orphaned for later cleanup.

Reading walks this tree top-down: contact the catalog for the current metadata file, open it to get the schema and partition scheme and pick a snapshot (the current one, or an older one by timestamp/ID for time travel), follow that snapshot's manifest list, prune manifest files using the list's partition bounds, open the surviving manifest files and prune data files using their column bounds, then read only the data files that remain — pruning happens at two separate levels (manifest-list level, then manifest-file level) because Iceberg records statistics at both.

Writing walks the same tree bottom-up: contact the catalog to learn the current schema/partition scheme, write the new data files, write a manifest file recording their statistics, write a manifest list referencing that manifest (plus how many files/rows were added or deleted), write a new metadata file that reuses everything from the previous one but adds the new snapshot, and only then ask the catalog to swap its pointer to that new metadata file.

*See also: [[apache-iceberg]] · [[occ-on-object-storage]] · [[copy-on-write-vs-merge-on-read]] · [[iceberg-branching-and-wap-implementation]]*
