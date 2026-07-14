---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 4
chapter_title: Encoding and Evolution
topic: Modes of Dataflow
type: subtopic
tags: [ddia, message-brokers, actor-model, async-messaging]
sources:
  - raw/ch04.md
---
# Message-Passing Dataflow
> Asynchronous messages via a broker sit between RPC and databases — low-latency delivery like RPC, an intermediary that stores data like a database — and encoding compatibility decides whether producers and consumers can deploy in any order.

## The Idea
The third mode of [[Dataflow]]. A sender publishes a *message* that reaches the recipient not directly but through a **message broker** (message queue / message-oriented middleware) that holds it temporarily. Communication is one-way and asynchronous: the sender fires and forgets rather than awaiting a reply (responses, if any, travel on a separate channel). This is RPC-like in latency ambitions and database-like in that a third party persists the bytes in between.

## How It Works
A producer sends to a named *queue* or *topic*; the broker delivers to one or more *consumers/subscribers*. Many producers and consumers can share a topic, consumers can republish to further topics (chaining into pipelines), or answer on a reply queue to simulate request/response. Advantages over direct RPC:
- buffers messages when the recipient is down or overloaded (reliability),
- redelivers to crashed processes (no lost messages),
- sender needn't know the recipient's address (vital when cloud VMs churn),
- one message can fan out to many recipients,
- sender and recipient are logically decoupled — publish without caring who consumes.

Brokers impose **no data model**: a message is bytes plus metadata, so any encoding works. If that encoding is backward *and* forward compatible, publishers and consumers can be changed independently and deployed in any order — the chapter's compatibility theme at its most liberating.

**Distributed actor frameworks** extend the single-process actor model (state-encapsulating actors exchanging async messages instead of sharing threads and locks) across nodes: the same message-passing semantics apply whether the peer is local or remote, with transparent encoding over the network. Location transparency actually works *better* here than in RPC because actors already assume messages can be lost even locally — the local/remote mismatch is smaller. Effectively an actor framework bundles a broker with the actor programming model.

## Trade-offs & Pitfalls
- A consumer that republishes must preserve unknown fields, or it reintroduces the data-loss round trip described in [[Dataflow Through Databases]].
- Rolling upgrades of actor systems still require message compatibility both ways: **Akka** defaults to Java serialization (no compatibility — swap in Protocol Buffers to enable rolling upgrades); **Orleans** defaults to a custom format that forces a new-cluster-and-cutover deployment unless you plug in custom serialization; **Erlang OTP** makes record-schema changes surprisingly painful despite its high-availability pedigree (the newer maps datatype may ease this).
- Delivery semantics vary by broker and configuration — don't assume guarantees.

## Examples & Systems
Commercial-era brokers (TIBCO, IBM WebSphere, webMethods); open-source RabbitMQ, ActiveMQ, HornetQ, NATS, and [[Apache Kafka]]; actor frameworks Akka, Orleans, Erlang OTP.

## Related
- up: [[Modes of Dataflow]] · chapter: [[Ch 04 - Encoding and Evolution]]
- [[Messaging Systems]] — Chapter 11's deep comparison of these brokers
- [[Partitioned Logs]] — Kafka's log-structured take on the broker
- [[Language-Specific Formats]] — why Akka's default serializer blocks upgrades
- [[Idempotence]] — deduplication concern shared with RPC retries
