---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Multi-Leader Replication
type: subtopic
tags: [ddia, replication-topology, causality, multi-leader]
sources:
  - raw/ch05.md
---
# Multi-Leader Replication Topologies

> The paths writes take between leaders — ring, star, or all-to-all — trade fault tolerance against ordering headaches.

## The Idea

With exactly two leaders there is only one option: each sends its writes to the other. Three or more leaders open up a design choice: along which communication paths do writes propagate? This *replication topology* determines both what happens when a node dies and whether writes can arrive out of order.

## How It Works

- **Circular** — each node receives changes from one neighbor and forwards them (plus its own) to the next. MySQL's default multi-leader support is limited to this shape.
- **Star** — one root node forwards writes to all others; generalizes to a tree.
- **All-to-all** — every leader sends its writes directly to every other leader; the most general topology.

In circular and star layouts a write passes through intermediate nodes, so nodes must forward changes they didn't originate. To stop infinite replication loops, each node has a unique identifier and every write is tagged in the log with the IDs of all nodes it has traversed; a node ignores any change already stamped with its own ID.

## Trade-offs & Pitfalls

- **Sparse topologies have single points of failure.** In a ring or star, one dead node severs the replication flow between others until someone (usually manually) reconfigures the paths around it. Densely connected all-to-all topologies route around failures.
- **All-to-all breaks [[Causality]].** Links differ in speed, so replication messages can overtake one another: leader 2 may receive an *update* to a row before the *insert* that created it. This mirrors the anomaly in [[Consistent Prefix Reads]]. Attaching timestamps doesn't fix it — [[Clock Skew]] means clocks can't be trusted to order events across nodes — but [[Version Vectors]] can order them correctly (see [[Detecting Concurrent Writes]]).
- **Implementations under-deliver.** At the time of writing, PostgreSQL BDR provided no causal ordering of writes, and Tungsten Replicator for MySQL didn't attempt conflict detection at all. If you run multi-leader replication, read the documentation skeptically and test that the guarantees you assume actually hold.

## Examples & Systems

- MySQL (circular by default, via native support or Tungsten Replicator), PostgreSQL BDR, Oracle GoldenGate.
- The loop-prevention trick of tagging writes with traversed node IDs is how these forwarding topologies stay finite (a broken version of it caused an infinite-loop bug in HBase master–master replication).

## Related

- up: [[Multi-Leader Replication]] · chapter: [[Ch 05 - Replication]]
- [[Detecting Concurrent Writes]] — version vectors, the fix for cross-leader ordering
- [[Consistent Prefix Reads]] — the same causality violation seen by readers
- [[Handling Write Conflicts]] — what happens once conflicting writes do meet
