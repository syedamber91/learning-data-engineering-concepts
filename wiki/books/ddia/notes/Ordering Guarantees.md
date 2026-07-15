---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
type: topic
tags: [ddia, ordering, causality, total-order]
sources:
  - raw/ch09.md
---
# Ordering Guarantees
> Ordering is the deep thread connecting replication logs, serializability, and timestamps — and the distinction between causal (partial) order and total order explains what different consistency mechanisms can and cannot do.

Ordering has recurred throughout the book: the leader in single-leader [[Replication]] exists to fix the order of writes; [[Serializability]] makes transactions behave as if executed in *some* sequential order; timestamps try to order events in time. This topic makes the theme explicit. [[Causality]] defines a *partial* order (concurrent operations are incomparable, like branches in Git); [[Linearizability]] defines a *total* order (a single timeline, no concurrency). Sequence numbers — especially [[Lamport Timestamps]] — can compactly produce a causality-consistent total order, but knowing the order isn't enough for decisions like uniqueness: you must also know the order is *final*, which is what [[Total Order Broadcast]] provides. That requirement turns out to be equivalent to [[Consensus]].

## Subtopics
- [[Ordering and Causality]] — happened-before, partial vs total order, why linearizability implies causal consistency, and how causal dependencies are captured.
- [[Sequence Number Ordering]] — logical clocks, why naive per-node counters and physical timestamps break causality, and how Lamport timestamps fix it.
- [[Total Order Broadcast]] — reliable, same-order message delivery to all nodes; its equivalence with linearizable storage and consensus.

## Key Takeaways
- Causal order is partial: concurrent events are simply incomparable. Total order (linearizability) forces every pair to be ordered.
- Linearizability implies causal consistency — but causal consistency is the strongest model that stays fast and available under partitions.
- Lamport timestamps give a causality-consistent total order but cannot tell concurrency from dependency (that's what [[Version Vectors]] do).
- A total order you learn only *after the fact* cannot enforce constraints; finality of the order is the extra ingredient.
- Total order broadcast = a replicated append-only log = repeated rounds of consensus.

## Related
- chapter: [[Ch 09 - Consistency and Consensus]]
- [[Linearizability]] — the total-order end of the spectrum
- [[Detecting Concurrent Writes]] — happened-before in leaderless stores
- [[Distributed Transactions and Consensus]] — where finalizing the order leads
- [[Partitioned Logs]] — the log abstraction reappearing in stream processing
