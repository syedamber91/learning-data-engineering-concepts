---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
type: chapter-moc
tags: [ddia2, linearizability, consensus, logical-clocks, cap, coordination, moc]
sources:
  - raw/ch10.md
---
# Ch 10 – Consistency and Consensus
Lots of things can go wrong in distributed systems. **If we want a service to keep working correctly despite them, we need ways of tolerating faults — and one of the best tools is replication.** But multiple copies increase the risk of inconsistencies: reads may hit a stale replica, and if multiple replicas accept writes we must handle conflicts. **Two competing philosophies:**

- **Eventual consistency** — **the fact that a system is replicated is made visible to the application**, and you as the developer are expected to deal with the inconsistencies and conflicts. Common in multi-leader and leaderless systems.
- **Strong consistency** — **applications should not have to worry about replication internals; the system should behave as if it were a single node.** **Simpler for the developer**, at the cost of **a performance penalty, and some faults an eventually consistent system tolerates cause outages in a strongly consistent one.**

Where replicas communicate over slow, unreliable links — sync engines and local-first software — **eventual consistency is inevitable.** **But eventual consistency can be difficult to deal with, and if your replicas are in datacenters with fast, reliable communication, strong consistency is often appropriate because its cost is acceptable.**

This chapter goes deep on the strongly consistent approach in three areas: **making "strong consistency" precise as linearizability**; **generating IDs and timestamps** (which sounds unrelated but is closely connected); and **achieving linearizability while remaining fault-tolerant — the answer being consensus algorithms.** Along the way we meet **fundamental limits on what is possible in a distributed system.**

> **These topics are notorious for being hard to implement correctly.** It is very easy to build systems that behave fine without faults but **completely fall apart on an unlucky combination of faults or message orderings their designers hadn't considered.** The chapter **sticks with informal intuitions and avoids the algorithmic nitty-gritty, formal models, and proofs** — to do serious work on consensus systems **you will need to go much deeper into the theory if you want any chance of your systems being robust.**

## Map
- [[Linearizability (2e)]] — behave as if there is only one copy of the data
  - [[What Makes a System Linearizable (2e)]] — the register model, the recency guarantee, and linearizability versus serializability
  - [[Relying on Linearizability (2e)]] — leader election, uniqueness constraints, and cross-channel timing dependencies
  - [[Implementing Linearizable Systems (2e)]] — which replication methods can and cannot deliver it
  - [[The Cost of Linearizability (2e)]] — CAP, why CAP is unhelpful, and why even your CPU isn't linearizable
- [[ID Generators and Logical Clocks (2e)]] — unique IDs, and what ordering they can promise
  - [[Logical Clocks (2e)]] — Lamport timestamps, hybrid logical clocks, and vector clocks
  - [[Linearizable ID Generators (2e)]] — the embarrassing-photo bug, timestamp oracles, and why IDs aren't enough for locks
- [[Consensus (2e)]] — getting multiple nodes to agree, fault-tolerantly
  - [[The Many Faces of Consensus (2e)]] — single-value consensus, CAS, shared logs, fetch-and-add, and atomic commitment are all equivalent
  - [[Consensus in Practice (2e)]] — epochs, two rounds of voting, and the pros and cons
  - [[Coordination Services (2e)]] — ZooKeeper, etcd, Consul, and what they're actually for

## Chapter Summary
**Linearizability** is a **recency guarantee**: make the system appear as if there is only one copy of the data and all operations on it are atomic, so **as soon as one client completes a write, all clients reading must see the value just written.** It is **the strongest consistency model in common use** and includes read-after-write, monotonic reads, and consistent prefix reads. **It is not the same as serializability** — serializability is a transaction isolation level over multiple objects with no recency requirement; linearizability is a single-object recency guarantee that does not prevent write skew. Together they are **strict serializability**.

