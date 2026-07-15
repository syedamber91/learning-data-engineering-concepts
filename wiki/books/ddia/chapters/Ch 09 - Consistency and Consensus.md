---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
type: chapter-moc
tags: [ddia, chapter-moc, consistency, consensus]
sources:
  - raw/ch09.md
---
# Ch 09 – Consistency and Consensus

The constructive answer to Chapter 8's pessimism: instead of engineering around every fault, build general-purpose abstractions with useful guarantees and let applications rely on them — the distributed analogue of what transactions did for crashes and concurrency. The chapter climbs a ladder of guarantees. [[Linearizability]] makes replicated data behave like a single copy touched atomically — the strongest, simplest model, but provably slow (latency proportional to network delay uncertainty) and unavailable under partitions (the honest reading of the [[CAP Theorem]]). [[Causality]] offers a cheaper middle path: a partial order of cause and effect, capturable with [[Lamport Timestamps]] — yet even a causality-consistent total order can't enforce a uniqueness constraint, because you must know the order is *final*. That demand leads to [[Total Order Broadcast]], which turns out to be equivalent to [[Consensus]] itself — as are linearizable compare-and-set registers, atomic commit, locks, membership services, and uniqueness constraints. [[Two-Phase Commit]] solves atomic commit but blocks when its coordinator dies; genuinely fault-tolerant algorithms (Paxos, Raft, Zab, VSR) use epochs and overlapping quorums to keep deciding as long as a majority survives, and services like [[ZooKeeper]] and [[Etcd]] rent that machinery out. The book's hardest chapter, and its keystone: precision about which guarantee is which — linearizability is not serializability, total order is not causal order, 2PC is not fault-tolerant consensus — is the whole game.

## Map
- [[Consistency Guarantees]]
- [[Linearizability]]
  - [[What Makes a System Linearizable]]
  - [[Relying on Linearizability]]
  - [[Implementing Linearizable Systems]]
  - [[The Cost of Linearizability]]
- [[Ordering Guarantees]]
  - [[Ordering and Causality]]
  - [[Sequence Number Ordering]]
  - [[Total Order Broadcast]]
- [[Distributed Transactions and Consensus]]
  - [[Atomic Commit and Two-Phase Commit (2PC)]]
  - [[Distributed Transactions in Practice]]
  - [[Fault-Tolerant Consensus]]
  - [[Membership and Coordination Services]]

## Chapter Summary
Linearizability puts every operation on one totally ordered timeline against a seemingly single copy of the data — easy to reason about (a database as a single-threaded variable) but slow, especially over wide-area networks. Causality is the weaker alternative: an ordering of what-happened-before-what that permits concurrency, giving a branching-and-merging version history with far less coordination overhead and less sensitivity to network faults. But even perfect causal ordering can't decide *now* whether a concurrent node is claiming the same username — that requires consensus: an agreement that is universal and irrevocable. A striking family of problems is reducible to it — linearizable compare-and-set registers, atomic transaction commit, total order broadcast, locks and leases, membership/coordination services, and uniqueness constraints. All are trivial on one node, or with one node holding all decision power — which is exactly single-leader replication. The catch is what happens when that leader fails or becomes unreachable: wait (and block, possibly forever — the XA coordinator answer), fail over manually (consensus by human), or elect automatically — which needs a real consensus algorithm. Even the single-leader design only defers consensus to election time rather than escaping it. Fault-tolerant consensus exists and works; ZooKeeper-style services package it as outsourced coordination, failure detection, and membership. Not everything needs it — leaderless and multi-leader systems live with conflicting, branching histories instead — but where fault-tolerant agreement is required, use a proven system. This closes Part II's theory; Part III returns to building practical systems from heterogeneous pieces.

## Related
- [[Part II - Distributed Data]] — the book part this chapter concludes
- [[Home]] — vault index
- previous: [[Ch 08 - The Trouble with Distributed Systems]] — the fault model these algorithms survive
- next: [[Ch 10 - Batch Processing]] — Part III begins with derived data
- [[Serializable Snapshot Isolation (SSI)]] — serializability, the isolation guarantee not to confuse with linearizability
- [[Leaders and Followers]] — single-leader replication, consensus's everyday disguise
