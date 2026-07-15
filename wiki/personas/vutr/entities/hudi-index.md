---
persona: vutr
kind: entity
sources:
- raw/iceberg-hudi-delta-open-table-formats/i-spent-5-hours-exploring-the-story.md
- raw/iceberg-hudi-delta-open-table-formats/why-walmart-chose-apache-hudi-for.md
last_updated: '2026-07-15'
qc: passed
slug: hudi-index
topics:
- iceberg
---

Every record in a Hudi table carries a "hoodie key" — a record key paired with the partition path the record belongs to (for non-partitioned tables, the record key alone). Hoodie keys give Hudi a uniqueness guarantee no other table format in this vault's notes maintains natively: no duplicate record key can exist across partitions (or, in a non-partitioned table, at all). Before Hudi 0.14.0 users had to supply the record key explicitly; from 0.14.0 onward Hudi can auto-generate one if it isn't specified.

The index is the structure that makes that guarantee cheap to enforce: it maps hoodie keys to the `fileId` of the file group holding that record. Once the first version of a record is written, its entry in the index — which file group owns it — never changes, even as the record itself is updated across many later file slices. That fixed mapping is what lets Hudi route an update or delete straight to the correct file group instead of scanning the table to find where a given key currently lives.

The notes are explicit that this is the feature that differentiates Hudi's design most sharply from Iceberg and Delta Lake: those two formats prune which files to open using column statistics (min/max, null counts) recorded in their metadata trees, but neither maintains a direct key-to-file lookup structure the way Hudi's index does. That trade-off traces directly back to why Hudi exists at all (see [[apache-hudi]]): Uber needed fast, targeted updates and deletes over a lake at record-level granularity, not just efficient full-partition scans.

The posts name that Hudi supports multiple index types (referencing Hudi's own documentation for the full list) without themselves describing how any specific index type is implemented internally — a genuine gap in what these sources cover, not something to fill in from outside knowledge.

*See also: [[apache-hudi]] · [[hudi-timeline]] · [[iceberg-metadata-layer]] · [[copy-on-write-vs-merge-on-read]] · [[occ-on-object-storage]]*
