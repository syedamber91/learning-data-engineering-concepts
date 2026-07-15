---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
topic: Databases and Streams
type: subtopic
tags: [ddia, cdc, replication-log, debezium]
sources:
  - raw/ch11.md
---
# Change Data Capture
> CDC extracts every write from a database as an ordered event stream so other systems can follow the database like replicas.

## The Idea
Replication logs were long treated as private internals — clients query the data model, not the log. That made it hard to mirror a database into a search index, cache, or warehouse. Change data capture (CDC) turns the write history into a public, consumable stream: the source database becomes the leader, and every derived system becomes a follower applying the same changes in the same order. This eliminates the races of dual writes (see [[Keeping Systems in Sync]]) and keeps [[Derived Data]] systems as faithful views of the system of record.

## How It Works
- **Extraction**: database triggers can append changes to a changelog table, but are fragile and slow; parsing the replication log (e.g. the MySQL binlog or PostgreSQL [[Write-Ahead Log]]) is more robust, though schema changes complicate it.
- **Transport**: a [[Log-Based Message Broker]] fits perfectly because it preserves ordering — no redelivery reordering.
- **Asynchrony**: the source commits without waiting for consumers, so a slow follower doesn't drag the database down, but all the usual lag anomalies apply (see [[Problems with Replication Lag]]).
- **Initial snapshot**: a truncated log can't rebuild full state (untouched rows never appear), so bootstrapping a new consumer needs a consistent snapshot tied to a known log offset, as with [[Setting Up New Followers]].
- **[[Log Compaction]]**: if every change carries a primary key and later values supersede earlier ones, the broker can keep only the newest record per key. A compacted topic then contains a complete latest-value copy of the database — a new consumer can start from offset 0 and skip the snapshot dance entirely. [[Apache Kafka]] supports this, making the broker viable as durable storage.

## Trade-offs & Pitfalls
CDC inherits [[Eventual Consistency]]: readers of derived views may not see their own recent writes. Trigger-based capture taxes the source database. Log parsing couples you to internal formats. Compaction only works when events are full-record overwrites, not deltas.

## Examples & Systems
LinkedIn Databus, Facebook Wormhole, Yahoo! Sherpa; Bottled Water (PostgreSQL), Maxwell and Debezium (MySQL binlog), Mongoriver (MongoDB oplog), Oracle GoldenGate. First-class change-stream APIs: RethinkDB, Firebase, CouchDB, Meteor, VoltDB stream export. Kafka Connect integrates CDC sources and sinks around Kafka.

## Related
- up: [[Databases and Streams]] · chapter: [[Ch 11 - Stream Processing]]
- [[Event Sourcing]] — same log idea at the application level
- [[Implementation of Replication Logs]] — the internal log CDC exposes
- [[State, Streams, and Immutability]] — why changelogs are foundational
- [[change-data-capture-cdc-and-data-sourcing]] — vutr's topic sorts the trigger-based and log-based extraction mechanisms this note describes onto a clean complexity/impact spectrum, and adds the DELETE-blindness failure mode of query-based CDC that this note doesn't cover.
- [[log-based-cdc]] — vutr's concept for the log-based approach specifically: reading the replication log directly for the lowest source impact but the highest coupling to internal formats, matching this note's binlog/WAL extraction method. Now grounded in Vu's own CDC deep-dive, including the WAL/redo-log/binlog naming and the Debezium-to-Kafka pipeline shape.
