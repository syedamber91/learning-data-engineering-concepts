---
persona: vutr
kind: concept
sources:
- raw/kafka/i-spent-8-hours-researching-warpstream.md
- raw/kafka/how-to-choose-the-right-diskless.md
last_updated: '2026-07-10'
qc: passed
slug: warpstream-stateless-agent-architecture
topics:
- kafka
---

Start with the misconception: WarpStream is not Kafka with S3 bolted on. That would be tiered storage ([[tiered-storage-kip-405]]), where brokers still hold recent data locally and stay stateful. WarpStream is a ground-up rewrite of the Kafka protocol in Go — announced in 2023, acquired by Confluent on September 10th, 2024 — that runs 100% on object storage and replaces brokers entirely with a stateless binary called the agent. The founders (who previously built Husky, a scalable data store at Datadog) were attacking specific cloud pain: cross-AZ transfer fees, expensive EBS multiplied by the replication factor, and the inability to scale storage independently of compute. Even adding a node to classic Kafka means rebalancing partitions and waiting for replication ([[partition-reassignment-and-cluster-balancing]]).

The deployment model is BYOC: agents run inside the customer's VPC, message data goes to the customer's own S3/GCS, and only metadata leaves for the WarpStream cloud. That split is the architecture — data plane (the agent pool) versus control plane (WarpStream cloud), which decides which agents compact files, which participate in the cache, and which delete files past retention. Instead of ZooKeeper or KRaft ([[zookeeper-to-kraft-metadata-management]]), metadata lives in a store combining a strongly consistent database with object storage in WarpStream's account: DynamoDB + S3 on AWS, Cloud Spanner + GCS on GCP, Cosmos DB + Blob Storage on Azure. Most of what it holds is pointers to batches of data in object storage.

Statelessness changes leadership. In Kafka, a specific broker leads each partition and all writes go through it ([[leader-follower-replication]]). In WarpStream, no agent leads anything — any agent can read or write any partition. But Kafka clients *expect* partition leaders, so the control plane lies to them: it assigns an agent and makes the client believe that agent is the leader. Service discovery works the same way — the client resolves a single WarpStream bootstrap URL via DNS, gets any agent, and the discovery service then hands back an agent in the client's own AZ. Where open-source Kafka rebalances partitions across nodes, WarpStream rebalances *connections* across agents, round-robin.

Walk the write path, because this is where the trade-off lives. Producers send batches to an agent; the agent buffers requests from multiple producers — by default 250ms or 8 MiB, whichever first — writes one file to object storage, commits metadata to the remote metadata store, and only then acks the clients. The metadata commit is also where message ordering is defined: since any agent can write any partition, a partition's data is scattered across files with no inherent order, and the metadata store — leader for all topic partitions — sequences the batches at commit time. On read, it returns an ordered list of files and batches so consumers see correct order. The cost of all this buffering-plus-two-hops: P99 produce latency around 400ms, end-to-end producer-to-consumer P99 around 1 second. The founders' own pitch is explicit about the exchange — if you can tolerate ~1s P99, streaming costs drop 5–10x per GiB. You can buy latency back by shrinking the buffer time (more PUT requests, higher cost) or paying for S3 Express One.

Reads route through a consistent hashing ring: each agent owns a subset of data, agent A forwards the Fetch to responsible agent B, which asks the metadata store for the right files, loads ~16 MB chunks into an in-memory cache, and serves from memory afterward. A separate cache per AZ keeps fetches from crossing zonal boundaries. Historical reads of 4 MB or larger skip the cache and hit object storage directly. Background compaction inside the agents merges small files into uniform ones so replay workloads get sequential reads. Agents can also be role-split: proxy-produce, proxy-consume, or jobs.

Two honest caveats from the sources. Compatibility is not 100% — the new protocol means WarpStream must re-implement Kafka features, and transactions took quite some time to arrive. And the consistent-hashing cache assignment is, in effect, a fall back to leader-based ideas to recover data locality — leaderless writes fragment a partition across many small objects, forcing workarounds (like distributed mmap against S3 GET costs) that a leader-based design such as [[automq-wal-shared-storage]] avoids. Which philosophy wins depends on your workload: see [[diskless-kafka-trade-off-framework]].
