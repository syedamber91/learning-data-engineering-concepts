---
persona: vutr
kind: concept
sources:
- raw/kafka/deep-dive-into-the-challenges-of.md
last_updated: '2026-07-15'
qc: passed
slug: automq-object-batching-and-compaction
topics:
- kafka
---

The problem starts with a price tag. S3 Standard PUT requests cost $0.005 per 1,000 requests — sounds trivial until a service doing 10,000 writes per second is doing the math: that rate would cost $130,000 a month if every incoming message triggered its own object-storage write. So every vendor building Kafka on object storage tells its brokers to batch: buffer messages in memory for a while, or until they reach a target size, then upload once. The dial is explicit and painful in both directions — shorten the buffer and latency drops, but PUT costs climb; lengthen it and the reverse happens.

Batching across many partitions at once, though, creates a bookkeeping problem: what does a given uploaded object actually contain? AutoMQ's compaction process can generate two kinds of object. A **Stream Object (SO)** holds consecutive data segments from a single partition — this happens when one partition alone produces enough data to fill the batch size. A **Stream Set Object (SSO)** holds consecutive segments from several different partitions, combined together because none of them individually reached the batch threshold. Which one gets written is a runtime decision, not a design choice: if a single stream's data fills the batch, it goes out as an SO; if it takes several partitions' worth of data pooled together to hit that size, it goes out as an SSO.

The SSO path solves the cost problem but creates a new one: a partition's data can end up scattered across many small SSOs, interleaved with other partitions' data. That fragmentation directly hurts read performance, because reading that partition back now means issuing more requests against more objects instead of a few sequential reads against one. AutoMQ's answer is a background compaction process that runs asynchronously, consolidating a partition's scattered segments onto the smallest possible number of objects. That's the same move a log-structured storage engine makes for the same reason: pay a write-side cost later, in the background, to keep the read path cheap and sequential.

Compaction pays off twice. Beyond restoring read locality, fewer, larger objects mean fewer entries the system has to track — the total volume of metadata a diskless Kafka needs (which objects hold which topic's data, how message ordering is preserved across batches) scales with the number of objects in S3, so consolidating objects is also how AutoMQ keeps that metadata bounded.

*See also: [[automq-wal-shared-storage]] · [[automq-stream-abstraction-and-kafka-internals]] · [[diskless-kafka-trade-off-framework]]*
