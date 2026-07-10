---
persona: vutr
kind: concept
sources:
- raw/kafka/apache-kafka-consumer.md
- raw/kafka/apache-kafka-part-1-overview.md
- raw/kafka/if-youre-learning-kafka-this-article.md
last_updated: '2026-07-10'
qc: passed
slug: pull-based-consumption-and-offset-commit
topics:
- kafka
---

A common assumption about messaging systems is that the broker should push data to consumers — that was the norm when Kafka was built. Scribe (from Facebook) and Flume both followed a push-based model. LinkedIn's engineers went the other way: they found the pull model more suitable because a consumer can retrieve messages at the maximum rate it can afford, instead of being flooded by messages pushed faster than it can handle. Two concrete advantages fall out of this choice:

- **Catching up**: a consumer that falls behind can catch up at its own pace.
- **Batching**: consumers pull batches of messages when ready, enabling efficient data transfer (see [[message-batching-and-compression]]).

## How a pull actually works

Behind the scenes, the Consumer API is an infinite loop polling the broker for more data. It issues asynchronous pull requests, and each request carries the offset of the message from which consumption should begin. The broker uses that offset to seek to the right position and return the desired data.

Here is the detail people miss: there is no explicit message ID in Kafka. Each message is addressed by its logical offset, which avoids the overhead of maintaining index structures that map message IDs to actual message locations (see [[log-segments-and-offset-addressing]]). So after receiving a message, the consumer itself computes the offset of the *following* message — current message's offset plus current message's length — and uses that in the subsequent pull request. The client does the arithmetic; the broker just seeks.

A consumer always consumes a particular partition sequentially. That is not incidental — sequential reads are half of why Kafka's disk-based design performs (see [[page-cache-sequential-io-and-zero-copy]]). And because consumption is strictly ordered within a partition, acknowledging one offset carries an implication: if the consumer acknowledges a particular message offset, the broker infers the consumer has received all previous messages in that partition.

## Why offset commit exists at all

The broker and consumer must agree on what has been consumed, and neither naive design works:

- If the broker marks a message consumed right after *sending* it and the consumer crashes, the message is lost — no instance ever processes it.
- If the broker instead waits for the consumer's confirmation before marking it consumed, other instances can pre-consume the message when the designated consumer fails to send an acknowledgment.

Kafka's answer is the unusual one: the consumer does not keep track of which messages it has consumed. It uses the broker to track the consume position, and the process of updating that position between consumer and broker is called **offset commit**. The consumer sends a message saying it has successfully processed everything up to a certain point; the broker assumes all messages before that point are processed and records the confirmation in the internal topic `__consumer_offsets`.

## The commit knobs and their trade-offs

Kafka exposes the commit behavior through configuration rather than hiding it:

- **Automatic commit** (`enable.auto.commit=true`): the consumer commits offsets at regular intervals automatically. Least effort, least control over *when* a commit lands.
- **Manual commit** (`enable.auto.commit=false`): the consumer decides when commits occur, via one of two calls:
  - `commitSync()` — synchronous; it waits until the commit either succeeds or errors.
  - `commitAsync()` — asynchronous; it does not wait. Errors are passed to a callback, or simply ignored if no callback is provided.

That last clause is the trade-off in miniature: `commitAsync()` buys you throughput by not blocking, and the price is that a commit failure can vanish silently unless you wire up the callback.

## Where this connects

Pull-based consumption is per-consumer mechanics; scaling reads across a topic is the job of [[consumer-groups-and-partition-assignment]], where each partition is owned by exactly one consumer in a group. When membership changes and ownership moves, committed offsets are what let the new owner resume where the old one stopped — the machinery for that handoff is [[consumer-group-rebalancing]]. And on the sending side, the mirror-image reliability knob is the producer's `acks` setting ([[producer-send-path-and-acks]]): `acks` governs when a write counts as delivered, offset commit governs when a read counts as processed.
