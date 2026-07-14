---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
topic: Partitioning of Key-Value Data
type: subtopic
tags: [ddia, hot-spots, skew, celebrity-problem]
sources:
  - raw/ch06.md
---
# Skewed Workloads and Relieving Hot Spots
> Hashing spreads *different* keys evenly, but a single wildly popular key still lands on one partition — fixing that is (for now) the application's job.

## The Idea
Hash [[Partitioning]] evens out load across distinct keys, but it is powerless against traffic concentrated on *one* key: identical inputs hash identically, so every request for that key hits the same partition. The canonical case is the celebrity problem on social media — a user with millions of followers posts something, and a flood of writes converges on a single key (the celebrity's user ID, or the ID of the post everyone is reacting to). One historical data point: Twitter once reportedly dedicated a noticeable slice of its servers to Justin Bieber traffic. This is exactly the [[Hot Spots]] scenario partitioning was meant to prevent.

## How It Works
The standard mitigation is key splitting, done in application code:
- Append (or prepend) a small random number to the hot key. A two-digit decimal suffix fans one key out into 100 distinct keys, whose hashes then scatter across partitions, dividing the write storm 100 ways.
- Reads must then reverse the trick: fetch all 100 sub-keys and merge the results.
- Because that read amplification is pure overhead for ordinary keys, you split *only* the known-hot keys — which means extra bookkeeping to track which keys are currently split.

## Trade-offs & Pitfalls
- Write relief is bought with read cost: every read of a split key becomes a 100-way fan-out plus a combine step.
- The split set must be managed: deciding which keys are hot, when to split them, and when to un-split them is manual, application-specific machinery.
- As of the book's writing, no mainstream data system detects and compensates for single-key skew automatically — Kleppmann flags automatic skew handling as a plausible future capability, but today the trade-off analysis is yours.

## Examples & Systems
No named system solves this out of the box; the technique lives in application code atop stores like Cassandra, MongoDB, or Riak. The social-media celebrity write storm is the motivating real-world example.

## Related
- up: [[Partitioning of Key-Value Data]] · chapter: [[Ch 06 - Partitioning]]
- [[Partitioning by Hash of Key]] — why hashing alone can't help identical keys
- [[Partitioning by Key Range]] — the other scheme's own hot-spot story (timestamps)
- [[Describing Load]] — Chapter 1's fan-out framing of the same celebrity workload
