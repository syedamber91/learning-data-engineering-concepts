---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
topic: Ordering Guarantees
type: subtopic
tags: [ddia, causality, partial-order, causal-consistency]
sources:
  - raw/ch09.md
---
# Ordering and Causality
> Causality defines a *partial* order of events (cause before effect, concurrent events incomparable), while linearizability defines a *total* order — and linearizability implies causal consistency, but not the other way around.

## The Idea
Ordering matters chiefly because it preserves [[Causality]] — the guarantee that effects never appear before their causes. Violations have surfaced all over the book: an observer seeing an answer before the question it answers ([[Consistent Prefix Reads]]), a multi-leader replica receiving an update to a row that doesn't exist yet, the [[Detecting Concurrent Writes]] happened-before relation, a "consistent" snapshot meaning *consistent with causality* ([[Snapshot Isolation and Repeatable Read]]), the causal dependency behind [[Write Skew and Phantoms]] that [[Serializable Snapshot Isolation (SSI)]] tracks, and the football-score race from this chapter's opening. A system that respects the order causality imposes is **causally consistent**.

## How It Works
The crucial distinction is between two kinds of order:
- **Total order** — any two elements are comparable, like natural numbers. [[Linearizability]] gives this: a single copy of the data, one timeline, every pair of operations ordered. By definition there are no concurrent operations in a linearizable store.
- **Partial order** — some pairs are incomparable, like mathematical sets under "is a subset of". Causality is partial: two events are ordered if one happened before the other, but concurrent events (neither knew of the other) simply cannot be compared. The timeline branches and merges — Git's commit history, with its concurrent branches and merge commits, is exactly a causal dependency graph.

Linearizability is *strictly stronger* than causal consistency: any linearizable system automatically preserves causality, even across multiple communication channels, with no extra machinery. But the implication doesn't reverse — and causal consistency is the strongest consistency model that does **not** slow down under network delays and stays available under network failures (the [[CAP Theorem]] does not apply to it).

To enforce causal order without linearizability, a replica must know which operations happened before which: it may only process an operation once everything that causally precedes it has been processed. That requires tracking the "knowledge" of nodes — which version of the data an application had read when it issued a write (the fraud-investigation question: did the CEO know about X when deciding Y?). [[Version Vectors]] generalized across the whole database (not just one key) can carry this, and SSI's commit-time check of whether the data a transaction read is still current is the same idea in another guise.

## Trade-offs & Pitfalls
- Many systems that seem to need linearizability actually only need causal consistency, which is cheaper — but causally consistent databases are largely still research (with real challenges), not mainstream production systems.
- Tracking every causal dependency explicitly is expensive; this motivates the compact sequence-number approach of the next subtopic.
- Don't equate "totally ordered" with "causally meaningful": order and causality are different properties (a random-UUID order is total yet useless).

## Examples & Systems
Git version histories as a causal graph; the question-answer anomaly in replicated conversations; snapshot isolation's causally consistent snapshots.

## Related
- up: [[Ordering Guarantees]] · chapter: [[Ch 09 - Consistency and Consensus]]
- [[Sequence Number Ordering]] — compacting causality into timestamps
- [[The Cost of Linearizability]] — why the stronger model is expensive
- [[Detecting Concurrent Writes]] — happened-before applied per key in leaderless stores
- [[Problems with Replication Lag]] — where the causality anomalies first appeared
