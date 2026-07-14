---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
topic: Linearizability
type: subtopic
tags: [ddia, replication, quorums, dynamo-style]
sources:
  - raw/ch09.md
---
# Implementing Linearizable Systems
> Of the standard replication schemes, only consensus-based replication reliably delivers linearizability — even strict quorums can violate it.

## The Idea
Literally keeping one copy of the data would be trivially linearizable but not fault-tolerant. So the question becomes: which fault-tolerant [[Replication]] strategies from Chapter 5 can preserve the single-copy illusion?

## How It Works
Scorecard by replication method:
- **Single-leader — potentially linearizable.** Reads from the leader or synchronously-updated followers *can* be linearizable, but many implementations are not (snapshot isolation by design, or concurrency bugs). The Achilles heel: you must *know* who the leader is. A node that wrongly believes itself leader will serve stale or lost data; asynchronous failover can drop committed writes, violating durability and linearizability at once. (Partitioning by key doesn't hurt — linearizability is per-object.)
- **Consensus algorithms — linearizable.** They resemble single-leader replication but add machinery against [[Split Brain]] and stale replicas. This is how [[ZooKeeper]] and [[Etcd|etcd]] safely offer linearizable storage.
- **Multi-leader — not linearizable.** Concurrent writes on multiple nodes with async replication produce conflicting versions — the opposite of a single copy.
- **Leaderless (Dynamo-style) — probably not.** The folk claim that w + r > n quorums give "strong consistency" fails under variable network delay.

**The quorum counterexample:** with n=3, w=3, r=2, a write of x=1 is propagating. Reader A's quorum includes the one updated replica, so A returns 1. Reader B starts *after A finished* but its two replicas are both still stale, so B returns 0. New value then old value, in real-time order — a linearizability violation despite strict quorums.

You *can* rescue Dynamo-style reads/writes: readers must perform synchronous [[Read Repair]] before returning, and writers must first read the latest state from a quorum. But Riak skips synchronous read repair for performance, and Cassandra — which does wait for it — still loses linearizability under concurrent writes because last-write-wins timestamps are subject to [[Clock Skew]]. And even the rescued version covers only reads and writes: a linearizable compare-and-set fundamentally requires [[Consensus]].

## Trade-offs & Pitfalls
- "Quorum overlap" guarantees you *touch* a fresh replica, not that you *return* fresh data in a real-time-consistent way.
- Sloppy quorums (hinted handoff) destroy linearizability entirely.
- LWW + time-of-day clocks is almost certainly non-linearizable — timestamps do not track true event order.
- Safe default assumption: leaderless systems are not linearizable.

## Examples & Systems
[[ZooKeeper]], [[Etcd|etcd]] (via Zab/Raft); Riak and Cassandra as cautionary quorum tales; MongoDB stale-read findings (Jepsen).

## Related
- up: [[Linearizability]] · chapter: [[Ch 09 - Consistency and Consensus]]
- [[Limitations of Quorum Consistency]] — Chapter 5's first pass at this result
- [[Sloppy Quorums and Hinted Handoff]] — the availability feature that forfeits recency
- [[Fault-Tolerant Consensus]] — the machinery that actually works
- [[Detecting Concurrent Writes]] — why LWW discards causal order
