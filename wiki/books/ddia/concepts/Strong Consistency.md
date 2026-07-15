---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, consistency]
sources:
  - raw/glossary.md
---
# Strong Consistency

Umbrella term for guarantees that make a replicated system behave like a single
up-to-date copy of the data. The precise formal version is [[Linearizability]]:
every operation appears to take effect atomically at some instant between its start
and end, and once a read returns a value, later reads can't return older ones.
Costly: waiting for coordination makes operations slower and unavailable during
partitions (the [[CAP Theorem]] trade).

In the book: Ch 9's [[Linearizability]] topic (what it is, [[Relying on Linearizability]] for locks/uniqueness, [[Implementing Linearizable Systems]], and
[[The Cost of Linearizability]]).

## Referenced In
- [[Data Integration]]
- [[Linearizability]]
- [[Monotonic Reads]]
- [[Problems with Replication Lag]]
