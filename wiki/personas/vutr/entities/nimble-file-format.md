---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/why-there-are-so-many-parquets-alternative.md
last_updated: '2026-07-15'
qc: passed
slug: nimble-file-format
topics:
- parquet
---

Nimble (originally called Alpha) is a file format Meta introduced around 2024, aiming to replace both Parquet and ORC internally. Its focus is decode speed for sequential reads across wide tables — the workload Meta sees in feature engineering and model training — and, unlike [[lance-file-format|Lance]], it was explicitly **not** designed for random access: the source is direct that Nimble's encodings target fast sequential decoding, not point lookups.

Structurally, Nimble still horizontally partitions data into [[row-group]]s, the way Parquet does — so the same row-group sizing tension persists (Nimble relocates its footer metadata to the end of the file, an improvement over ORC's inline stripe footers, but Parquet already stores row-group metadata in its own footer, so this isn't a structural advantage over Parquet specifically). Within a row group, each column decomposes into one or more "streams": a nullable string column, for example, produces a nullability stream, a length stream, and a data stream, with encoding information stored directly inside each stream rather than centralized. The footer itself uses FlatBuffers instead of Thrift, so a query engine can read one column's information without deserializing the whole footer — directly addressing the [[footer-filemetadata|wide-table metadata bloat]] problem.

Nimble's governance model is the sharpest contrast with Lance: where Lance is an open spec that accepts multiple, potentially fragmented implementations, Nimble is a single canonical C++ library, and Meta explicitly discourages reimplementation. It supports many encodings and lets developers extend them, but consistency is enforced by there being only one implementation to keep in sync, rather than by a spec designed to tolerate divergence.

*See also: [[row-group]] · [[footer-filemetadata]] · [[lance-file-format]] · [[vortex-file-format]] · [[parquet-random-access-limitation]]*
