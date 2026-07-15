---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/file-formats-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: apache-avro
topics:
- parquet
---

Apache Avro is a row-oriented data serialization framework that originated in the Apache Hadoop ecosystem, with a language-independent schema definition. It supports a richer type set than JSON, including complex types like unions, enums, and maps, and is the dominant format for streaming data pipelines — particularly with Apache Kafka — thanks to its ability to evolve schema over time. Avro is also used for optimized write workloads, such as Hudi's log files.

The schema is defined in JSON, while the data itself is binary; Avro doesn't store field names in every record at all, just the values in the order the schema declares, which keeps the data compact. Schema evolution works through a writer's-schema / reader's-schema split: the writer encodes with whatever schema it was built against, the reader expects its own schema, and the two need not be identical — only compatible. When the reader reads, Avro resolves any conflict and translates the writer's-schema data into the reader's-schema shape.

Physically, an Avro data file is designed for parallel processing. A File Header at the start carries the schema, so any process reading the file knows the data's structure up front. Following the header is a series of Data Blocks, each compressed independently, each holding an object count, a size, and the objects themselves. Between blocks sit 16-byte Sync Markers — a randomly generated, file-unique byte sequence — which is what lets readers split the file for parallel processing: each worker can seek to sync-marker boundaries and take a set of blocks. The block size, object counts, and sync markers together also let Avro detect block corruption.

Avro's own disadvantage, stated plainly: being row-oriented, it is not suitable for analytics workloads — the same limitation that motivated [[pax-hybrid-layout|Parquet's]] column-oriented design.

*See also: [[pax-hybrid-layout]] · [[parquet-origin]] · [[parquet-physical-and-logical-types]]*
