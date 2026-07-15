---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, consistency, replication]
sources:
  - raw/ch05.md
---
# Eventual Consistency

The weak promise that if writes stop, replicas will *eventually* converge to the
same value — with no bound on how long "eventually" takes and no guarantees about
what reads return meanwhile. It's the default posture of asynchronously replicated
and leaderless systems.

In the book: the anomalies of [[Problems with Replication Lag]] (stale reads,
going-backward reads, causal inversions) are what eventual consistency permits, and
the session guarantees ([[Reading Your Own Writes]], [[Monotonic Reads]],
[[Consistent Prefix Reads]]) are patches over it. Contrast with
[[Strong Consistency]] / [[Linearizability]].

## Referenced In
- [[Ch 05 - Replication]]
- [[Change Data Capture]]
- [[Combining Specialized Tools by Deriving Data]]
- [[Consistency Guarantees]]
- [[Detecting Concurrent Writes]]
- [[Knowledge, Truth, and Lies]]
- [[Leaderless Replication]]
- [[Limitations of Quorum Consistency]]
- [[Monotonic Reads]]
- [[Problems with Replication Lag]]
- [[Reading Your Own Writes]]
- [[Solutions for Replication Lag]]
- [[Synchronous Versus Asynchronous Replication]]
- [[System Model and Reality]]
- [[The Meaning of ACID]]
