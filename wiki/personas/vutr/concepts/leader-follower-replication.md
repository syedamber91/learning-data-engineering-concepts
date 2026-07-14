---
persona: vutr
kind: concept
sources:
- raw/kafka/apache-kafka-part-1-overview.md
- raw/kafka/automq-achieving-auto-partition-reassignment.md
- raw/kafka/how-to-choose-the-right-diskless.md
- raw/kafka/stream-kafka-topic-to-the-iceberg.md
last_updated: '2026-07-10'
qc: passed
slug: leader-follower-replication
topics:
- kafka
---

Replication in Kafka is usually presented as a pure durability feature. It is — but treat it as only that and you miss half the story: broker-level replication is also the reason partition rebalancing means moving real data over the network, and the reason multi-AZ Kafka deployments quietly bleed money on cross-zone traffic. The mechanism and its costs come as a package.

Start with the mechanism itself. At its heart, Kafka is a leader-based system. Messages in a topic are split across partitions, and each partition is replicated to a configurable number of brokers — the replication factor. Of those replicas, a single broker owns the partition: the leader. The brokers holding the additional copies are the followers. The division of labor is strict on the write side and loose on the read side: all producers must connect to the leader to publish, while consumers may fetch from either the leader or one of the followers (see [[producer-send-path-and-acks]] and [[pull-based-consumption-and-offset-commit]]).

The write path is what makes durability work. When the leader receives messages from producers, it replicates them to the followers. Physically, each partition is a logical log implemented as segment files of roughly equal size (around 1GB); the broker appends each incoming message to the last segment ([[log-segments-and-offset-addressing]]). Because the followers hold full copies, one of them can take over leadership if the leader's broker fails — Kafka automatically reassigns leadership of the dead broker's partitions to other brokers that hold replicas, and may eventually create new replicas on other available brokers to restore the replication factor. Within the cluster, one broker acts as the controller, responsible for administrative operations like these. To avoid concentrating high-traffic topics on a few nodes, Kafka distributes partition replicas across the cluster in a round-robin fashion.

Now the trade-offs, which follow directly from Kafka's tightly coupled compute-and-storage design. First, data movement: because replicas live on brokers' local disks, any change in cluster membership — a broker dies, a broker is added, or you want to even out load — forces partition data to move across the network ([[partition-reassignment-and-cluster-balancing]]). Second, cloud economics. In a typical high-availability setup with brokers spread across three availability zones, the cost shows up twice for the same message. Producers must reach the partition leader, and with leaders spread across three zones, roughly two-thirds of producer sends cross a zone boundary. Then the leader replicates that data to its followers in the other two AZs — an even larger wave of cross-AZ transfer, and a second set of network fees for data you already paid to move once.

That double cost is exactly what the newer architectures attack. Tiered storage ([[tiered-storage-kip-405]]) offloads historical segments to remote storage but leaves brokers stateful, so the replication problem persists. Diskless systems go further: cloud object storage is designed for extreme durability (often 99.999999999% or higher) using erasure coding and automatic cross-AZ replication, so the storage layer itself provides what leader-follower replication was doing. AutoMQ draws the blunt conclusion: with object storage guaranteeing durability and availability, replicating data across brokers is unnecessary, and every partition has exactly one replica — the leader ([[automq-wal-shared-storage]]). Notably, AutoMQ keeps the leader-based model even without followers — all writes for a partition still go through its leader — because that preserves Kafka's partition logic, keeps metadata small, and avoids the extra coordinator component that leaderless designs like WarpStream and Bufstream need ([[diskless-kafka-trade-off-framework]]).

The correct mental model, then: leader-follower replication is how shared-nothing Kafka buys durability and failover on local disks, at the price of network-heavy rebalancing and doubled cross-AZ fees. Whether that price is worth paying is precisely the question the diskless generation was built to reopen.

## Related in the other wiki
- [[Leaders and Followers]] — DDIA's chapter explains the general single-leader replication model — writes serialized through one leader, followers apply in order — that Kafka's partition leader/follower mechanism is a concrete instance of.
- [[Replication]] — DDIA's Replication concept frames the fault-tolerance/read-scaling trade-offs this Kafka-specific mechanism instantiates in a single, concrete leader-based system.
