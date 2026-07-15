---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
type: topic
tags: [ddia, replication-lag, eventual-consistency, read-anomalies]
sources:
  - raw/ch05.md
---
# Problems with Replication Lag

Read-scaling architectures pile up asynchronous followers and spread read traffic across them — attractive for read-heavy web workloads, but only workable asynchronously, since synchronously replicating to many nodes would make a single failure freeze all writes. The price is **replication lag**: a follower may serve data the leader has already superseded, so the same query can return different answers on different replicas. Left alone, replicas converge once writes stop — that is [[Eventual Consistency]], a deliberately vague promise with no bound on "eventually." Lag is usually sub-second but can stretch to minutes under load or network trouble, at which point three concrete anomalies bite real users. Each anomaly has a matching consistency guarantee that rules it out.

## Subtopics

- [[Reading Your Own Writes]] — a user's fresh submission seems to vanish when their next read hits a stale replica; fixed by read-after-write consistency.
- [[Monotonic Reads]] — successive reads from differently-lagged replicas make time appear to run backward; fixed by pinning each user to one replica.
- [[Consistent Prefix Reads]] — an observer sees an answer before its question because partitions replicate at different speeds; fixed by preserving causal order.
- [[Solutions for Replication Lag]] — why per-app workarounds are fragile and stronger guarantees belong in the database (transactions).

## Key Takeaways

- Eventual consistency guarantees convergence, not freshness — design for the case where lag hits minutes or hours, not the sub-second happy path.
- Each anomaly maps to a named guarantee: read-after-write, monotonic reads, consistent prefix reads — all weaker than [[Strong Consistency]] but stronger than plain eventual consistency.
- The anomalies stem from *where* a read lands, so remedies mostly steer reads: to the leader, to a pinned replica, or to a replica proven fresh enough via timestamps.
- [[Causality]] violations (consistent prefix) are specific to partitioned systems with no global write order.
- Solving these in application code is error-prone; transactions exist so the database can shoulder the guarantee instead.

## Related

- chapter: [[Ch 05 - Replication]]
- [[Synchronous Versus Asynchronous Replication]] — the root cause of lag
- [[Limitations of Quorum Consistency]] — leaderless systems fail these guarantees too
- [[Consistency Guarantees]] — the broader hierarchy these models sit in
- [[Linearizability]] — the strongest read guarantee, contrasted in Chapter 9
