---
persona: vutr
kind: concept
sources:
- raw/apache-arrow-additional/apache-arrow-for-data-engineers.md
- raw/apache-arrow-additional/i-spent-6-hours-learning-apache-arrow.md
last_updated: '2026-07-15'
qc: passed
slug: zero-copy-data-sharing
topics:
- apache-arrow
---

Before Arrow, every system on a data path used its own internal memory format, so any time data crossed a boundary it had to be **serialized** (rewritten into a simpler shared representation) on the way out and **deserialized** (rewritten back into the receiving system's proprietary format) on the way in. Vu frames this cost as unavoidable under the old model and structures Arrow's interoperability pitch around three specific boundaries where that cost shows up, each with its own failure mode and its own Arrow-shaped fix. (He credits this three-scenario framing explicitly to Dunith Danushka's article on Arrow, which he used both as inspiration and to validate his own research.)

**Between two libraries in the same process.** When two libraries in one program work on the same data, one library's internal layout has to be converted into the other's before it can be used — meaning each library keeps its own copy, pays serialization/deserialization CPU cost, and in the worst case can't even convert safely if the two libraries' type systems are incompatible. If both libraries speak Arrow instead, there's nothing to convert: both already share the same in-memory layout, so the hand-off is just a pointer.

**Between two processes on the same machine.** Because operating systems isolate process memory, one process can only reach into another's memory through IPC (shared memory, message passing, pipes, or sockets). Without Arrow, the sending process still has to serialize into an intermediate format like JSON, ship it across the IPC channel, and have the receiver deserialize it into its own internal layout — the same CPU and memory-wastage costs as before, plus the added burden of implementing an IPC mechanism at all if neither side already has one. Arrow's answer is its own efficient IPC mechanism (see [[arrow-ipc]]): one process writes its data into an Arrow buffer in shared memory, and the other process reads directly from that region — no serialization, no deserialization, no copying.

**Between two processes on two different machines.** Now the data has to cross a network, and JSON is the typical choice because of how widely it's supported — but JSON is verbose and redundant (every record repeats its attribute keys), which eats bandwidth, and its type system is too thin to guarantee integrity when converting to and from richer formats. Arrow's answer here is Arrow Flight (see [[arrow-flight]]): a high-performance RPC framework that streams Record Batches over the wire in native, compressed Arrow format, so the receiver gets bytes already shaped the way it needs them, with the schema preserved and only the necessary columns transferred.

Across all three, the shape of the fix is the same: once every party already speaks the same in-memory format, the conversion step simply isn't needed, and what would have been a copy becomes a pointer or a stream of already-usable bytes. Vu's own gloss on why systems adopt Arrow ties directly back to this: Arrow supplies the performant columnar format ([[arrow-columnar-array-layout]], [[simd-memory-alignment]]) and the rich type system that make this kind of sharing safe, and "whatever reason a system chooses at first, whether interoperability or robustness, it will ultimately achieve both." Neither post details the boundary cases where a copy is still unavoidable even with Arrow on both sides.

*See also: [[arrow-ipc]] · [[arrow-flight]] · [[arrow-columnar-array-layout]] · [[apache-arrow]]*
