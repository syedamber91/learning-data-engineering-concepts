---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
topic: Linearizability
type: subtopic
tags: [ddia, cap-theorem, availability, latency]
sources:
  - raw/ch09.md
---
# The Cost of Linearizability
> Linearizability forces a choice between consistency and availability during partitions (CAP), and imposes a latency penalty all the time — which is why even CPU memory isn't linearizable.

## The Idea
If linearizability is so useful, why doesn't everything provide it? Two distinct costs: unavailability under network faults, and slowness even without them.

## How It Works
**The partition trade-off.** Picture a multi-datacenter deployment with the link between datacenters cut, clients still able to reach their local one. Multi-leader replication keeps working — writes queue and exchange later. Single-leader replication does not: clients in the follower datacenter cannot reach the leader, so they can make no writes and no linearizable reads. This is not an artifact of the implementation: *any* linearizable system, on any unreliable network, faces it. The dichotomy:
- Require linearizability → disconnected replicas must refuse requests (wait or error): consistent but unavailable.
- Drop linearizability → each replica can serve requests independently: available but not linearizable.

**The [[CAP Theorem]], properly understood.** Named by Eric Brewer (2000), though the trade-off was known in the 1970s. The pop formulation "pick 2 of 3" is misleading — partitions are a fault, not a menu option. Better: *Consistent OR Available when Partitioned*. When the network works you can have both. Kleppmann's critique goes further: the formal theorem is narrow (one consistency model — linearizability; one fault — partitions), says nothing about latency, dead nodes, or other trade-offs, and its idiosyncratic "availability" doesn't match what HA systems actually mean. Its historical credit is real — it pushed designers toward shared-nothing NoSQL designs — but it has been superseded by more precise results and is best avoided as a design tool. The chapter likewise warns off the CP/AP labeling.

**The everyday latency cost.** Even RAM on a multi-core CPU is not linearizable: per-core caches and store buffers mean one core's write isn't immediately visible to another without a memory barrier. That trade was made for *performance*, not fault tolerance — a CPU doesn't expect one core to soldier on while disconnected. Same story for many databases: they drop linearizability to be fast, not to survive partitions. And this is provably unavoidable: Attiya and Welch showed linearizable read/write response time is at least proportional to the network's delay *uncertainty*. No faster algorithm exists; weaker models (like causal consistency) can be much faster.

## Trade-offs & Pitfalls
- Don't cite CAP to justify non-linearizable designs inside one machine or one healthy network — the honest reason is usually latency.
- "Highly available" in marketing rarely means CAP-available.
- Chapter 12 explores keeping correctness without linearizability.

## Examples & Systems
Multi-core x86 memory models; multi-datacenter single-leader vs multi-leader deployments; the NoSQL design explosion CAP helped trigger.

## Related
- up: [[Linearizability]] · chapter: [[Ch 09 - Consistency and Consensus]]
- [[Multi-Leader Replication]] — the availability-first alternative
- [[Ordering and Causality]] — causal consistency dodges this cost
- [[Timeouts and Unbounded Delays]] — why delay uncertainty is high in practice
- [[The End-to-End Argument for Databases]] — Chapter 12's correctness-without-linearizability agenda
