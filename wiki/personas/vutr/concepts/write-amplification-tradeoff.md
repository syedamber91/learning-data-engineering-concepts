---
persona: vutr
kind: concept
sources:
- raw/lsm-tree-storage-engines-additional/i-spent-the-weekend-learning-about.md
last_updated: '2026-07-15'
qc: passed
slug: write-amplification-tradeoff
topics:
- lsm-tree-storage-engines
---

Write amplification is Vu's central lens for comparing storage engines: how much extra physical I/O a small logical write triggers. A [[b-tree]] pays it on every random write — modifying 30 bytes still means rewriting a full 4KB/8KB page — while the LSM-tree avoids that by converting writes into sequential flushes of a sorted [[memtable]] (see [[sequential-vs-random-io]]), which is why it can sustain higher write throughput in most cases.

But the trade doesn't disappear inside the LSM-tree — it just moves into [[compaction]], and the two compaction strategies sit on opposite ends of the same amplification axis. Size-Tiered compaction only rewrites data when a tier is promoted, so it's the more write-optimized of the two, but it tolerates overlapping key ranges across SSTables in a tier, which pushes the cost onto reads — a lookup may have to check several overlapping SSTables to find the latest value (high read amplification). Leveled compaction keeps levels non-overlapping, which lowers read amplification (fewer files to check per key), but it's the more write-amplifying strategy: pulling a small amount of new data into a level forces a much larger volume of existing, unrelated data in that level to be rewritten just because its key range overlaps.

The upshot Vu draws is that there's no free win — a B-Tree buys predictable, low-latency reads at the cost of write amplification on every random write; an LSM-tree buys write throughput by deferring and batching that cost into background compaction, and then has to choose, via Size-Tiered versus Leveled, exactly where along the read/write amplification spectrum it wants to sit.

*See also: [[b-tree]] · [[compaction]] · [[sequential-vs-random-io]] · [[sstable]]*
