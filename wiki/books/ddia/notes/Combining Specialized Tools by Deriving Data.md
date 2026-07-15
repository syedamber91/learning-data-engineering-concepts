---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
topic: Data Integration
type: subtopic
tags: [ddia, derived-data, total-ordering, change-data-capture]
sources:
  - raw/ch12.md
---
# Combining Specialized Tools by Deriving Data

> Keep many specialized systems consistent by routing all writes through one ordered log and deriving every other representation from it.

## The Idea
A typical application pairs an OLTP database with a full-text search index, plus caches, warehouses, ML pipelines, and notification systems — because no one tool serves every access pattern. Kleppmann argues that dismissals like "99% of users never need X" reveal the speaker's limited vantage point: zoom out to organization-wide dataflow and integration needs appear everywhere. Once the same data lives in several places, the crucial questions become: where is data written first, and which representations derive from which? His thesis: designate a system of record, capture its changes in a defined order, and update everything else from that stream.

## How It Works
- **Ordered derivation**: writes go only to the system of record; [[Change Data Capture]] or an [[Event Sourcing]] log feeds every downstream view in the same order. This is state machine replication via [[Total Order Broadcast]]. Applying an event log deterministically and with [[Idempotence]] makes fault recovery straightforward.
- **Why not dual writes**: if the application writes directly to both database and index, concurrent clients can be applied in different orders by the two systems, leaving them permanently inconsistent — no one is "in charge" of ordering.
- **Versus distributed transactions**: [[Atomic Commit and Two-Phase Commit (2PC)]] orders writes with locks and gives [[Linearizability]] (hence read-your-writes), while log-based systems order with a log and rely on retry + idempotence. Kleppmann considers XA's fault tolerance and performance too poor, so absent a better widely adopted protocol, log-based derivation is the most promising integration approach — though users still deserve guidance beyond "accept [[Eventual Consistency]]".

## Trade-offs & Pitfalls
- Total ordering requires funneling events through a single leader; it breaks down when throughput exceeds one machine (partitioned logs have no cross-partition order), across geo-distributed datacenters (one leader each), across microservices with separate state, and with offline-capable clients.
- Ordering events is equivalent to [[Consensus]]; algorithms that scale ordering beyond a single node's throughput remain an open research problem.
- Subtle [[Causality]] violations persist: an "unfriend" event stored in one system and a message-send in another may be processed out of order, notifying the very person the sender excluded. Partial remedies — [[Lamport Timestamps]]-style logical ordering, logging the state a user saw and referencing that event ID, conflict-resolution algorithms — all have gaps, especially for external side effects.

## Examples & Systems
PostgreSQL's built-in full-text search (adequate for simple cases) versus dedicated retrieval tools; single-leader databases as proof that totally ordered logs work at moderate scale; the social-network unfriend/notification scenario as the causality cautionary tale.

## Related
- up: [[Data Integration]] · chapter: [[Ch 12 - The Future of Data Systems]]
- [[Keeping Systems in Sync]] — Ch 11 statement of the same problem
- [[Ordering and Causality]] — theory behind the causal-dependency pitfalls
- [[Partitioned Logs]] — why order is only per-partition at scale
- [[Multi-Leader Replication]] — the cross-datacenter case that defeats total order
