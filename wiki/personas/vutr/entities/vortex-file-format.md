---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/why-there-are-so-many-parquets-alternative.md
last_updated: '2026-07-15'
qc: passed
slug: vortex-file-format
topics:
- parquet
---

Vortex is the youngest of the three Parquet-alternative formats the source covers, created at SpiralDB and claimed to be 100x faster than modern Apache Parquet for random-access reads. (Note: this is a distinct project from Google's BigQuery storage engine, also named Vortex — see [[vortex-storage-engine]] — the two share only a name.)

Vortex's differentiator is that both the *encoding* and the *physical layout* are extensible and composable. The same Vortex file spec can express a Parquet-like layout (row groups → chunks → pages), a Lance-like layout (no row groups, per-column chunking), or something else entirely, because the physical organization is described by a "layout FlatBuffer" — a tree of composable layout types such as FlatLayout (a single array), StructLayout (child layouts), ChunkedLayout (row-wise-partitioned child layouts), DictionaryLayout, and ZonedLayout (a zone-map of statistics for data skipping). The file itself is organized as data segments, followed by per-column statistics, a schema FlatBuffer, the layout FlatBuffer, a postscript FlatBuffer giving the location of the other sections, and an 8-byte end-of-file marker. Vortex's own default layout splits struct arrays into fields, repartitions each field into 8K-row chunks carrying zone-map statistics, repartitions again until chunks reach roughly 1MB uncompressed, then compresses each chunk with a BtrBlocks-inspired sampling compressor.

For [[parquet-random-access-limitation|random access]], Vortex chooses "transparent" encodings that remain navigable without full decompression — FastLanes bit-packing for integers, ALP for floating point, FSST for strings — paired with compute kernels that operate directly on the compressed data, so individual values stay addressable without decompressing their neighbors.

Vortex's answer to encoding-fragmentation (the same problem Nimble solves with one canonical library, and Lance accepts as a cost of its open spec) is, per the source, not yet implemented: a plan to embed WebAssembly decompression kernels directly inside the file, so a reader that doesn't natively support a given encoding could still decode the data via the file's own embedded WASM logic — letting Vortex evolve its encodings without breaking existing readers, a problem the source says has "plagued Parquet for years."

*See also: [[lance-file-format]] · [[nimble-file-format]] · [[row-group]] · [[footer-filemetadata]] · [[parquet-random-access-limitation]]*
