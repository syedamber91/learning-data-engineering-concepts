---
persona: vutr
kind: entity
sources:
- raw/lakehouse-architecture-and-practical-builds/build-a-lakehouse-on-a-laptop-with.md
- raw/lakehouse-architecture-and-practical-builds/bauplan-operate-your-lakehouse-with.md
last_updated: '2026-07-15'
qc: passed
slug: project-nessie
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

Project Nessie is the Iceberg catalog Vu picked for his laptop lakehouse build, and separately the catalog underneath [[bauplan]]'s storage layer. His stated reason for choosing it is direct: he found Nessie "the most mature catalog available on the market," and its git-like behavior — branches, commits — is what drew him in specifically. In his Trino build, a Nessie namespace is the logical container tables live under (analogous to a schema in Snowflake or a dataset in BigQuery), and each namespace maps to its own prefix in the underlying object storage.

The deeper reason Nessie matters, per the Bauplan post, is what it adds on top of Iceberg's own guarantees. Apache Iceberg, on its own, "only ensures atomic transactions at the table level" — a single table's changes are atomic, but nothing coordinates a commit that touches several tables at once. Nessie is an open-source versioned metadata catalog that sits above Iceberg specifically to close that gap: it enables cross-table transactions, letting users update multiple tables together with an all-or-nothing commit across all of them. Bauplan builds directly on this to give users a Git-like experience over their data — branch, commit, and merge tables the way you would source code — while Iceberg supplies the underlying data layer (data files, manifest files, manifest list, metadata files) that Nessie's catalog then versions as a whole.

*See also: [[trino]] · [[bauplan]] · [[lakehouse]] · [[lakehouse-metadata-layer-as-translator]]*
