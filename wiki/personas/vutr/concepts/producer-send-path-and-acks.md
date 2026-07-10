---
persona: vutr
kind: concept
sources:
- raw/kafka/apache-kafka-producer.md
- raw/kafka/if-youre-learning-kafka-this-article.md
- raw/kafka/doordashs-real-time-processing-system.md
last_updated: '2026-07-10'
qc: passed
slug: producer-send-path-and-acks
topics:
- kafka
---

A common assumption is that calling the producer API "sends a message to Kafka." It doesn't — not directly. What actually happens is a multi-stage pipeline inside the client, and understanding it is the difference between guessing at producer behavior and tuning it deliberately.

## The send path, step by step

When you use the Kafka producer API:

1. **You create a ProducerRecord.** It must include the message's value and the destination topic; it can optionally carry a key, partition, timestamp, and headers.
2. **The producer serializes** the record's key and value objects into byte arrays, because that's what goes over the network.
3. **If no partition was specified, the record goes to the partitioner**, which chooses the destination partition based on the key (see [[message-key-partitioning-strategies]] for how null keys, hashed keys, and the round-robin vs. sticky partitioners behave).
4. **The record is added to a batch** of messages headed to the same topic and partition. Kafka deliberately accumulates data in memory and sends larger batches in a single request — this avoids too many small requests and enables larger sequential disk operations on the broker. You control the batching behavior via the batch's limit size (`batch.size`) and the waiting time before the batch is sent (`linger.ms`). The batching and compression mechanics are covered in [[message-batching-and-compression]].
5. **A different thread sends the batches** to the appropriate brokers. The application thread never does the network send itself.
6. **The broker responds.** On success it returns a metadata object with the topic, partition, and record offset. On failure it returns an error, and the producer may retry a few times before giving up.

## Three ways to call send

Can you control how you send? Yes — and each option is a distinct failure-handling contract:

- **Fire-and-forget**: send and never check whether it arrived. On errors or timeout the message is simply lost and the application is never notified.
- **Synchronous**: send and wait for the response, so the producer can catch exceptions if Kafka returns an error or retries fail. Waiting on every message hurts performance, which is why synchronous send is rare in production.
- **Asynchronous**: send everything without waiting for replies — this takes almost no time — and attach a callback to handle errors.

## What "delivered successfully" actually means: `acks`

"The broker got it" is not one condition; the producer defines it via the `acks` parameter, which controls how many partition replicas must receive the record before the write counts as successful:

- **acks=0**: the producer doesn't wait for any reply and assumes success. Very high throughput, but if the broker never received the message, the producer won't know — the data disappears.
- **acks=1**: success as soon as the partition leader has the message. If the leader can't take the write, the producer gets an error and can retry, reducing loss risk — but a message can still be lost if the leader crashes before replicating it. The replica mechanics behind this are in [[leader-follower-replication]].
- **acks=all**: success only after all replicas receive the message. Safest — the message survives a broker crash — but latency rises because the producer waits for every replica-holding broker.

## The trade-offs in production: DoorDash

DoorDash's real-time platform shows how these knobs get set when throughput and availability outrank consistency. At their scale, having every service create a client, connect to bootstrap brokers, and retrieve topic-leader metadata added overhead, made producer configuration hard to unify, and left mobile/web apps unable to connect to Kafka directly — so they front Kafka with the Confluent Kafka REST Proxy, customized to produce to multiple clusters, send asynchronously without waiting for acknowledgment, pre-fetch topic metadata, and produce test records. On top of that they cut the replication factor from 3 (one leader, two followers) to 2, saving disk and replication CPU, and set `acks=1` so the producer gets its acknowledgment as soon as the leader has the message rather than waiting on followers. They also use the sticky partitioner to keep a batch's records on one partition until the batch fills. Combined, this tuning dropped Kafka broker CPU utilization by 30 to 40% — a concrete measure of what accepting weaker delivery guarantees buys you.
