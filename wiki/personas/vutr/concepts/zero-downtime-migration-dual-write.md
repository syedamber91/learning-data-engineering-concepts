---
persona: vutr
kind: concept
sources:
- raw/kafka/kafka-migration-with-zero-downtime.md
- raw/kafka/the-company-that-created-kafka-is.md
last_updated: '2026-07-10'
qc: passed
slug: zero-downtime-migration-dual-write
topics:
- kafka
---

Start with the misconception: people assume MirrorMaker 2 gives you a safe Kafka migration. It replicates data to a target cluster, yes — but to guarantee nothing is lost or reordered during cutover, producers must **stop producing and wait** for all remaining messages to settle on the new cluster before resuming there. Consumers have nothing to consume during that wait. That wait is the downtime, and it's inherently **unpredictable and uncontrollable** — it depends on data volume, network latency, and the sync tool's processing speed. Worse, MM2 doesn't preserve offsets: it relies on an **imprecise offset mapping** rather than direct replication (the mapping isn't maintained for every record because that would be too costly), which can cause data reprocessing when consumers migrate. And the offset translation doesn't work at all for applications like Flink or Spark that manage offsets externally. Add the manual orchestration — stopping/starting numerous app instances, coordinating teams, hand-verifying consistency — and there's no native client redirection mechanism, so the whole thing is error-prone by construction.

AutoMQ's Kafka Linking is the industry's **first** zero-downtime Kafka migration solution with message offset preservation (currently Kafka→AutoMQ only). It rests on two principles: **dual write** and **rolling upgrade**.

**Dual write.** Data written to Kafka is synced to AutoMQ, and data written to AutoMQ is synced *back* to Kafka — so admins can roll back safely at any point. AutoMQ's partition leaders run the migration, wearing two hats:

- As **Fetcher**, the AutoMQ partition leader acts like a consumer pulling from Kafka's partition leaders. Setup takes the source cluster details, topics, and a sync starting point (`earliest` = first message's offset, `latest` = current last message's offset, or a `timestamp`); if a fresh AutoMQ partition uses `latest`/`timestamp`, the Fetcher may internally truncate it so its start aligns with the chosen source offset. Kafka Linking continuously monitors source leadership — on a leader change, the affected partition goes into a "pre-processing queue" processed asynchronously. The Fetcher fetches incrementally (only new data since the last successful fetch), appends responses to object storage, retries on failure by error type (e.g., re-resolving a changed leader), and resumes exactly where it left off — no gaps, no duplicates. It also fetches rack-aware to avoid cross-AZ traffic.
- As **Router**, the same leader acts like a producer forwarding AutoMQ writes back to Kafka. It maps received messages into an in-memory map keyed by partition, and within each partition's pool groups messages **by source producer** — because Kafka guarantees FIFO per producer per partition, this grouping preserves ordering ([[producer-send-path-and-acks]]). It reuses the producer's existing batches instead of re-aggregating ([[message-batching-and-compression]]), sends complete batches, and parallelizes across producers while keeping each producer's batches strictly sequential.

**Rolling upgrade.** Instead of a big-bang cutover, clients move in small batches. Producers first: a subset is repointed to AutoMQ while the rest keep writing to Kafka; everything a migrated producer sends is immediately forwarded back to Kafka, so the source cluster stays the **single source of truth** for consumption and rollback stays trivial. Then consumers: when a consumer connects to AutoMQ mid-migration, AutoMQ **disables reading** for it — if it read immediately while the group was still partially active on the source, messages would be consumed more than once. Only when the entire consumer group is redirected and detected offline from the source does Kafka Linking sync that group's committed offset from the source ([[pull-based-consumption-and-offset-commit]]), then enable reading; the AutoMQ control plane monitors and auto-promotes the group. Finally, per-topic promotion is manual: AutoMQ stops copying from and forwarding to the source for that topic and becomes its standalone cluster. Other topics follow in batches.

The same dual-write logic shows up at LinkedIn's scale. Migrating off Kafka (150 clusters, 10,000 machines, 400,000 topics, 17PB/day) to [[northguard-segment-level-replication]] is even harder because Northguard speaks a different protocol entirely. Their answer, **Xinfra**, is a virtualized Pub/Sub layer abstracting physical clusters for both systems. It migrates producers first, then consumers, with producers writing to **both** Kafka and Northguard during migration for safe fallback — clients operate normally throughout, and dual writes are switched off at the end.

The trade-off framing matters: dual write buys you a reversible, incremental migration at the cost of running forwarding machinery in both directions. What MM2 makes an unpredictable maintenance window, dual write plus rolling upgrade turns into a controlled, per-topic, per-group promotion — related context on why teams migrate at all lives in [[automq-wal-shared-storage]] and [[diskless-kafka-trade-off-framework]].
