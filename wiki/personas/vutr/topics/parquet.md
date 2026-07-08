---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: parquet
---

Related: [[row-group]] · [[column-chunk]] · [[page]] · [[footer-filemetadata]] · [[rle-dictionary]] · [[rle-bit-packing-hybrid]] · [[delta-encodings]] · [[definition-repetition-levels]] · [[pax-hybrid-layout]] · [[predicate-pushdown]] · [[cpu-bound-lakehouse]]

## Comparisons
**Encoding choice is data-shape dependent.** [[rle-dictionary]] is the aggressive default for almost every column type, but it isn't always the best fit — [[delta-encodings]] like DELTA_BINARY_PACKED beat it on sorted timestamps or auto-incrementing keys, DELTA_BYTE_ARRAY wins on prefix-sharing strings, and BYTE_STREAM_SPLIT is aimed at FLOAT/DOUBLE. Note also that [[rle-dictionary]] falls back to another encoding once the dictionary exceeds a size threshold (~1MB), so it's not unconditional.

**Row group sizing is a parallelism-vs-overhead trade-off.** A smaller [[row-group]] gives better parallelism but more metadata overhead; a larger one reduces I/O overhead at the cost of coarser parallelism (recommended 128MB-1GB, or 100K-1M rows per DuckDB).

**Compression codecs trade ratio for speed.** Snappy is fast with a moderate ratio, Gzip gives a higher ratio but is slower, and ZSTD lands as the excellent balance between the two. But under [[cpu-bound-lakehouse]] conditions, the sharper question is whether to apply general-purpose compression at all.

**Purely columnar vs hybrid.** Everyone knows Parquet's columnar layout, but the [[pax-hybrid-layout]] framing is more precise: it's row-group-first, then columnar within — not purely columnar.

## Open questions
- If the CPU, not I/O, is now the bottleneck in the [[cpu-bound-lakehouse]] paradigm, should we skip general-purpose compression entirely — and for which workloads does that actually pay off?
- Parquet is not optimized for random access and AI workloads expose this; what should the format (or its successor) change to serve those access patterns?
- When does the [[rle-dictionary]] size threshold (e.g. 1MB) get hit in practice, and which fallback encoding does the writer choose?
- Given the [[delta-encodings]] and codec options, how much of the '5x slower jobs' from wrong row group size or poor partitioning could be recovered by tuning encoding alone?

## Synthesis
Parquet's real story is the [[pax-hybrid-layout]]: it partitions horizontally into [[row-group]]s, then columnar into [[column-chunk]]s, down to the [[page]] where [[rle-dictionary]] and other encodings do the physical work most people never inspect. The [[column-chunk]] min/max statistics in the [[footer-filemetadata]] are what make [[predicate-pushdown]] possible, and much of a pipeline's speed comes from getting row group size and encoding right rather than from the code. But the ground has shifted: under the [[cpu-bound-lakehouse]] paradigm, I/O is cheap and the CPU is the constraint, which is why Parquet's compression defaults and its weak random access are now being questioned.
