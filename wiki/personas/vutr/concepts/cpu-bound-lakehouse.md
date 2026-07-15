---
persona: vutr
kind: concept
sources:
- raw/parquet-file-format/i-spent-8-understanding-how-parquet.md
- raw/parquet-file-format/its-time-to-replace-parquet.md
- raw/parquet-file-format/why-there-are-so-many-parquets-alternative.md
last_updated: '2026-07-15'
qc: passed
slug: cpu-bound-lakehouse
topics:
- parquet
---

Since Parquet's [[parquet-origin|2013 origin]], storage and network performance have improved significantly, but CPU speed hasn't kept pace — and the lakehouse paradigm's shift toward high-bandwidth object storage means I/O is no longer the constraint it once was. Parquet's defaults, tuned in an I/O-bound world, are now being reconsidered from the opposite direction: the bottleneck has moved to decode and decompression CPU cost.

Two concrete threads follow from this, per the sources. First, cited (but not detailed by name beyond reference links) research proposes skipping general-purpose compression on Parquet pages entirely — accepting a larger file on disk in exchange for removing a decompression step before every read, a trade that only makes sense once I/O is cheap relative to CPU. Second, the broader "encoding extensibility" critique: Parquet supports a robust set of encodings ([[rle-dictionary]], [[delta-encodings]], [[byte-stream-split-encoding]]) but hasn't kept up with newer, more CPU-efficient schemes, and because keeping the Java, Python, C++, and Go implementations in sync is hard, extending Parquet's own encoding set moves slowly. That slow-moving extensibility is named directly as part of what motivated [[lance-file-format|Lance]], [[nimble-file-format|Nimble]], and [[vortex-file-format|Vortex]] to exist as separate formats rather than as Parquet patches.

*See also: [[parquet-random-access-limitation]] · [[lance-file-format]] · [[nimble-file-format]] · [[vortex-file-format]]*
