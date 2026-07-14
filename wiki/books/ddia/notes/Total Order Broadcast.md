---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
topic: Ordering Guarantees
type: subtopic
tags: [ddia, total-order-broadcast, state-machine-replication, atomic-broadcast]
sources:
  - raw/ch09.md
---
# Total Order Broadcast
> A protocol that delivers every message to every node, in the same order, with the order fixed at delivery time — equivalent to an append-only log, to linearizable compare-and-set storage, and ultimately to consensus itself.

## The Idea
On one CPU core a total order is free: it's just execution order. Across nodes, getting everyone to agree on one order of operations — while tolerating faults — is the problem the literature calls **total order broadcast** (or *atomic broadcast*, an unfortunate name unrelated to [[ACID]] atomicity). It supplies what [[Sequence Number Ordering]] lacked: knowing the order is *final*, so decisions like uniqueness constraints become safe.

## How It Works
Two safety properties must always hold, even with faulty nodes or networks:
- **Reliable delivery** — no message is lost; if one node gets it, all do.
- **Totally ordered delivery** — every node sees the messages in the same order.

Messages can't flow during a network interruption, but a correct algorithm retries until they get through — still in order. Note the scope caveat: partitioned databases with one leader per partition usually order only *within* a partition, forfeiting cross-partition guarantees ([[Partitioning and Replication]]).

Crucially, the order is **fixed at delivery time**: no node may retroactively slot a message before ones already delivered. That is exactly what timestamp ordering could not offer. Equivalently, total order broadcast *is* a log (like a replication log or [[Write-Ahead Log]]): delivering a message is appending to it, and everyone reads the same sequence. Uses follow directly:
- **State machine replication** — if each message is a write and replicas apply identical writes in identical order, they stay consistent.
- **Serializable transactions** — deterministic stored procedures executed in message order ([[Actual Serial Execution]]).
- **[[Fencing Tokens]]** — log positions are monotonically increasing sequence numbers (ZooKeeper's `zxid`).

**Linearizable storage from total order broadcast.** Broadcast is asynchronous (no recency promise); [[Linearizability]] is a recency guarantee — yet you can build one from the other. Linearizable compare-and-set for username claims: (1) append a message tentatively claiming the name, (2) wait until your message is delivered back, (3) if the *first* claim delivered for that name is yours, commit; otherwise abort. All nodes agree who was first. This makes *writes* linearizable; reads served from asynchronously updated state may be stale (yielding only sequential/timeline consistency). Linearizable reads need extra work: sequence the read itself through the log, ask the log for the latest position and wait to catch up (ZooKeeper's `sync()`), or read a synchronously updated replica (chain replication).

**The reverse direction** also works: given a linearizable integer register with atomic increment-and-get, stamp each message with the value you get and deliver by sequence number. Unlike [[Lamport Timestamps]], these numbers have *no gaps* — a node holding message 6 after message 4 knows it must wait for 5. That gap-freeness is the key difference from timestamp ordering, and it's why a linearizable sequence generator, pursued to its fault-tolerant conclusion, *is* a consensus algorithm: linearizable compare-and-set (or increment-and-get) and total order broadcast are both equivalent to [[Consensus]].

## Trade-offs & Pitfalls
- Waiting for delivery-back is essential; acknowledging on enqueue gives you roughly x86's memory model — neither linearizable nor sequentially consistent.
- Per-partition ordering means no consistent snapshots or foreign-key checks across partitions without extra coordination.

## Examples & Systems
[[ZooKeeper]] and [[Etcd]] implement total order broadcast; etcd's quorum reads and ZooKeeper's `sync()`; chain replication; Calvin-style deterministic transaction execution.

## Related
- up: [[Ordering Guarantees]] · chapter: [[Ch 09 - Consistency and Consensus]]
- [[Fault-Tolerant Consensus]] — the algorithms that implement this in practice
- [[Implementing Linearizable Systems]] — the sibling problem it can solve
- [[Partitioned Logs]] — the same log abstraction in stream processing
- [[The Truth Is Defined by the Majority]] — why finality needs agreement, not self-belief
