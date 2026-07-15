---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/why-there-are-so-many-parquets-alternative.md
last_updated: '2026-07-15'
qc: passed
slug: lance-file-format
topics:
- parquet
---

Lance is a modern, open-source columnar data format designed for machine learning and multimodal AI, launched around 2022 by LanceDB (a YC W22 startup) explicitly to address Apache Parquet's performance limitations in AI workloads.

Its most radical structural choice is abandoning [[row-group]]s completely. A column's data is stored across multiple disk pages, but different columns can have different numbers of pages — columns don't need to be the same length — and each column writer keeps its own buffer, with no requirement that a column's pages even be contiguous. Metadata describing each page sits near the end of the file as a set of protobuf messages, one per column, referenced through an offset array and a footer — so the engine can read the protobuf metadata only for the columns it needs and skip the rest ([[footer-filemetadata]]).

Lance's answer to [[parquet-random-access-limitation|random access]] depends on value size. For small values (integers, short strings), it uses "miniblock" encoding — conceptually similar to a Parquet page, still requiring a chunk read-and-decode, but kept deliberately tiny so the decode cost per lookup is far smaller. For large values (vector embeddings, images, large text — the source's threshold is 128 bytes per value), it uses "full-zip" encoding, which interleaves each value's own metadata directly with its data and restricts compression to "transparent" schemes — ones where a single value can be decompressed without touching its neighbors. So fetching embedding #48 means jumping straight to it and decompressing only that value. In short, Lance achieves random access by doing less decode work per lookup than Parquet, using more targeted encodings, rather than by changing the fundamental columnar bet.

Because [[row-group]]s are gone, each column can be written at its own pace, sidestepping the row-group buffering/sizing constraint entirely. And because metadata is already split per-column, wide-table metadata bloat is avoided by construction. The trade-off is governance: Lance is an open *specification* rather than one canonical implementation, so the same fragmentation risk that affects Parquet across its Java/Python/C++/Go implementations applies to Lance too as more implementations appear.

*See also: [[row-group]] · [[footer-filemetadata]] · [[nimble-file-format]] · [[vortex-file-format]] · [[parquet-random-access-limitation]]*
