---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
topic: Transmitting Event Streams
type: subtopic
tags: [ddia, message-brokers, pub-sub, backpressure]
sources:
  - raw/ch11.md
---
# Messaging Systems
> Publish/subscribe systems push events from producers to consumers, and differ mainly in how they handle overload and node failures.

## The Idea
Polling a database for new events wastes effort as polling frequency rises, so streaming setups prefer push-based notification. A messaging system lets many producers publish events to a topic and many consumers receive them. Two design questions separate all such systems: what happens when producers outpace consumers (drop, buffer, or apply [[Backpressure]]), and whether messages survive node crashes (durability via disk and [[Replication]], at a throughput cost).

## How It Works
- **Direct messaging**: producer talks straight to consumer — UDP multicast for low-latency finance feeds, brokerless libraries like ZeroMQ, StatsD-style metrics over UDP, or webhooks (HTTP callbacks). Fast, but both sides must stay online and the application must cope with loss.
- **Message brokers**: a broker (RabbitMQ, ActiveMQ, HornetQ, Qpid, TIBCO EMS, IBM MQ, Azure Service Bus, Google Cloud Pub/Sub — the JMS/AMQP tradition) acts as a specialized database for messages. Clients come and go; durability becomes the broker's problem. Delivery is asynchronous: the producer gets an ack when the broker buffers the message, not when a consumer processes it.
- **Broker vs database**: the query models are inverted. A database query hands back a snapshot as of that moment — if the data changes a second later, nothing tells you unless you poll again. A broker can't answer arbitrary queries over its contents, but it *pushes* a notification the moment new data arrives. The broker's counterpart to picking out a subset of data via a query or [[Secondary Indexes]] is subscribing to topics matching a pattern — you choose your slice by topic, not by predicate.
- **Two consumer patterns**: *load balancing* hands each message to one member of a group (parallelize expensive processing); *fan-out* delivers every message to every subscriber, like multiple batch jobs reading one file. Groups can combine both.
- **Acknowledgments & redelivery**: a consumer must explicitly ack; if the connection drops first, the broker redelivers to someone else. A lost ack after successful processing means duplicate work unless you have atomic commit — see [[Atomic Commit and Two-Phase Commit (2PC)]].

## Trade-offs & Pitfalls
Load balancing plus redelivery reorders messages: if one consumer crashes mid-message, its message is redelivered after later ones were processed. That's harmless for independent messages, dangerous when there is [[Causality]] between them. Brokers delete acked messages, so a new consumer only sees the future — receiving is destructive, and you can't rerun a consumer for the same result. Long queues degrade throughput once messages spill to disk.

## Examples & Systems
ZeroMQ/nanomsg (brokerless), StatsD/Brubeck (UDP metrics), webhooks; JMS/AMQP brokers: RabbitMQ, ActiveMQ, IBM MQ, Azure Service Bus, Google Cloud Pub/Sub. Contrast with the log approach of [[Apache Kafka]].

## Related
- up: [[Transmitting Event Streams]] · chapter: [[Ch 11 - Stream Processing]]
- [[Partitioned Logs]] — the durable alternative to transient brokers
- [[Message-Passing Dataflow]] — Ch 4 view of message-based communication
- [[Two-Phase Commit]] — brokers can join distributed transactions
- [[Fault Tolerance]] — redelivery duplicates motivate exactly-once techniques
