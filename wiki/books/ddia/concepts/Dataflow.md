---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, architecture, derived-data]
sources:
  - raw/ch04.md
  - raw/ch10.md
  - raw/ch12.md
---
# Dataflow

The lens of "which process produces data that which process consumes" — following
how data moves and is transformed across a system rather than how any single
component works. Ch 4 classifies the channel types: [[Dataflow Through Databases]],
[[Dataflow Through Services - REST and RPC]], [[Message-Passing Dataflow]].

Ch 12 turns it into an architecture: [[Designing Applications Around Dataflow]] —
application state as a chain of derived transformations over event streams, with
"the log is the API." The unifying idea of Part III and of [[Derived Data]]
generally.

## Referenced In
- [[Batch and Stream Processing]]
- [[Beyond MapReduce]]
- [[Ch 04 - Encoding and Evolution]]
- [[Ch 10 - Batch Processing]]
- [[Ch 12 - The Future of Data Systems]]
- [[Dataflow Through Databases]]
- [[Dataflow Through Services - REST and RPC]]
- [[High-Level APIs and Languages]]
- [[Materialization of Intermediate State]]
- [[Message-Passing Dataflow]]
- [[Modes of Dataflow]]
- [[Processing Streams]]
- [[Trust, but Verify]]
- [[Unbundling Databases]]
