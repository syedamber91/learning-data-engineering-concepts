---
persona: vutr
kind: entity
sources:
- raw/druid-pinot-real-time-olap/the-architecture-of-apache-druid.md
last_updated: '2026-07-15'
qc: passed
slug: druid-realtime-node
topics:
- apache-pinot-druid-and-real-time-olap
---

Druid's real-time nodes ingest and query event streams, making incoming events immediately available for querying. They inform Zookeeper of their state and the data they're responsible for. Functionally, a real-time node acts as a row store for events: it maintains an in-memory index buffer for all incoming events, built up incrementally as events arrive, and that index can be queried directly while it's still in memory.

**From memory to deep storage.** Because memory is limited, real-time nodes persist the in-memory index to disk in one of two ways: periodically, or once a maximum row threshold is hit. This persistence step also converts the data from row-storage format (in memory) to column-oriented storage (on disk), and once on disk the data is immutable. The node then schedules a background task that looks for all the locally persisted data on disk, merges these indexes, and builds a single immutable data block covering a specific time range — what the source calls a "segment." The real-time node later uploads this segment to remote deep storage, such as S3 or HDFS (see [[immutable-segment]] and [[druid-historical-node]] for what happens to it next).

**Kafka as the ingestion layer.** Real-time nodes typically consume from a message bus like Kafka: a producer sends data to a Kafka topic, and the real-time node reads from that topic. The source calls out two specific advantages of having Kafka as this middle layer:

- **Event buffer** — Kafka tracks offsets, telling the real-time node its current consumption position. The node updates this offset every time it persists its in-memory buffer to disk. If the disk survives a failure, the node can resume reading from the last committed offset rather than from scratch, which reduces recovery time.
- **Single data endpoint** — because every consumer reads from the same Kafka topic, Druid can run either redundant consumers (multiple real-time nodes ingesting the same set of events, so one node's failure doesn't lose data) or load-balanced consumers (each node ingests one stream partition, scaling ingestion throughput across nodes).

*See also: [[apache-druid]] · [[druid-historical-node]] · [[druid-broker]] · [[immutable-segment]]*
