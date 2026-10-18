---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
topic: Linearizability
type: subtopic
tags: [ddia2, replication, quorum, read-repair, consensus, dynamo]
sources:
  - raw/ch10.md
---
# Implementing Linearizable Systems
> Single-leader: potentially. Consensus: likely. Multi-leader: no. Leaderless quorums: probably not, even with w + r > n.

## The Idea
**Since linearizability means "behave as though there is only a single copy of the data and all operations on it are atomic," the simplest answer would be to really use only a single copy.** **But that couldn't tolerate faults** — if that node failed, the data would be lost, or at least inaccessible until it came back.

So the question is which replication methods can be made linearizable.

## How It Works
**Single-leader replication (potentially linearizable).** The leader has the primary copy used for writes; followers hold backups. **As long as you perform all reads and writes on the leader, they are likely to be linearizable.** **But this assumes you know for sure who the leader is** — and **it is quite possible for a node to think it is the leader when it is not, and if the delusional leader continues serving requests it is likely to violate linearizability.** **With asynchronous replication, failover may even lose committed writes, violating both durability and linearizability.**

**Sharding a single-leader database, with a separate leader per shard, does not affect linearizability, since it is only a single-object guarantee.** Cross-shard transactions are a different matter.

**Consensus algorithms (likely linearizable).** Some are **essentially single-leader replication with automatic leader election and failover**, **carefully designed to prevent split brain**, which lets them implement linearizable storage safely. **ZooKeeper uses Zab; etcd uses Raft.** **However, just because a system uses consensus does not guarantee all operations on it are linearizable** — **if it allows reads on a node without checking that it is still the leader, results may be stale if a new leader has just been elected.**

**Multi-leader replication (not linearizable).** These **concurrently process writes on multiple nodes and asynchronously replicate them**, so **they can produce conflicting writes requiring resolution.**

**Leaderless replication (probably not linearizable).** People sometimes claim you get "strong consistency" from quorum reads and writes with **w + r > n**. **Depending on the exact algorithm and how you define strong consistency, this is not quite true.**

**LWW conflict resolution based on time-of-day clocks — as in Cassandra and ScyllaDB — is almost certainly nonlinearizable**, because clock timestamps cannot be guaranteed consistent with actual event ordering given clock skew. **And even with quorums, nonlinearizable behavior is possible:**

x starts at 0; a writer updates it to 1, sending to all three replicas (n = 3, w = 3). **Concurrently, client A reads from a quorum of two nodes and sees the new value 1 on one and the old value 0 on the other. Also concurrently, client B reads from a different quorum of two and gets 0 from both.** **The quorum condition w + r > n is met, but this execution is not linearizable: B's request begins after A's completes, yet B returns the old value while A returns the new one.** Aaliyah and Bryce again.

## Trade-offs & Pitfalls
**It is possible to make Dynamo-style quorums linearizable, at the cost of reduced performance:**
- **A reader must perform read repair synchronously before returning results.**
- **Before writing, a writer must read the latest state of a quorum to fetch the greatest prior timestamp and ensure the new write has a greater one.**

**Riak does not perform synchronous read repair because of the performance penalty.** **Cassandra does wait for read repair to complete on quorum reads, but loses linearizability anyway because of its use of time-of-day clocks for timestamps.**

**And even then, only linearizable read and write operations can be implemented this way — a linearizable CAS operation cannot, because it requires a consensus algorithm.** **In summary, it is safest to assume that a leaderless system with Dynamo-style replication does not provide linearizability, even with quorum reads and writes.**

## Examples & Systems
ZooKeeper (Zab), etcd (Raft); Riak and Cassandra as the leaderless counterexamples.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Implementing Linearizable Systems]] — the same four-way assessment of replication methods, the same nonlinearizable-quorum example, and the same conclusion about Dynamo-style systems. One of the most stable sections in the chapter.

## Related
- up: [[Linearizability (2e)]] · chapter: [[Ch 10 - Consistency and Consensus (2e)]]
- [[Writing to the Database When a Node Is Down (2e)]] — the quorum machinery being assessed
- [[Consensus in Practice (2e)]] — how consensus algorithms achieve this safely
- [[Handling Node Outages (2e)]] — the delusional-leader problem
- 1st edition: [[Implementing Linearizable Systems]] — the same subtopic
