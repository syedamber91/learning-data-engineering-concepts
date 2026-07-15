---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, streams, messaging]
sources:
  - raw/ch11.md
---
# Log-Based Message Broker

A message broker built as a partitioned, append-only log on disk: producers append,
consumers read sequentially by offset. Unlike AMQP/JMS-style brokers that delete
messages after ack, the log retains history — consumers can lag, replay, or be added
later, and message order within a partition is guaranteed. Throughput comes from
sequential I/O and per-partition parallelism; offset tracking makes consumer state a
single number.

Book home ground: [[Partitioned Logs]] (Ch 11); exemplified by [[Apache Kafka]];
foundational for [[Change Data Capture]], [[Event Sourcing]], and
[[State, Streams, and Immutability]].

## Referenced In
- [[Batch and Stream Processing]]
- [[Ch 11 - Stream Processing]]
- [[Change Data Capture]]
- [[Distributed Transactions in Practice]]
- [[Event Sourcing]]
- [[Observing Derived State]]
- [[Part III - Derived Data]]
- [[Partitioned Logs]]
- [[Transmitting Event Streams]]

## Related in the other wiki
- [[kafka]] — this page's abstract "producers append, consumers read by offset" model is the general shape that vutr's topic shows one implementation (Kafka) building at LinkedIn, then partially abandoning again with Northguard's segment-level replication once the same company outgrew it.
