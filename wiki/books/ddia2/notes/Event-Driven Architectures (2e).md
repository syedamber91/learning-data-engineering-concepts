---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 5
chapter_title: Encoding and Evolution
topic: Modes of Dataflow
type: subtopic
tags: [ddia2, message-broker, kafka, actors, asynchronous, pub-sub, schema-registry]
sources:
  - raw/ch05.md
---
# Event-Driven Architectures
> Send it and forget it. A broker in the middle buys you buffering, redelivery, fan-out, and decoupling — and costs you the synchronous answer.

## The Idea
Another way encoded data flows from process to process. Here a request is called an **event** or **message**. Unlike RPC, **the sender usually does not wait for the recipient to process the event**, and events are typically **not sent over a direct network connection** but via an intermediary called a **message broker** (also **event broker**, **message queue**, or **message-oriented middleware**), which stores the message temporarily.

## How It Works
Advantages of a broker over direct RPC:
- It can act as a **buffer if the recipient is unavailable or overloaded**, improving reliability.
- It can **automatically redeliver messages to a process that has crashed**, preventing loss.
- It **avoids the need for service discovery**, since senders don't connect to the recipient's IP address.
- It allows the **same message to be sent to several recipients**.
- It **logically decouples sender from recipient** — the sender publishes and doesn't care who consumes.

Communication is **asynchronous**: the sender doesn't wait for delivery, it sends and forgets. A synchronous RPC-like model can still be implemented by having the sender wait for a response **on a separate channel**.

**Message brokers.** The landscape was once dominated by commercial enterprise software from **TIBCO, IBM WebSphere, and webMethods**, before open source implementations — **RabbitMQ, ActiveMQ, HornetQ, NATS, Redpanda, Apache Kafka** — became popular. More recently cloud services such as **Amazon Kinesis, Azure Service Bus, and Google Cloud Pub/Sub** have gained adoption.

Delivery semantics vary by implementation and configuration, but two distribution patterns dominate:
- One process adds a message to a **named queue**, and a consumer receives it. **If there are multiple consumers, one of them receives the message.**
- One process publishes to a **named topic**, and the broker delivers to all subscribers. **If there are multiple subscribers, they all receive it.**

Brokers typically **don't enforce any particular data model** — a message is a sequence of bytes with some metadata, so any encoding works. A common approach is Protocol Buffers, Avro, or JSON with a **schema registry deployed alongside the broker** to store all valid schema versions and check their compatibility. **AsyncAPI**, a messaging equivalent of OpenAPI, can also specify message schemas.

**Distributed actor frameworks.** The **actor model** is a concurrency model for a single process: rather than dealing with threads and the attendant race conditions, locking, and deadlock, logic is encapsulated in **actors**, each typically representing one client or entity, with local state not shared with other actors, communicating by **asynchronous messages**. **Message delivery is not guaranteed** — in certain error scenarios messages are lost. Since each actor processes only one message at a time it needn't worry about threads, and each can be scheduled independently by the framework.

**Distributed actor frameworks** — **Akka, Orleans, Erlang/OTP** — use this model to scale across multiple nodes. The same message-passing mechanism is used whether sender and recipient are on the same node or different ones; across nodes, the message is transparently encoded to bytes, sent, and decoded.

## Trade-offs & Pitfalls
- **Durability varies.** Many brokers write messages to disk so they survive a broker crash or restart. **Unlike databases, many brokers automatically delete messages after they have been consumed** — though some can be configured to store messages indefinitely, which you would need for **event sourcing**.
- **If a consumer republishes messages to another topic, be careful to preserve unknown fields** — otherwise you hit exactly the silent data-loss problem from the start of the chapter.
- **Location transparency works better in the actor model than in RPC**, because the actor model **already assumes messages may be lost, even within a single process**. Latency over the network is likely higher than within a process, but there is **less of a fundamental mismatch** between local and remote communication.
- **A distributed actor framework essentially integrates a message broker and the actor programming model into one framework** — but if you want rolling upgrades of an actor-based application you still have to worry about forward and backward compatibility, since messages may travel from a node on the new version to one on the old and vice versa.

## Examples & Systems
RabbitMQ, ActiveMQ, HornetQ, NATS, Redpanda, Kafka; Kinesis, Azure Service Bus, Google Cloud Pub/Sub; Akka, Orleans, Erlang/OTP; AsyncAPI and schema registries.

## Since the 1st Edition
This is the 1st edition's [[Message-Passing Dataflow]], **renamed to Event-Driven Architectures** — a reframing that matches how the pattern is now discussed. The broker advantages, the queue-versus-topic distinction, and the actor-model material carry over. **New:** the modern broker roster (NATS, Redpanda, Kinesis, Azure Service Bus, Pub/Sub) alongside the legacy enterprise names; **schema registries and AsyncAPI** as the compatibility mechanism for messaging; the note that brokers can be configured for indefinite retention to support event sourcing; and the warning about preserving unknown fields when republishing.

## Related
- up: [[Modes of Dataflow (2e)]] · chapter: [[Ch 05 - Encoding and Evolution (2e)]]
- [[Transmitting Event Streams (2e)]] — brokers examined in depth in Chapter 12
- [[Event Sourcing and CQRS (2e)]] — why indefinite retention matters
- [[Log-Based Message Brokers (2e)]] — the Kafka-style variant
- 1st edition: [[Message-Passing Dataflow]] — the same subtopic under its old name
