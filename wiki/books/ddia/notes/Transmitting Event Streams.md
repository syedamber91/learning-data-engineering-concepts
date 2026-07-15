---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
type: topic
tags: [ddia, event-streams, messaging, pub-sub]
sources:
  - raw/ch11.md
---
# Transmitting Event Streams

Batch jobs read and write files; streaming needs an equivalent transport. The unit is the *event* — a small, immutable, self-contained record of something that happened, usually carrying a time-of-day timestamp — produced once by a producer and consumed by any number of consumers, grouped into topics. A plain file or database could connect the two ends, but frequent polling wastes ever more requests on empty results as latency requirements tighten, so streaming systems push notifications instead. Two questions separate the design space: what happens when producers outrun consumers (drop, buffer, or apply [[Backpressure]]), and what is lost when a node crashes (durability via disk and [[Replication]] costs throughput). The chapter's answer evolves from direct producer→consumer messaging, through JMS/AMQP-style brokers, to the [[Log-Based Message Broker]] that treats a message stream as a durable, replayable log — recovering the repeatability that made batch processing safe to experiment with.

## Subtopics
- [[Messaging Systems]] — direct messaging (UDP multicast, ZeroMQ, webhooks) versus broker-based delivery; load balancing vs fan-out; acknowledgments, redelivery, and the ordering problems they cause.
- [[Partitioned Logs]] — brokers built on partitioned append-only logs ([[Apache Kafka]], Kinesis): offsets, consumer groups, disk-buffer retention math, and replaying old messages.

## Key Takeaways
- An event is the streaming analog of a record; producer/consumer/topic mirror writer/reader/filename.
- Drop, buffer, or backpressure — every messaging system must pick a stance for slow consumers, and durability under crashes is a separate, priced decision.
- AMQP/JMS brokers delete on acknowledgment, so consumption is destructive; combined load balancing + redelivery also reorders messages, which matters when events have causal dependencies ([[Causality]]).
- Log-based brokers make consumption a read-only cursor over a durable log: fan-out is free, ordering per partition is guaranteed, and old messages can be replayed for reprocessing.
- Choose JMS/AMQP style for expensive per-message work with no ordering needs; choose logs for high throughput, cheap messages, and order-sensitive processing.

## Related
- chapter: [[Ch 11 - Stream Processing]] · part: [[Part III - Derived Data]]
- [[Databases and Streams]] — the reverse move: applying streaming ideas to databases
- [[Processing Streams]] — what consumers actually do with the transported events
- [[Message-Passing Dataflow]] — Ch 4 first pass over message brokers as dataflow
- [[The Output of Batch Workflows]] — the batch repeatability that log-based messaging restores
