---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
type: chapter-moc
tags: [ddia, chapter-moc, stream-processing, event-streams]
sources:
  - raw/ch11.md
---
# Ch 11 – Stream Processing

Chapter 10's batch jobs assumed bounded input; real data arrives forever, and daily batches surface changes a day late. This chapter rebuilds the derived-data machinery for unbounded input processed continuously. It moves through three questions. How are event streams *transmitted*? — from direct messaging through AMQP/JMS brokers to the [[Log-Based Message Broker]], which marries database durability to low-latency notification and makes consumption replayable. How do streams relate to *databases*? — a [[Replication]] log is already an event stream, dual writes to multiple systems silently diverge, and [[Change Data Capture]] or [[Event Sourcing]] fix that by deriving every system from one ordered log, with immutable events as the system of record. And how are streams *processed*? — CEP, windowed analytics, [[Materialized Views]], and stream search, all forced to confront event time versus processing time, joins against changing state, and fault tolerance without a finish line. The chapter is where the book's "turn the database inside out" argument becomes concrete.

## Map
- [[Transmitting Event Streams]]
  - [[Messaging Systems]]
  - [[Partitioned Logs]]
- [[Databases and Streams]]
  - [[Keeping Systems in Sync]]
  - [[Change Data Capture]]
  - [[Event Sourcing]]
  - [[State, Streams, and Immutability]]
- [[Processing Streams]]
  - [[Uses of Stream Processing]]
  - [[Reasoning About Time]]
  - [[Stream Joins]]
  - [[Fault Tolerance]]

## Chapter Summary
Stream processing is batch processing done continuously on never-ending input, with brokers and event logs playing the filesystem's role. Two broker families divide the space: AMQP/JMS brokers assign and delete individual messages on acknowledgment — right for task-queue-style asynchronous RPC where ordering and replay don't matter — while log-based brokers assign whole partitions, preserve order, retain messages on disk, and track consumers by offset, echoing database replication logs and suiting [[Derived Data]] pipelines. Streams originate in user activity, sensors, and market feeds, but also in databases themselves: CDC captures the changelog implicitly, event sourcing declares it explicitly, and [[Log Compaction]] keeps a full latest-value copy in bounded space, so search indexes, caches, and analytics stores can be kept current — or rebuilt from scratch — by consuming one log. Processing purposes span pattern search (CEP), windowed aggregation (analytics), and view maintenance. Time is treacherous: processing time and event timestamps diverge, and windows declared complete still receive stragglers. Joins come in three shapes — stream-stream (windowed event matching), stream-table (enrichment against a CDC-maintained local copy), table-table (a materialized join view) — all state-keeping and order-sensitive. Finally, because an infinite job can't discard "the whole output" on failure, exactly-once effects come from finer tools: microbatching, checkpointing, framework-internal atomic commit, and idempotent writes.

## Related
- [[Part III - Derived Data]] — the book part this chapter advances
- [[Home]] — vault index
- previous: [[Ch 10 - Batch Processing]] — the bounded-input machinery generalized here
- next: [[Ch 12 - The Future of Data Systems]] — builds the unbundled-database vision on these logs
- [[Total Order Broadcast]] — the ordering principle beneath log-based derivation
- [[Implementation of Replication Logs]] — databases were streaming all along
