---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, replication, distributed-systems]
sources:
  - raw/ch05.md
  - raw/ch08.md
---
# Quorum

Requiring acknowledgment from a minimum number of nodes before declaring an
operation done. With n replicas, writes to w nodes and reads from r nodes overlap
when w + r > n, so a read should see the latest acknowledged write. Majority quorums
(⌈n/2⌉+1) also make consensus safe: any two majorities share a node.

In the book: [[Limitations of Quorum Consistency]] shows the fine print — sloppy
quorums, concurrent writes, and partial failures mean quorum overlap alone doesn't
give [[Linearizability]]. Central to [[Leaderless Replication]] (Dynamo-style
systems) and to every [[Consensus]] algorithm's voting rounds.

## Referenced In
- [[Ch 05 - Replication]]
- [[Ch 08 - The Trouble with Distributed Systems]]
- [[Home]]
- [[Fault-Tolerant Consensus]]
- [[Knowledge, Truth, and Lies]]
- [[Leaderless Replication]]
- [[Limitations of Quorum Consistency]]
- [[Sloppy Quorums and Hinted Handoff]]
- [[The Truth Is Defined by the Majority]]
- [[Writing to the Database When a Node Is Down]]
