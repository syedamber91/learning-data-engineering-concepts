---
persona: vutr
kind: concept
sources:
- raw/kafka/groupby-43-uber-kafka-the-tiered.md
- raw/kafka/how-do-we-run-kafka-100-on-the-object.md
- raw/kafka/if-youre-learning-kafka-this-article.md
- raw/kafka/stream-kafka-topic-to-the-iceberg.md
last_updated: '2026-07-10'
qc: passed
slug: tiered-storage-kip-405
topics:
- kafka
---

Start with the problem tiered storage actually solves, because it is narrower than people assume. Original Kafka stores messages in segment files on the broker's own filesystem (see [[log-segments-and-offset-addressing]]), so compute and storage are tightly coupled: the only way to scale storage is to add more machines, which means paying for CPU and RAM you don't need just to get more disk. On the cloud this coupling bites twice — you can't scale compute and storage independently to exploit pay-as-you-go pricing, and replication across availability zones racks up significant cross-AZ transfer fees. After hitting exactly these elasticity and resource-utilization problems, Uber proposed Kafka Tiered Storage (KIP-405).

The mechanism: instead of one storage system, a broker gets two tiers. The **local tier** is the broker's existing local disk, which keeps receiving the latest data. The **remote tier** extends storage to systems like HDFS, S3, GCS, or Azure and persists historical data. Each tier has its own retention configuration, by size and by time — and this asymmetry is the whole point. Local retention can be cut down to **hours**, while the remote tier retains data for **days or months**. Latency-sensitive consumers read from the local tier and keep the page-cache benefits of the original design ([[page-cache-sequential-io-and-zero-copy]]); backfill and failure-recovery workloads, which need older data, go to the remote tier.

Concretely, a topic partition's log is divided into two components: a **local log** made of local log segments and a **remote log** made of remote log segments. A remote log subsystem copies eligible segments from local to remote storage. Eligibility has a precise rule: a segment qualifies when its end offset is less than the partition's **LastStableOffset (LSO)** — the offset such that all lower offsets have been decided and are always present. The **leader broker** for the partition performs the copying, moving segments in sequence from earliest to latest. Uber's own illustration: local segments before offset "300" get deleted under the local retention config, but stay readable because they were already copied remotely.

On the read path, the two tiers are deliberately isolated. If a fetch request targets an offset still in local storage, the normal local fetch mechanism serves it. If it targets remote data, a **dedicated thread pool** handles it — so slow remote reads and fast local reads never block each other. Consumers can access remote messages directly without the data being loaded back onto the broker first.

Replication changes too (see [[leader-follower-replication]]): followers replicate segments only from the leader's **local** storage, and before fetching messages they must build auxiliary state — leader epoch state and producer-ID snapshots. The follower fetch protocol keeps messages consistent and ordered across replicas even through broker replacements or failures. The operational payoff is that brokers carry far less local data, so recovery and rebalancing move much less data over the network ([[partition-reassignment-and-cluster-balancing]]).

Now the correction, because this is where the hype outruns the design: **tiered storage does not make the broker stateless.** The broker still owns the local hot tier, replication between brokers still happens, and messages still have to move around when cluster membership changes. KIP-405 loosens the compute-storage coupling; it does not remove it. That residual statefulness is precisely the question AutoMQ's engineers asked next — "is there a way to store *all* of Kafka's data in object storage while keeping local-disk-like performance?" — which leads to the shared-storage generation: [[automq-wal-shared-storage]], [[warpstream-stateless-agent-architecture]], and eventually proposals like KIP-1150 diskless topics ([[diskless-kafka-trade-off-framework]]). In the evolution story — shared-nothing → tiered storage → shared storage → shared data ([[kafka-iceberg-zero-etl]]) — KIP-405 is the first step, and an intentionally conservative one.

The trade-off summary: you gain independent storage scaling, much longer retention (months instead of what a broker disk can hold), lighter brokers with faster recovery and rebalancing, and remote reads that don't pollute the hot path. You keep a stateful broker, tier-management complexity (two retention configs per topic instead of one), and the full replication cost for the local tier. If your pain is retention and disk growth, tiered storage is the fix; if your pain is cross-AZ replication cost or elasticity itself, it only gets you partway.
