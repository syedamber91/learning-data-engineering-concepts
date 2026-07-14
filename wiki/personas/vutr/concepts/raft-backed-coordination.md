---
persona: vutr
kind: concept
sources:
- raw/consensus/the-company-that-created-kafka-is.md
- raw/consensus/i-spent-8-hours-learning-the-cap.md
last_updated: '2026-07-15'
qc: passed
slug: raft-backed-coordination
topics:
- consensus
---

Raft-family consensus keeps showing up in the notes wherever a distributed system needs one thing to be unambiguously true — who owns this piece of metadata right now, who the leader is — even while the system as a whole keeps running across many machines that can fail independently.

LinkedIn's Northguard, the system LinkedIn built to replace Kafka at their own scale, is the clearest example. Northguard shards its metadata — about topics, ranges, and segments — across many vnodes using consistent hashing (topic metadata hashed by topic name, range/segment metadata by range ID), and each vnode's slice of metadata is kept correct with Raft-backed replicated state machines. The choice is explained by what it buys, not by how the algorithm itself works: sharding metadata across many small Raft-backed groups instead of routing everything through one central controller (the way classic Kafka's controller works) eliminates that single controller as a bottleneck, while consensus within each shard still gives strong consistency for the metadata that shard owns. Northguard's design goal, in the notes' own framing, was strong consistency for both data and metadata without giving up the high throughput, low latency, high availability, and high durability Kafka already had — decentralized, Raft-backed metadata is the piece that lets LinkedIn hold onto consistency while decentralizing everything else about the system.

ZooKeeper is the second example, and it plays a related but distinct role: coordination *for* other systems, rather than a system's own internal metadata layer. The notes place ZooKeeper squarely on the CP side of the CAP theorem — it's "designed to be the source of truth for distributed configuration, leader election, and service discovery," a role where handing back two different, inconsistent answers is not acceptable, so ZooKeeper will make a caller wait (or fail) rather than do that. Northguard's Raft-backed metadata layer is solving the same underlying requirement — one unambiguous answer about who the leader is or what a segment's current state is — but its own source frames this differently: it describes Raft-backed consensus per shard as delivering strong consistency for metadata *alongside* high availability, not the explicit refuse-or-wait trade-off the CAP source states for ZooKeeper. Classic Kafka relied on ZooKeeper for exactly this job before KRaft moved metadata management inside the Kafka cluster itself (see [[zookeeper-to-kraft-metadata-management]]) — so the systems-level continuity across ZooKeeper, KRaft, and Northguard is that whether the coordination lives in an external CP service, an internal Raft-based controller quorum, or many per-shard Raft groups, the requirement being solved is the same one: exactly one leader, and a single, consistent, non-forking answer about state that must not diverge.

The common thread across both sources: Raft-family consensus gets reached for specifically when a system needs a CP guarantee — for metadata, or for leader election — and is willing to pay availability during a network partition to get it. See [[cap-vs-acid-consistency]] for the CAP/PACELC trade-off this sits inside, and [[zookeeper-to-kraft-metadata-management]] for the Kafka-specific version of the same choice.

## Open questions
- **source gap**: neither captured post explains Raft's actual election-term/log-matching/quorum-commit mechanics — for that depth, see [[Fault-Tolerant Consensus]] in the DDIA book wiki (`wiki/books/ddia/notes/Fault-Tolerant Consensus.md`).
