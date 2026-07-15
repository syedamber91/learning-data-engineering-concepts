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

## Related in the other wiki
- [[schema-change-severity-and-detection]] — vutr's concept ranks schema changes by severity (additive/rename-drop/type-change/semantic-change) for the pipeline-consumer side of exactly the same problem this page frames as backward/forward code-data compatibility, and names concrete defenses (schema registry, selective reads, ingestion-time validation) a data engineer applies when they don't control the producer's schema decisions.
- [[safe-writes-and-schema-evolution-in-serving]] — vutr's concept names five concrete serving-layer strategies for this exact problem (native table-format evolution in Delta/Iceberg/Hudi, additive-only-nullable-columns, versioned tables/snapshots, schema registries for streaming, and CI-time schema-change tests), giving this page's abstract backward/forward compatibility framing a serving-layer-specific menu of mechanisms.
