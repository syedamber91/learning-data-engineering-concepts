---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
type: topic
tags: [ddia, consensus, atomic-commit, distributed-transactions]
sources:
  - raw/ch09.md
---
# Distributed Transactions and Consensus
> Getting several nodes to irrevocably agree on something — deceptively simple to state, subtle enough that decades of research (and many broken systems) went into solving it.

[[Consensus]] is the most fundamental problem in distributed computing: nodes propose values, and everyone must agree on one, irrevocably. It appears late in the book because appreciating it needs everything that came before — replication, transactions, system models, [[Linearizability]], and [[Total Order Broadcast]]. Two motivating faces of the problem: [[Leader Election]] (all nodes must agree who the leader is, or [[Split Brain]] corrupts data) and **atomic commit** (all nodes of a distributed transaction must agree to commit or all abort, preserving [[ACID]] atomicity). The famous FLP result proves consensus unsolvable — but only in the asynchronous model where algorithms may use no clocks, timeouts, or randomness; real systems escape it. The arc of this topic: [[Two-Phase Commit]] solves atomic commit but blocks on coordinator failure — a consensus algorithm, just not a good one; true fault-tolerant algorithms (Paxos, Raft, Zab, VSR) use epochs and overlapping quorums to make progress with a majority; and services like [[ZooKeeper]] package that machinery so applications can outsource it.

## Subtopics
- [[Atomic Commit and Two-Phase Commit (2PC)]] — the prepare/commit protocol, its system of promises, and why a crashed coordinator leaves participants stuck in doubt.
- [[Distributed Transactions in Practice]] — XA heterogeneous transactions, exactly-once message processing, and the operational pain of locks held by in-doubt transactions.
- [[Fault-Tolerant Consensus]] — the formal properties (agreement, integrity, validity, termination), epoch numbering and quorum overlap, and the limits of Raft/Paxos/Zab/VSR.
- [[Membership and Coordination Services]] — how ZooKeeper and etcd expose consensus as locks, leases, ephemeral nodes, watches, and service discovery.

## Key Takeaways
- Atomic commit and consensus are reducible to each other, but they differ in formalization: 2PC needs *every* participant's "yes", consensus needs only a majority — which is precisely why consensus tolerates faults and 2PC doesn't.
- A wide family of problems is equivalent to consensus: linearizable compare-and-set registers, total order broadcast, locks and leases, membership services, uniqueness constraints.
- FLP impossibility is about a maximally restrictive model; timeouts or randomness make consensus practically solvable.
- Single-leader replication doesn't dodge consensus — it defers it to leader election and failover ("kicks the can down the road").
- Epochs plus overlapping quorums break the "to elect a leader you need a leader" circularity.
- Use a proven system ([[ZooKeeper]], [[Etcd]]) rather than implementing consensus yourself; the track record of homegrown attempts is poor.

## Related
- chapter: [[Ch 09 - Consistency and Consensus]]
- [[Ordering Guarantees]] — total order broadcast, the equivalent problem this topic solves head-on
- [[Linearizability]] — buildable from consensus, and vice versa
- [[Knowledge, Truth, and Lies]] — the Ch 8 fault model consensus must survive
- [[Handling Node Outages]] — the failover problem consensus makes safe
