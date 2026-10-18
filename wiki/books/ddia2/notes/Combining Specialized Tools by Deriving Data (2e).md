---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
topic: Data Integration
type: subtopic
tags: [ddia2, dataflow, total-order-broadcast, causality, derived-data]
sources:
  - raw/ch13.md
---
# Combining Specialized Tools by Deriving Data
> Funnel all input through one system that decides an order, and every other representation becomes a deterministic derivation. That works — until the system outgrows a single ordering node.

## The Idea
**A common example: integrating an OLTP database with a full-text search index to handle arbitrary keyword queries.** **Some databases include full-text indexing, sufficient for simple applications, but more sophisticated search requires specialist information-retrieval tools** — **and conversely, search indexes are generally not very suitable as a durable system of record.** **So many applications need both.**

**As the number of representations increases, integration gets harder.** Besides the database and index you may need **copies in analytical systems, caches or denormalized versions, machine learning/classification/ranking/recommendation systems, and notification systems.**

## How It Works
**Reasoning about dataflows.** **When copies of the same data live in several systems, you need to be very clear about inputs and outputs. Where is data written first, and which representations are derived from which sources?**

**Arrange for data to be written first to a system-of-record database, then capture the changes and apply them to the search index in the same order.** **If CDC is the only way of updating the index, you can be confident the index is entirely derived from the system of record and therefore consistent with it** (barring bugs). **Writing to the database is the only way of supplying new input.**

**Allowing the application to write directly to both introduces the dual-writes problem**: **neither system is "in charge" of determining the order of writes, so they may make contradictory decisions and become permanently inconsistent.**

**If you can funnel all user input through a single system that decides an ordering for all writes, it becomes much easier to derive other representations by processing the writes in the same order** — **an application of state machine replication.** **Whether you use CDC or an event sourcing log is less important than the principle of deciding on a total order.** **And updating a derived system based on an event log can often be made deterministic and idempotent, making it quite easy to recover from faults.**

**Derived data versus distributed transactions.** **The classic approach to keeping systems consistent is distributed transactions. How does derived data compare?** **At an abstract level they achieve a similar goal by different means: distributed transactions use an atomic commit protocol to ensure changes are applied atomically, while log-based systems achieve correctness through deterministic retry and idempotence.**

**The biggest difference: transaction systems usually guarantee you can immediately read the up-to-date value after writing, whereas derived data systems are often updated asynchronously and so don't by default guarantee up-to-date reads.**

**Distributed transactions have been used successfully where their performance and operational costs are acceptable.** **But XA has poor fault tolerance and performance characteristics, severely limiting its usefulness.** **It might be possible to create a better protocol, but getting it widely adopted and integrated with existing tools would be challenging and is unlikely to happen soon.**

**In the absence of a good, widely supported distributed transaction protocol, log-based derived data is the most promising approach for integrating different data systems.** **But guarantees such as reading your own writes are useful, and it is not productive to tell everyone "eventual consistency is inevitable — suck it up and learn to deal with it"** (at least not without good guidance on how).

## Trade-offs & Pitfalls
**The limits of total ordering.** **With small enough systems, constructing a totally ordered event log is entirely feasible** — as the popularity of single-leader replication demonstrates. **But as systems scale, limitations emerge:**
- **Constructing a totally ordered log usually requires all events to pass through a single leader node.** **If throughput exceeds one machine, you must shard the log — and the order of events in two shards is then ambiguous.**
- **If servers are spread across geographically distributed regions**, you typically have a **separate leader per datacenter**, because **network delays make synchronous cross-datacenter coordination inefficient** — **implying an undefined ordering of events originating in different datacenters.**
- **With microservices, a common design choice is each service and its durable state as an independent unit with no shared durable state.** **When two events originate in different services, they have no defined order.**
- **Applications maintaining client-side state updated immediately on user input, and continuing to work offline, mean clients and servers are very likely to see events in different orders.**

**Formally, deciding a total order is total order broadcast, equivalent to consensus.** **Most consensus algorithms are designed for situations where a single node's throughput suffices for the entire event stream, and they provide no mechanism for multiple nodes to share the work of ordering.**

**Ordering events to capture causality.** **If no causal link exists, lack of total order is not a big problem — concurrent events can be ordered arbitrarily.** **Some cases are easy: multiple updates of the same object can be totally ordered by routing all updates for an object ID to the same log shard.** **But causal dependencies sometimes arise more subtly.**

**The book's example:** **a social network, two users who were in a relationship and have just broken up.** **One removes the other as a friend, then sends a message to their remaining friends complaining about their ex-partner.** **The intention is that the ex-partner should not see the rude message, since it was sent after the friend status was revoked.** **But in a system storing friendship status in one place and messages in another, that ordering dependency may be lost** — **and a notification service may process the message-send event before the unfriend event and incorrectly notify the ex-partner.**

**The notifications are effectively a join between the messages and the friend list**, making this related to the time-dependence of joins. **Unfortunately, this problem doesn't seem to have a simple answer. Starting points:**
- **Logical timestamps can provide total ordering without coordination**, so they may help when total order broadcast isn't feasible — **but they still require recipients to handle out-of-order events and additional metadata to be passed around.**
- **Log an event recording the state the user saw before making a decision, give it a unique identifier, and have later events reference that identifier to record the causal dependency.**
- **Conflict resolution algorithms help with events delivered in unexpected order.** **Useful for maintaining state, but they don't help if actions have external side effects such as sending a notification.**

**Perhaps patterns will emerge that allow causal dependencies to be captured efficiently, and derived state maintained correctly, without forcing all events through the bottleneck of total order broadcast.**

## Examples & Systems
OLTP database plus full-text search index as the canonical integration; the unfriend-then-complain scenario as the causality example.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Combining Specialized Tools by Deriving Data]] — the same dataflow-reasoning argument, the same derived-data-versus-distributed-transactions comparison, the same four limits of total ordering, and the same unfriend example with the same three partial answers. Another very stable section, since the open problem it names is still open.

## Related
- up: [[Data Integration (2e)]] · chapter: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[Keeping Systems in Sync (2e)]] — the dual-writes failure this avoids
- [[Logical Clocks (2e)]] — one of the three partial answers
- [[The Many Faces of Consensus (2e)]] — total order broadcast as consensus
- 1st edition: [[Combining Specialized Tools by Deriving Data]] — the same subtopic
