---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, encoding, compatibility]
sources:
  - raw/ch02.md
  - raw/ch04.md
---
# Schema Evolution

Changing your data's schema while old and new code and old and new data coexist.
The two directions of compatibility: backward (new code reads old data) and forward
(old code reads new data — the harder, often forgotten one, needed for rolling
upgrades). Formats differ in mechanism: field tags in [[Thrift and Protocol Buffers]], writer's/reader's schema resolution in [[Avro]].

Book home ground: all of [[Ch 04 - Encoding and Evolution]], especially
[[The Merits of Schemas]]; resurfaces wherever data outlives code — archived
storage, [[Dataflow Through Databases]], service APIs, event logs.

## Referenced In
- [[Avro]]
- [[Batch and Stream Processing]]
- [[Ch 02 - Data Models and Query Languages]]
- [[Ch 04 - Encoding and Evolution]]
- [[Dataflow Through Databases]]
- [[Evolvability - Making Change Easy]]
- [[Formats for Encoding Data]]
- [[Language-Specific Formats]]
- [[Part I - Foundations of Data Systems]]
- [[Relational Versus Document Databases Today]]
- [[The Birth of NoSQL]]
- [[The Merits of Schemas]]
- [[The Output of Batch Workflows]]
- [[Thrift and Protocol Buffers]]
