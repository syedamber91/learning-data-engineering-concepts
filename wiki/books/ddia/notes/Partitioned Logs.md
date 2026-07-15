---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
topic: Transmitting Event Streams
type: subtopic
tags: [ddia, kafka, log-broker, offsets]
sources:
  - raw/ch11.md
---
# Partitioned Logs
> A log-based message broker stores messages as an append-only, partitioned log on disk, marrying database durability with low-latency notification.

## The Idea
Traditional brokers treat messages as transient — delivered, then deleted — so consuming is destructive and history is unrecoverable. Databases keep data until told otherwise. The [[Log-Based Message Broker]] is the hybrid: keep every message in a durable log, notify consumers as new entries arrive, and let anyone re-read the past. This restores the batch-processing virtue of repeatable, experiment-friendly input (see [[The Output of Batch Workflows]]).

## How It Works
Producers append to the end of a log; consumers read it sequentially and wait at the tail (like `tail -f`). For throughput beyond one disk, the log is split by [[Partitioning]] across machines; a *topic* is the set of partitions carrying one message type. Each partition assigns every message a monotonically increasing **offset**, giving a total order *within* a partition (none across partitions). Fan-out is trivial — reads don't delete. Load balancing assigns whole partitions to nodes in a consumer group, not individual messages. Progress tracking is just a per-consumer offset (like the log sequence number a replication follower keeps — see [[Setting Up New Followers]]): the broker acts like a leader database, the consumer like a follower. On consumer failure, another node resumes from the last recorded offset (possibly reprocessing a few messages). Old segments are deleted or archived, making the log a large disk-backed circular buffer — a modern drive can buffer roughly 11 hours at full write speed, typically days-to-weeks in practice.

## Trade-offs & Pitfalls
Parallelism is capped by partition count, and one slow message blocks everything behind it in its partition (head-of-line blocking). So JMS/AMQP-style brokers win when messages are costly to process, ordering doesn't matter, and you want per-message parallelism; logs win for high throughput, cheap messages, and where ordering matters. A consumer that lags past the retention window silently loses messages — monitor lag and alert. Throughput stays constant regardless of retained history (everything hits disk anyway), unlike memory-first brokers that slow down when queues spill.

## Examples & Systems
[[Apache Kafka]], Amazon Kinesis Streams, Twitter DistributedLog; Google Cloud Pub/Sub is similar internally but exposes a JMS-style API. Offset rewinding enables replay for reprocessing — a key tool for [[Derived Data]] pipelines.

## Related
- up: [[Transmitting Event Streams]] · chapter: [[Ch 11 - Stream Processing]]
- [[Messaging Systems]] — the transient-broker model this improves on
- [[Implementation of Replication Logs]] — same leader/follower log mechanics
- [[Change Data Capture]] — log brokers transport database change events
- [[Log Compaction]] — keeps a full latest-value copy in bounded space
- [[kafka]] — the offset-addressed, partition-parallel log described here in the abstract is exactly what vutr's notes trace from LinkedIn's original 1GB-segment design through to tiered and diskless storage.
