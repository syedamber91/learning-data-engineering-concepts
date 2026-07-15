---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
topic: Ordering Guarantees
type: subtopic
tags: [ddia, lamport-timestamps, logical-clocks, total-order]
sources:
  - raw/ch09.md
---
# Sequence Number Ordering
> Logical clocks compress causality into compact, totally ordered sequence numbers — Lamport timestamps get this right where per-node counters and wall clocks fail — but even a causality-consistent total order can't enforce constraints, because it only becomes known after the fact.

## The Idea
Explicitly tracking every causal dependency is impractical: a client may read lots of data before writing, and recording all of it is heavy. A **logical clock** — an algorithm generating counter-based sequence numbers, unrelated to time-of-day — offers a shortcut: a few bytes per operation that yield a *total order consistent with [[Causality]]* (if A happened before B, A gets the smaller number; concurrent operations get an arbitrary but consistent order). Such an order carries all the causality information, plus extra ordering causality never demanded.

## How It Works
With single-leader replication this is trivial: the leader's replication log is a causality-consistent total order, produced by one incrementing counter ([[Leaders and Followers]]). Without a single leader, common generators all break causality:
- **Per-node counters** (one node issues odd, another even numbers): nodes process at different rates, so an even number says nothing about causal order relative to an odd one.
- **Physical timestamps**: [[Clock Skew]] can stamp a causally *later* operation with an *earlier* time (the known hazard of last-write-wins from [[Relying on Synchronized Clocks]]).
- **Preallocated blocks** (node A takes 1–1,000, node B takes 1,001–2,000): a causally later operation can land in a lower block.

**[[Lamport Timestamps]]** (Lamport, 1978) fix this with a pair *(counter, node ID)*: greater counter wins, ties broken by node ID. The causal magic is one rule — every node and client carries the maximum counter it has ever seen and attaches it to each request; a recipient seeing a bigger maximum jumps its own counter forward to match. Every causal dependency therefore forces the timestamp upward, making the total order consistent with causality. Crucially, this differs from [[Version Vectors]]: version vectors can *tell apart* concurrency from dependency, Lamport timestamps cannot — they just impose a total order (their advantage is compactness).

## Trade-offs & Pitfalls
- **Timestamp ordering is not sufficient for decisions made *now*.** For a uniqueness constraint (two users grabbing the same username), picking the lower timestamp works only *after* collecting all operations. A node fielding a request this instant can't know whether some other node is concurrently issuing a lower-timestamped claim — checking with every node would stall on any failure, the opposite of fault tolerance.
- The root problem: the total order only *emerges* once all operations are known; unknown operations may still need slotting in earlier. Enforcing constraints needs to know when the order is **final** — which is exactly [[Total Order Broadcast]].
- A total order that ignores causality (e.g., ordering random UUIDs lexicographically) is valid but useless.

## Examples & Systems
Odd/even node counters; timestamp-based last-write-wins; block allocators; Google Spanner's clock-uncertainty wait as the rare causally safe physical-clock scheme; Lamport's 1978 paper, among the most cited in distributed systems.

## Related
- up: [[Ordering Guarantees]] · chapter: [[Ch 09 - Consistency and Consensus]]
- [[Ordering and Causality]] — the partial order these numbers linearize
- [[Total Order Broadcast]] — adding the missing finality
- [[Detecting Concurrent Writes]] — where version vectors earn their keep
- [[Unreliable Clocks]] — why physical timestamps can't be trusted
