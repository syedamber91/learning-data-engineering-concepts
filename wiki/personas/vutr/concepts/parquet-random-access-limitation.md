---
persona: vutr
kind: concept
sources:
- raw/parquet-file-format/its-time-to-replace-parquet.md
- raw/parquet-file-format/why-there-are-so-many-parquets-alternative.md
last_updated: '2026-07-15'
qc: passed
slug: parquet-random-access-limitation
topics:
- parquet
---

Parquet's [[column-chunk]] layout — the very thing that makes analytical scans cheap — is exactly what makes single-row lookups expensive. Rebuilding one logical row means reading from as many separate physical locations as there are columns, turning what a row-oriented format does in a single read into N separate reads that then have to be stitched back together. Compounding this, the [[page]] is the unit of both encoding and (by default) compression: reading even a single value inside a page requires fetching and decompressing the *entire* page, then decoding past whatever precedes the target value within it, before the value is reachable at all.

Why this matters now, per the sources, is squarely about AI workloads. Feature stores hold vector embeddings — arrays of hundreds of floats representing items, users, or documents — and a semantic-search system, after an index lookup returns candidate matches, must execute a burst of random-access reads against the underlying data store to retrieve the actual documents or features. If that store is Parquet, every one of those lookups pays the full page-decode cost described above. Vector-embedding columns are also exactly the "large column value" case that strains [[row-group|row-group sizing]] from the other direction — a 4KiB embedding value means far fewer rows fit in a row group of a given size than an 8-byte scalar would, which multiplies the number of row groups (and thus the metadata and non-sequential I/O) a file needs.

This single limitation is the throughline connecting Parquet's original design intent (large sequential analytical scans, built when I/O was the bottleneck — see [[cpu-bound-lakehouse]]) to the wave of AI-era successor formats, each of which answers it differently: [[lance-file-format|Lance]] splits its response by value size (tiny "miniblock" chunks for small values, "full-zip" transparently-compressed chunks for large ones like embeddings); [[nimble-file-format|Nimble]] doesn't try to solve it at all, explicitly optimizing for sequential decode instead; and [[vortex-file-format|Vortex]] leans on "transparent" encodings plus compute kernels that operate directly on compressed data, claiming a 100x random-access speedup over Parquet as a result.

*See also: [[page]] · [[row-group]] · [[lance-file-format]] · [[vortex-file-format]]*
