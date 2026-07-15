---
persona: vutr
kind: topic
sources:
- raw/consensus
last_updated: '2026-07-15'
qc: passed
topic: consensus
---

Related: [[raft-backed-coordination]]

## Overview
This topic covers Raft-family consensus at the systems level — which real systems use it and why, grounded in vutr's own posts on LinkedIn's Northguard and on the CAP theorem/ZooKeeper's CP role. It's deliberately scoped to what vutr's own captured writing actually supports: the systems-level "why consensus, why here" story, not Raft's internal algorithmic mechanics (leader election terms, log replication, quorum commit), which neither source explains — that depth lives in the DDIA book's [[Fault-Tolerant Consensus]] note instead.

## Open questions
- **source gap**: neither captured post explains Raft's actual election-term/log-matching/quorum-commit mechanics — for that depth, see [[Fault-Tolerant Consensus]] in the DDIA book wiki.
- The sources don't reconcile how Northguard's "strong consistency without sacrificing availability" framing squares with CAP's usual CP-vs-AP tension — is Northguard's per-shard Raft group small enough that partitions are rare in practice, or is there a nuance the sources don't spell out?

## Synthesis
The common thread across both sources: Raft-family consensus gets reached for specifically when a system needs one unambiguous, non-forking answer — who the leader is, what a shard's metadata state is — and is willing to trade availability during a network partition to get it. LinkedIn's Northguard shards that requirement across many small Raft groups (avoiding the single-controller bottleneck classic Kafka has); ZooKeeper centralizes it as an external CP coordination service other systems delegate to. Both are the same underlying bet, applied at different granularities.

## Related topics
- [[transactions]] — a different axis of "which answer is the true one under concurrency": this topic covers agreement across machines (Raft, leader election); that topic covers agreement across concurrent transactions on one machine (isolation levels, MVCC).
- [[zookeeper-to-kraft-metadata-management]] — the Kafka-specific version of this same choice: classic Kafka delegated to ZooKeeper (this topic's second example), then moved metadata management to an internal Raft-based quorum (KRaft) instead.
- [[kafka]] — Northguard was built to replace Kafka at LinkedIn's own scale; KRaft is Kafka's own internal adoption of the same Raft-based pattern this topic covers.
- [[cap-vs-acid-consistency]] — the CAP/PACELC framing this topic's CP-vs-availability trade-off sits inside.
- [[Fault-Tolerant Consensus]] (DDIA book) — the algorithmic depth (Paxos/Raft/Zab/VSR mechanics, epoch numbers, quorum overlap) that this topic's own sources don't cover — the explicit target of this topic's source-gap flag above.
