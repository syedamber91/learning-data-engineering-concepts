---
persona: vutr
kind: concept
sources:
- raw/kafka/how-do-we-run-kafka-100-on-the-object.md
- raw/kafka/automq-achieving-auto-partition-reassignment.md
- raw/kafka/groupby-5-the-story-of-s3-kafka-at.md
last_updated: '2026-07-10'
qc: passed
slug: zookeeper-to-kraft-metadata-management
topics:
- kafka
---

A common assumption is that Kafka's cluster metadata has always lived inside Kafka. It hasn't. Traditional Kafka relies on a separate fleet of ZooKeeper servers for cluster metadata management — an entire external coordination system you must deploy, operate, and keep healthy alongside the brokers themselves. KRaft is the correction to that design: it eliminates ZooKeeper, simplifying Kafka and enhancing resilience by moving metadata management inside the cluster.

Here is the actual mechanism. In KRaft mode, Kafka uses an internal Raft-based controller quorum — a group of brokers responsible for maintaining and ensuring metadata consistency. The Raft consensus algorithm does two jobs: it elects a leader for the quorum, and it replicates metadata changes across the quorum. The write path is strictly single-owner: the cluster metadata is stored in the controller quorum leader, and only the leader can modify it. If any broker wants to change the metadata, it must communicate with the leader — there is no side channel. The read path is fanned out: each broker in KRaft mode keeps a local copy of the metadata, and any change is propagated to every broker by the controller. That split — one writer, replicated to all readers — is what reduces operational complexity and removes the potential failure points that a separate ZooKeeper deployment introduced. (See [[raft-backed-coordination]] for the systems-level view of why Kafka, LinkedIn's Northguard, and ZooKeeper all reach for Raft-family consensus for exactly this kind of job — the note is honest that neither source explains the election-term/log-matching/quorum-commit mechanics themselves, which is still the open gap here.)

What actually lives in this metadata? The mappings that define the cluster's shape: the mapping between topic/partition and data, and the mapping between partitions and brokers. This sounds mundane until you see what it enables. In a shared-storage design like AutoMQ (which reuses Kafka's KRaft mechanism wholesale), the broker is entirely stateless — the relationship between a broker and a partition is managed *only* through this metadata, instead of physically storing partition data on the broker's local disk. Reassigning a partition then stops being a data-copy operation and becomes a metadata edit at the controller: adjust the broker-to-partition mapping in the leader, let the controller propagate it, done. That is the whole difference between Kafka rebalancing (move gigabytes over the network) and AutoMQ rebalancing (rewrite a mapping) — see [[partition-reassignment-and-cluster-balancing]] and [[automq-wal-shared-storage]].

The KRaft log also becomes an integration point, not just a bookkeeping detail. AutoMQ's AutoBalancer runs on the controller and maintains a ClusterModel of the cluster's current state and partition loads. Changes to the cluster — broker additions, removals, partition reassignments and deletions — are tracked by monitoring KRaft metadata to update that ClusterModel. And because AutoBalancer is an integral part of the system rather than an external tool like Cruise Control, it can directly consume the KRaft log, enabling it to react faster to cluster changes. An external balancer has to observe the cluster from outside; a component sitting on the controller reads the source of truth as it is written. Note the division of labor, though: load *metrics* (network traffic throughput and the like) do not travel through KRaft — AutoMQ ships those between broker and controller via an internal Kafka topic, while KRaft carries the membership and mapping changes.

The trade-off history matters here. ZooKeeper mode worked; the cost was a second distributed system and extra failure points. KRaft folds consensus into Kafka itself, but that only pays off if you can get there without stopping the cluster. That arrived with Apache Kafka 3.6.0, which shipped cluster migration from ZooKeeper to KRaft with no downtime — in the same release, incidentally, as Tiered Storage ([[tiered-storage-kip-405]]), the other pillar of decoupling Kafka's brokers from the state they carry. Metadata went to an internal quorum; historical data went to remote storage. Both moves point the same direction: brokers that own less state.
