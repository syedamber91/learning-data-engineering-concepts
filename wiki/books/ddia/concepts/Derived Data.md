---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, architecture, derived-data]
sources:
  - raw/ch10.md
  - raw/ch11.md
  - raw/ch12.md
---
# Derived Data

Any data you could regenerate from another system's data: caches, indexes,
materialized views, ML model outputs. Opposed to the *system of record*, which
holds the authoritative first-written copy. The distinction is architectural gold:
derived data can be wrong or lost without catastrophe (rebuild it), can exist in
many query-optimized shapes, and clarifies dataflow direction.

Book home ground: the Part III intro ([[Part III - Derived Data]]) and everything
after — batch jobs producing indexes ([[The Output of Batch Workflows]]), streams
maintaining views ([[Databases and Streams]]), and the unbundled-database vision in
[[Ch 12 - The Future of Data Systems]].

## Referenced In
- [[Ch 10 - Batch Processing]]
- [[Ch 11 - Stream Processing]]
- [[Ch 12 - The Future of Data Systems]]
- [[Change Data Capture]]
- [[Home]]
- [[Data Integration]]
- [[Databases and Streams]]
- [[Designing Applications Around Dataflow]]
- [[Many-to-One and Many-to-Many Relationships]]
- [[Part III - Derived Data]]
- [[Partitioned Logs]]
- [[Unbundling Databases]]
