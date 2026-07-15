---
persona: vutr
kind: concept
sources:
- raw/uber-data-infrastructure-case-studies/how-did-uber-build-their-data-infrastructure.md
- raw/uber-data-infrastructure-case-studies/i-spent-7-hours-understanding-ubers.md
last_updated: '2026-07-15'
qc: passed
slug: uber-kafka-scale-customizations
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Uber runs "one of the largest deployments of Apache Kafka" — trillions of messages and petabytes of data per day, backing everything from rider/driver event propagation to database change-log distribution. Stock Kafka wasn't enough at that scale, so Uber layered four customizations on top of it.

**Cluster federation** hides physical cluster topology from producers and consumers behind "logical Kafka clusters": a dedicated server centralizes cluster and topic metadata and routes each client request to the right physical cluster. This buys two things — horizontal scalability (a fully-utilized cluster gets more clusters added, and new topics land there seamlessly) and easier topic management, since migrating a live topic between physical clusters normally requires manual reconfiguration and a consumer restart; federation instead redirects traffic to the new physical cluster without touching the application.

**Dead Letter Queues (DLQ)** solve the "downstream can't process this message" problem. Stock Kafka only offers two bad options — drop the message, or retry indefinitely and block everything behind it. Uber's DLQ strategy gives a third path: if the consumer still can't process a message after retries, it publishes that message to the DLQ, so the unprocessed message is quarantined without stalling the rest of the stream.

**Consumer Proxy** exists because tens of thousands of Kafka-consuming applications, written in many languages, made debugging and client-library upgrades painful. The proxy reads messages from Kafka and routes them to a gRPC service endpoint, so applications only need a thin gRPC client rather than the full consumer library's complexity. It also retries failed deliveries and routes to the DLQ after repeated failures — and, notably, it flips Kafka's delivery model from pull-based polling to push-based dispatch, which improves consumption throughput and opens up more concurrent processing.

**Cross-cluster replication** answers two needs that come from running multiple Kafka clusters across data centers: getting a *global* view of data (e.g., consolidating trip metrics computed per-datacenter) and buying redundancy against datacenter failure. Uber built and open-sourced uReplicator for this. Architecturally, uReplicator uses Apache Helix for cluster management: a Helix controller distributes topic-partitions to worker nodes, detects failures, and redistributes partitions away from failed nodes; it writes the topic/partition-to-worker mapping to ZooKeeper as the source of truth, and Helix agents on each worker are notified when that mapping changes, with `DynamicKafkaConsumer` instances actually carrying out the replication work. uReplicator's rebalancing algorithm specifically minimizes the number of affected topic-partitions during a rebalance, and it can redistribute load to standby workers at runtime during a traffic burst. Uber paired this with Chaperone, an open-sourced auditing service that collects per-stage message counts across the replication pipeline and raises an alert on any mismatch — the mechanism that lets Uber trust that cross-cluster replication isn't silently losing data.

Together these four pieces show a consistent shape: Uber didn't change Kafka's core log/partition model, it wrapped operational and reliability concerns (topology, poison messages, client sprawl, multi-DC redundancy) in additional infrastructure layered on top.

*See also: [[uber-data-platform]] · [[uber-flink-unified-platform]] · [[uber-realtime-infra-requirements]]*
