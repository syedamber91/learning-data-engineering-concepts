---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
topic: Rebalancing Partitions
type: subtopic
tags: [ddia, rebalancing, operations, cascading-failure]
sources:
  - raw/ch06.md
---
# Operations: Automatic or Manual Rebalancing
> Rebalancing sits on a gradient from fully automatic to fully manual — and pairing full automation with automatic failure detection is a recipe for cascading failure.

## The Idea
Someone has to decide *when* partitions move. At one extreme the system rebalances itself with zero operator involvement; at the other, an administrator explicitly assigns partitions to nodes and nothing moves until they say so. Real systems sit at points along this gradient, and the choice is fundamentally about operational risk, not algorithms.

## How It Works
- **Middle ground in practice:** Couchbase, Riak, and Voldemort compute a suggested partition assignment automatically but hold it until an administrator commits it — automation proposes, a human disposes.
- **Fully automatic:** convenient, less routine maintenance work, but unpredictable, because rebalancing is inherently heavyweight — it reroutes requests and ships large volumes of data across the network, and done carelessly it degrades every other request in flight.

## Trade-offs & Pitfalls
The headline danger is automation compounding automation. Suppose a node is merely overloaded and slow to answer. Automatic failure detection declares it dead; automatic rebalancing then starts migrating its load — piling transfer traffic onto the already-struggling node, its peers, and the network. The "cure" deepens the overload and can snowball into a cluster-wide cascading failure. (This misdiagnosis pattern — slow ≠ dead — recurs throughout [[Unreliable Networks]] and [[Detecting Faults]].)

Keeping a human in the loop trades speed for safety: slower to converge than full automation, but far less likely to produce an operational surprise. This echoes Chapter 1's argument in [[Operability - Making Life Easy for Operations]] that good systems give operators visibility and control rather than opaque autonomy.

## Examples & Systems
Couchbase, Riak, and Voldemort exemplify propose-then-confirm rebalancing. Couchbase's overall design is simplified precisely because it doesn't rebalance automatically (its `moxi` routing tier just learns changes from the cluster — see [[Request Routing]]).

## Related
- up: [[Rebalancing Partitions]] · chapter: [[Ch 06 - Partitioning]]
- [[Strategies for Rebalancing]] — the mechanics being triggered automatically or manually
- [[Detecting Faults]] — why "node seems dead" is an unreliable signal
- [[Operability - Making Life Easy for Operations]] — the operations philosophy behind human-in-the-loop
