---
persona: vutr
kind: entity
sources:
- raw/flink-additional/i-spent-8-hours-understanding-which.md
last_updated: '2026-07-15'
qc: passed
slug: flink-memorysegments
topics:
- flink
---

Flink avoids storing data directly as plain Java objects — the same problem Spark's Tungsten project set out to solve, since (per the same Databricks source Vu cites) a 4-byte string can balloon to over 48 bytes once it becomes a JVM object. To sidestep that overhead, Flink's creators built a custom serialization/deserialization framework that controls the binary representation of data directly, which also lets operations like comparison or grouping run straight against the binary bytes instead of deserializing first — a significant performance win.

The fundamental unit this framework operates on is the **MemorySegment**: a fixed-size block, typically 32KB, that Flink data lives in whenever it's held in memory. Instead of allocating a new Java object per incoming record, Flink allocates a large pool of MemorySegments once, at TaskManager startup, and reuses them for the TaskManager's entire lifetime — they're only cleaned up when the TaskManager is torn down. That reuse is what cuts garbage-collection pressure on the JVM for what would otherwise be a very long-running process. The total memory reserved for the MemorySegment pool is configurable.

MemorySegments aren't only an in-memory-processing detail — the same 32KB unit is reused as Flink's default network buffer size for batching records before sending them to a receiving task (see [[flink-networking-and-flow-control]]), so the same allocation strategy that avoids per-record JVM objects during computation also avoids it during network exchange.

*See also: [[apache-flink]] · [[flink-networking-and-flow-control]] · [[flink-state-management-and-backends]]*