**Linearizability is genuinely useful** for **leader election and locking**, for **hard uniqueness constraints**, and wherever there are **cross-channel timing dependencies** — two communication paths between the same parties, where the faster one can outrun replication. **Single-leader replication and consensus algorithms can provide it; multi-leader cannot; leaderless quorums probably don't**, even with w + r > n.

**It has a cost.** During a network partition you must choose between linearizability and availability — the honest reading of **CAP**, which the book calls **mostly of historical interest today** and misleading as usually stated. **But the deeper cost isn't fault tolerance at all: it's latency.** Even RAM on a multi-core CPU is not linearizable, for performance reasons — and **Attiya and Welch prove that linearizable response times are at least proportional to the uncertainty of network delays.** **A faster algorithm does not exist.**

**ID generation turns out to be the same problem in disguise.** Sharded IDs, preallocated blocks, random UUIDs, and wall-clock-based schemes all give uniqueness but **weak ordering**. **Logical clocks** — Lamport timestamps and hybrid logical clocks — **give a total order consistent with causality without special hardware**, and **vector clocks** additionally detect concurrency at the cost of size. **But even a linearizable ID generator is not sufficient for locks and uniqueness constraints**: a node cannot tell whether its own timestamp is lowest without hearing from every other node, **so we need something stronger — consensus.**

**Consensus** unifies the chapter. **Single-value consensus, compare-and-set, shared logs (total order broadcast), atomic fetch-and-add, and atomic commitment are all equivalent** — a solution to one converts into a solution for any other. **Most practical consensus systems provide shared logs**, which underpin state machine replication, event sourcing, serializable transactions, and fencing tokens. The algorithms — **Viewstamped Replication, Paxos, Raft, Zab** — work by **defining epochs in which the leader is unique**, then requiring **two rounds of quorum voting**: one to elect, one per log entry. **Consensus is essentially "single-leader replication done right"**, and **any system providing automatic failover without a proven consensus algorithm is likely to be unsafe** — but it **requires a strict majority, can't scale throughput by adding nodes, and is sensitive to timeout tuning.**

## Since the 1st Edition
This is the 1st edition's Chapter 9, **substantially reorganised**. **Moved out:** the entire **atomic commit / two-phase commit / XA** section, which is now in [[Ch 08 - Transactions (2e)]] where it belongs — atomic commit is a transaction property, not a consistency model. **Moved in and expanded:** ID generation. The 1st edition's [[Ordering Guarantees]] topic (causal order, sequence number ordering, Lamport timestamps, total order broadcast) is **dissolved and redistributed**: Lamport timestamps and the new **hybrid logical clocks** become [[Logical Clocks (2e)]] under a new [[ID Generators and Logical Clocks (2e)]] topic, while **total order broadcast is refolded into [[The Many Faces of Consensus (2e)]] as "shared logs."**

**Genuinely new:** **hybrid logical clocks**; **[[Linearizable ID Generators (2e)]]** with the embarrassing-photo scenario and **timestamp oracles** (TiDB/TiKV, Percolator); the systematic **equivalence proof sketch** across five formulations of consensus, including **consensus numbers** (fetch-and-add is 2, CAS and shared logs are ∞); **EPaxos and Raft's pre-vote phase**; and Kafka's **unclean leader election** as a worked example of trading consensus properties for availability. **Sharpened:** the CAP verdict — the 1st edition called CAP misleading; **the 2nd says it has been superseded and is of mostly historical interest**, and adds **PACELC** with the same criticism.

## Related
- home: [[Home (2e)]] · previous: [[Ch 09 - The Trouble with Distributed Systems (2e)]] · next: [[Ch 11 - Batch Processing (2e)]]
- [[Ch 08 - Transactions (2e)]] — serializability, and the atomic commit material that moved there
- [[Ch 06 - Replication (2e)]] — the weaker models this chapter is measured against
- 1st edition: [[Ch 09 - Consistency and Consensus]] — the chapter this one revises
