---
persona: vutr
kind: concept
sources:
- raw/kafka/apache-kafka-important-designs.md
- raw/kafka/apache-kafka-producer.md
- raw/kafka/if-youre-learning-kafka-this-article.md
last_updated: '2026-07-10'
qc: passed
slug: message-batching-and-compression
topics:
- kafka
---

Batching in Kafka is usually explained as a network optimization, and that framing undersells it. The real starting point is a consequence of Kafka's storage decision: because Kafka uses the OS filesystem at the back (see [[page-cache-sequential-io-and-zero-copy]]), too many small requests from the client to the broker can harm performance. Batching attacks that problem at both ends of the wire — the network hop *and* the disk write behind it.

## The mechanism, end to end

**The protocol-level abstraction.** The Kafka protocol has a *message set* abstraction that groups messages together. Instead of paying a network round trip per message, the client sends one request carrying many messages, mitigating the round-trip overhead of firing too many single-message requests.

**Where batches form: inside the producer.** When you call the producer API, the record is serialized, routed to a partition, and then — this is the step that matters here — added to *the batch of messages headed to the same topic and partition*. The producer accumulates data in memory and sends larger batches in a single request. A different thread is responsible for shipping those batches to the appropriate brokers, so accumulation and sending are decoupled. The full path is in [[producer-send-path-and-acks]].

**The two knobs.** Batching behavior is controlled by two producer configs: the batch's limit size (`batch.size`) and the waiting time before sending the batch to the broker (`linger.ms`). The trade-off is implicit in the pair: cap by size and you bound memory per batch; cap by time and you bound how long a record sits waiting for the batch to fill.

**What the broker does with a batch.** Batching isn't only about fewer requests — it changes the shape of the disk write. Instead of appending messages one by one to the active segment file, the broker appends a chunk of messages at once. That gives Kafka larger sequential disk operations, which is exactly the access pattern its filesystem-backed storage is designed around (segments are appended-only files of roughly equal size, e.g. 1GB — see [[log-segments-and-offset-addressing]]).

**Compression rides on batches.** When network bandwidth — not the broker — is the bottleneck, Kafka supports compressing *batches* of messages with an efficient batching format: a batch of messages is grouped, compressed, and sent to the broker as a unit. Compressing at the batch level rather than per message is what makes the format efficient.

**Why the broker never re-compresses.** Here is the design detail that ties batching to Kafka's other optimizations: the data format on disk is kept the same throughout — from when the producer sends it to when the broker ships it to the consumer. Keeping one message format end to end lets Kafka use the zero-copy technique efficiently *and* avoid decompressing and recompressing messages. The broker doesn't unpack your compressed batch to inspect it; it appends it and later hands the same bytes to consumers via `sendfile()`.

**Batching on the read side too.** The benefit is symmetric. Kafka's pull-based consumption model (see [[pull-based-consumption-and-offset-commit]]) means consumers can pull batches of messages when they're ready, enabling efficient data transfer — one of the two advantages LinkedIn's engineers cited for choosing pull over the push model used by Scribe and Flume.

## The partitioner interaction people miss

Batches are per topic-partition, so the partitioning strategy directly affects how well batches fill. With the Round-Robin partitioner (Kafka ≤ v2.3), keyless messages are sprayed cyclically across partitions — one after another. The Sticky Partitioner (Kafka ≥ 2.4) instead tries to send as many records as possible to the *same* partition until a condition is met — such as the batch reaching its limit — and only then switches to another partition. Sticking to one partition per batch is a batching optimization dressed up as a partitioning change; the details are in [[message-key-partitioning-strategies]].

## The trade-off summary

Nothing here is free. Batching buys throughput (fewer round trips, larger sequential appends) at the cost of latency — a record can wait up to the configured linger time or until the batch fills before it even leaves the producer. Compression buys bandwidth when the network is the constraint. The sources are explicit about the ordering: compression is the lever you reach for *when network bandwidth is the bottleneck*, not a default posture.
