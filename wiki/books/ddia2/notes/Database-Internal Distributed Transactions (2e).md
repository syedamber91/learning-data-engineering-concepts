---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
topic: Distributed Transactions
type: subtopic
tags: [ddia2, newsql, spanner, cockroachdb, consensus, 2pc]
sources:
  - raw/ch08.md
---
# Database-Internal Distributed Transactions
> The same 2PC, without the lowest-common-denominator trap. Four specific fixes turn XA's worst problems into non-problems.

## The Idea
**There is a big difference between distributed transactions spanning multiple heterogeneous storage technologies and those internal to one system**, where all participating nodes are part of the same database running the same software. **Such internal distributed transactions are a defining feature of "NewSQL" databases** — **CockroachDB, TiDB, Spanner, FoundationDB, YugabyteDB** — and **some message brokers, such as Kafka, also support them.**

**Many of these systems use 2PC to ensure atomicity of transactions writing to multiple shards, yet they don't suffer from XA's problems.** Because their transactions **don't need to interface with any other technology, they avoid the lowest-common-denominator trap** — their designers are **free to use better protocols that are more reliable and faster.**

## How It Works
**The biggest problems with XA can be fixed by:**
- **Replicating the coordinator**, with automatic failover to another coordinator node if the primary crashes.
- **Allowing the coordinator and data shards to communicate directly**, without intermediary application code.
- **Replicating the participating shards**, so the risk of aborting a transaction because of a fault in one shard is reduced.
- **Coupling the atomic commitment protocol with a distributed concurrency control protocol** that supports deadlock detection and consistent reads across shards.

**Consensus algorithms are commonly used to replicate the coordinator and the database shards.** They **tolerate faults by automatically failing over from one node to another without human intervention, while continuing to guarantee strong consistency properties.**

**The isolation levels offered depend on the system, but snapshot isolation and serializable snapshot isolation are both possible across shards.**

## Trade-offs & Pitfalls
- Each of the four fixes maps directly onto one of XA's failure modes: **coordinator as SPOF → replicate it; application code as SPOF → direct communication; one shard's fault aborting everything → replicate shards; no cross-system deadlock detection or SSI → integrate commitment with concurrency control.** Read as a list, it is a diagnosis of XA rather than a feature list.
- **The cost of the fixes is the constraint that made them possible**: they work precisely because you control every participant. **There is no path from here to heterogeneous transactions** — which is why the next subtopic reaches for idempotence instead.

## Examples & Systems
CockroachDB, TiDB, Spanner, FoundationDB, YugabyteDB, VoltDB, Cassandra, MySQL Cluster NDB; Kafka for internal transactions in a message broker.

## Since the 1st Edition
**Entirely new as a subtopic.** The 1st edition drew the internal-versus-heterogeneous distinction in a paragraph and then focused almost entirely on XA's problems, leaving the reader with a broadly negative impression of distributed transactions. **The 2nd edition adds this subtopic to make the positive case**: the same 2PC algorithm, under different constraints, is a defining and successful feature of the NewSQL generation — and it names the four specific engineering changes that make the difference.

## Related
- up: [[Distributed Transactions (2e)]] · chapter: [[Ch 08 - Transactions (2e)]]
- [[Distributed Transactions Across Different Systems (2e)]] — the problems this fixes
- [[Consensus (2e)]] — the mechanism doing the replication
- [[What Exactly Is a Transaction (2e)]] — the NewSQL verdict this supports
