---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
type: chapter-moc
tags: [ddia, replication, moc]
sources:
  - raw/ch05.md
---
# Ch 05 – Replication

[[Replication]] keeps copies of the same data on multiple machines — for latency (data near users), availability (survive node or datacenter failure), and read throughput. Copying static data is trivial; the whole chapter is about handling *changes* to replicated data, through the three architectures nearly every distributed database picks from: single-leader, multi-leader, and leaderless. Along the way it confronts the sync/async trade-off, failover's sharp edges ([[Split Brain]], lost writes), the anomalies of replication lag and the session guarantees that tame them, write conflicts between leaders, [[Quorum]] arithmetic, and the happens-before machinery ([[Version Vectors]], siblings) for detecting concurrency. The dataset is assumed small enough for every node to hold in full — [[Ch 06 - Partitioning]] drops that assumption.

## Map

- [[Leaders and Followers]] — single-leader replication: all writes through one node, followers apply its change stream
  - [[Synchronous Versus Asynchronous Replication]] — durability guarantee vs. write availability; semi-synchronous compromise
  - [[Setting Up New Followers]] — consistent snapshot + log position, catch-up without downtime
  - [[Handling Node Outages]] — follower catch-up recovery; leader failover and everything it can break
  - [[Implementation of Replication Logs]] — statement-based, WAL shipping, logical (row-based), trigger-based
- [[Problems with Replication Lag]] — read-scaling on async followers invites anomalies; [[Eventual Consistency]] made precise
  - [[Reading Your Own Writes]] — read-after-write consistency, including the cross-device case
  - [[Monotonic Reads]] — never see time run backward across successive reads
  - [[Consistent Prefix Reads]] — causally ordered writes must be read in order
  - [[Solutions for Replication Lag]] — application workarounds vs. trusting transactions
- [[Multi-Leader Replication]] — several write-accepting leaders, each a follower of the others
  - [[Use Cases for Multi-Leader Replication]] — multi-datacenter, offline clients, collaborative editing
  - [[Handling Write Conflicts]] — avoidance, convergent resolution, custom handlers, CRDTs
  - [[Multi-Leader Replication Topologies]] — circular, star, all-to-all; loop prevention and causality violations
- [[Leaderless Replication]] — no write ordering at all; quorums, repair, and merged conflicts
  - [[Writing to the Database When a Node Is Down]] — quorum reads/writes, [[Read Repair]], [[Anti-Entropy]]
  - [[Limitations of Quorum Consistency]] — the edge cases behind `w + r > n`, and monitoring staleness
  - [[Sloppy Quorums and Hinted Handoff]] — write availability during partitions; multi-datacenter operation
  - [[Detecting Concurrent Writes]] — last-write-wins, happens-before, siblings, version vectors

## Chapter Summary

Replication serves high availability, disconnected operation, latency, and scalability — yet "keep a copy on several machines" turns out remarkably tricky once concurrency and faults enter. Three approaches: *single-leader* (all writes to one node that streams changes to followers — easy to reason about, no conflicts to resolve), *multi-leader* (several write-accepting nodes exchanging change streams — more robust to faulty nodes, network interruptions, and latency spikes, but harder to reason about and only weakly consistent), and *leaderless* (writes and reads fan out to several nodes in parallel, with staleness detected and corrected). Whether replication is synchronous or asynchronous profoundly shapes fault behavior: async is fast until a leader dies unrecovered, and then acknowledged writes may be gone. Replication lag produces real anomalies, matched by consistency models that name what applications need — *read-after-write* (see your own submissions), *monotonic reads* (no time travel backward), *consistent prefix* (causal order preserved, question before answer). Finally, multi-leader and leaderless designs must decide whether one write happened before another or the two are concurrent — and resolve genuine conflicts by merging. Next, the complementary axis of distribution: splitting big datasets into partitions.

## Related

- part: [[Part II - Distributed Data]] · home: [[Home]]
- previous: [[Ch 04 - Encoding and Evolution]] — encoded change streams are what replication logs ship
- next: [[Ch 06 - Partitioning]] — replication composes with splitting data across nodes
- [[Ch 08 - The Trouble with Distributed Systems]] — the fault model underneath failover and quorums
- [[Ch 09 - Consistency and Consensus]] — [[Consensus]], [[Linearizability]], and leader election done rigorously
