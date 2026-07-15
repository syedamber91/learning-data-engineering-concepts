---
persona: vutr
kind: concept
sources:
- raw/apache-arrow-additional/apache-arrow-for-data-engineers.md
- raw/apache-arrow-additional/i-spent-6-hours-learning-apache-arrow.md
last_updated: '2026-07-15'
qc: passed
slug: simd-memory-alignment
topics:
- apache-arrow
---

Arrow's performance argument rests on two mechanisms that only work because the format is columnar (see [[arrow-columnar-array-layout]]): CPU cache efficiency and SIMD.

**Cache efficiency** comes directly from storing each column's values contiguously. When a workload processes one column, the CPU can pull contiguous blocks straight into cache, producing fewer cache misses and faster access. Vu contrasts this with row-oriented storage, where the system has to load an entire record into cache before it can extract the handful of columns a query actually needs — wasting cache space on data nobody asked for.

**SIMD** (Single Instruction, Multiple Data) is a CPU technique for applying the same operation to multiple values in one instruction. Arrow is built to take advantage of it, but SIMD only works on data that sits at predictable, aligned addresses — which is why Arrow enforces **memory alignment**: buffers should be allocated at addresses that are multiples of 8 or 64 bytes, and **padding** (extra, unused bytes appended after a data block) is used to make sure the total length is also a multiple of 8 or 64 bytes, so whatever comes next starts aligned too. Misaligned data forces the CPU into extra operations just to read it, which is the exact cost alignment is designed to avoid; padding buys that avoidance at the price of some wasted memory. Vu ties this specific alignment choice to Intel's performance guidelines, which recommend matching memory alignment to SIMD register widths — particularly for the AVX-512 instruction set. Neither post quantifies the actual speedup alignment or SIMD delivers on Arrow data; the mechanism is explained, the magnitude isn't measured.

Vu also notes, without elaborating, that columnar storage improves compression rates — a third performance lever alongside cache locality and SIMD that the source names but doesn't work through mechanically.

*See also: [[arrow-columnar-array-layout]] · [[apache-arrow]] · [[zero-copy-data-sharing]]*
