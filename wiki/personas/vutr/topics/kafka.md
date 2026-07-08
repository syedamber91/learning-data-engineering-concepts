---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: kafka
---

Related: [[kafka-origin]] · [[linkedin-kafka-scale]] · [[paypal-kafka-scale]] · [[logical-offset]] · [[page-cache-storage]] · [[zero-copy-sendfile]] · [[partition]] · [[consumer-offsets-topic]] · [[acks-setting]] · [[kraft]] · [[tiered-storage-kip-405]] · [[pull-over-push]] · [[broker-side-validation]] · [[cross-az-cost]]

## Comparisons
**Durability vs. throughput — the [[acks-setting]] dial.** acks=0 maximizes throughput at the cost of very high data-loss risk; acks=1 accepts loss only if the leader dies before replication; acks=all is safest but highest-latency. DoorDash's move to replication factor 2 + acks=1 shows the cost lever this exposes (30–40% CPU drop).

**Pull vs. push — [[pull-over-push]].** LinkedIn picked pull so consumers set their own pace and avoid being flooded, at the cost of consumers having to poll.

**Where storage lives — [[page-cache-storage]] vs. proprietary cache.** Kafka delegates to the OS page cache instead of a JVM-managed cache, avoiding object overhead and GC, and betting that sequential disk beats random RAM. This design choice is what enables [[zero-copy-sendfile]], since the on-disk format stays identical end-to-end.

**Where validation lives — [[broker-side-validation]] vs. client-side.** Client checks are opt-in and skippable; the broker is the one point every client must pass through, so validation is enforced there.

**Diskless Kafka designs.** AutoMQ is open-source, 100% Kafka-compatible, and leader-based (WAL on EBS or S3), whereas WarpStream and Bufstream are leaderless with a custom-built protocol and are not 100% compatible — a trade-off between compatibility and clean-slate design. All of these are reactions to [[cross-az-cost]].

**Partitioner evolution.** Round-Robin partitioner (Kafka ≤ 2.3) gave way to the Sticky Partitioner (Kafka ≥ 2.4).

## Open questions
- Is the compatibility cost of leaderless diskless designs (WarpStream, Bufstream, not 100% Kafka-compatible) worth it versus AutoMQ's compatible-but-leader-based approach?
- Given [[cross-az-cost]] can exceed 50% of the bill, at what scale does staying on self-managed Kafka stop making economic sense versus adopting a diskless variant?
- [[tiered-storage-kip-405]] keeps the broker stateful — what would it actually take to make Kafka brokers stateless, and is that the direction diskless designs are heading?
- After [[kraft]] removed ZooKeeper, what new operational trade-offs does folding metadata into Kafka itself introduce?
- Why did the [[partition]]er default shift from Round-Robin to Sticky at version 2.4, and what workloads regressed under the old behavior?

## Synthesis
Kafka came out of LinkedIn as a log-processing engine and was named after Franz Kafka because it is "a system optimized for writing" ([[kafka-origin]]) — a naming choice that foreshadows every design decision below. That write-first bet paid off at staggering scale: LinkedIn itself ran ~100 clusters / 4,000 brokers / 7M partitions / 7 trillion messages a day by 2019 ([[linkedin-kafka-scale]]), and PayPal independently reached 85+ clusters and a 1.3-trillion-messages-per-day peak ([[paypal-kafka-scale]]) — proof the architecture generalizes beyond its birthplace. Kafka's core performance story is about getting out of the data's way: [[logical-offset]] addressing avoids index structures, [[page-cache-storage]] avoids JVM/GC overhead, and [[zero-copy-sendfile]] avoids unnecessary copies — all held together by keeping one on-disk format from producer to consumer. Its scalability and correctness rest on ownership decisions: the [[partition]] is the unit of parallelism, the broker (not the client) owns the consume position via the [[consumer-offsets-topic]] and enforces [[broker-side-validation]], and consumers set their own pace through [[pull-over-push]]. The frontier is economic — [[cross-az-cost]] driving diskless and leaderless redesigns — and architectural, with [[kraft]] and [[tiered-storage-kip-405]] reshaping what a broker depends on and stores, while [[acks-setting]] remains the everyday dial operators turn to trade durability for cost.

## Related topics
- [[amazon-s3-gfs-hdfs-and-distributed-file-systems]] — Diskless Kafka designs (AutoMQ, WarpStream) push the write-ahead log onto S3/EBS, reacting to the same cross-AZ economics of distributed storage.
- [[apache-pinot-druid-and-real-time-olap]] — Real-time OLAP engines ingest streaming events from Kafka to serve low-latency queries over fresh data.
- [[big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter]] — LinkedIn invented Kafka and Uber runs it at trillions of messages/day, while Spotify and Meta deliberately routed around it — the case studies map Kafka's real adoption boundary.
- [[change-data-capture-cdc-and-data-sourcing]] — Even a Kafka consumer is pull-model consumption, and Kafka is the canonical transport onto which CDC change streams are published.
- [[flink]] — Flink is the low-latency stream processor that consumes Kafka's log, and true exactly-once depends on watermarks plus an idempotent sink at the streaming boundary.
- [[lsm-tree-storage-engines]] — Kafka is a log-structured, write-optimized engine — logical offsets over sequential disk I/O — the same append-first bet an LSM-tree makes against random writes.
