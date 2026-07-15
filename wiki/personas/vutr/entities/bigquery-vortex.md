---
persona: vutr
kind: entity
sources:
- raw/lsm-tree-storage-engines-additional/i-spent-the-weekend-learning-about.md
last_updated: '2026-07-15'
qc: passed
slug: bigquery-vortex
topics:
- lsm-tree-storage-engines
---

Vu names Google's Vortex (introduced 2024) as his lead example of the LSM pattern surfacing in OLAP: a storage engine built to support real-time analytics in BigQuery, organized as an LSM-tree of "Fragments." Its design bet, per Vu, is that it's better to build a storage system for streaming first and use it for batch afterward, rather than adapting batch-built infrastructure to handle streaming.

The LSM structure shows up as a two-format pipeline: an **Ingestion Format (Hot)**, where buffered in-memory data is written to a Write-Optimized-Storage (WOS) format built to accept high-velocity writes; and an **Analytical Format (Cold)**, where a background Storage Optimization Service asynchronously converts WOS data into Read-Optimized-Storage (ROS) — a highly compressed, columnar format. That hot-to-cold aging is the same Memtable-flush-then-compact shape as any other LSM-tree, just applied at the fragment level of an OLAP warehouse rather than inside a key-value store.

*See also: [[memtable]] · [[compaction]] · [[vortex-storage-engine]] — the fully grounded mechanics (Streams, Streamlets, Fragments, the Storage Optimization Service, control/data plane split) behind this entity's brief WOS/ROS sketch live under the [[bigquery-internals]] topic, from Vu's dedicated Vortex deep-dive posts.*
