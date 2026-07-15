---
persona: vutr
kind: concept
sources:
- raw/kafka/the-company-that-created-kafka-is.md
last_updated: '2026-07-10'
qc: passed
slug: northguard-segment-level-replication
topics:
- kafka
---

The reflex is to assume Kafka's partition is the natural unit of replication — it's the log, so of course you copy the whole log. LinkedIn, the company that created Kafka fifteen years ago, concluded the opposite: at their scale, partition-level replication is exactly what makes the system hard to operate. Their replacement, Northguard, replicates **segments** instead, and that one change in granularity drives almost everything else about its design.

First, the scale that forced the decision. By 2025 LinkedIn had over 1.2 billion users, and its Kafka footprint was 150 clusters on 10,000 machines serving 400,000 topics with 17PB of data daily. Kafka's tightly coupled architecture means scaling traffic means adding machines — but because each replica must store the entire copy of a whole partition (see [[leader-follower-replication]]), two operational problems compound at that size:

- A new broker added to a Kafka cluster is not automatically load-balanced into. It sits idle and underutilized until someone creates new topics or partitions, or manually rebalances — and manual data movement is ineffective ([[partition-reassignment-and-cluster-balancing]]).
- A broker holding hot partitions (intensive data ingestion) gets overloaded, and fixing that requires re-partitioning data.

LinkedIn wanted higher scalability and more even load distribution, plus strong consistency in data *and* metadata, without giving up Kafka's high throughput, low latency, availability, and durability. Northguard's answer: break data and metadata into smaller chunks and distribute them evenly by design.

The data model makes the mechanism concrete. A record (key, value, optional headers) is appended to a **segment** — a 1GB file, as in Kafka ([[log-segments-and-offset-addressing]]). An active segment is sealed when it hits max size, has been active for more than 1 hour, or fails to replicate. Segments chain into a **range**, Northguard's log abstraction, which covers a contiguous span of keys (A→D, D→M, M→Q); a **topic** is the set of ranges covering the whole keyspace (A→Z). Ranges can be split (seal the source, create two new ranges) or merged (seal both sources, create one). Storage policies carry a retention period plus constraints, and because brokers are deployed with encoded rack/data-center information, those constraints give rack-aware replica placement.

Now the payoff of replicating segments rather than partitions: segments are created far more frequently than logs. When a broker is buckling under write pressure, Northguard doesn't move an existing partition to a new broker the way Kafka must — it simply assigns the **next active segment** to the new broker, and ingest traffic routes there immediately, relieving the struggling node. And because segments are smaller than Kafka's partitions, any data that does need to move is cheaper to move. Fewer clients are affected by rebalancing, and load spreads without the availability hit Kafka takes when cluster membership changes.

Metadata gets the same decentralizing treatment. Instead of a controller ([[zookeeper-to-kraft-metadata-management]]), Northguard runs Raft-backed replicated state machines across vnodes, sharding topic metadata by topic name and range/segment metadata by range ID via consistent hashing — eliminating Kafka's controller bottlenecks. The protocol differs too: metadata is request-response to any broker (which routes to the right vnode), while data operations are sessionized streaming. Producers handshake with the active segment leader, get a window size, and receive ACKs only when records are committed on all replicas; consumers get data **pushed** within a client-declared budget — the reverse of Kafka's pull model ([[pull-based-consumption-and-offset-commit]]). Storage is pluggable: the default writes a per-segment WAL with Direct I/O (skipping the page-cache copy Kafka's write path pays — contrast [[page-cache-sequential-io-and-zero-copy]]) plus a sparse index in RocksDB and application-level caching.

The trade-off is brutal honesty about compatibility. Most Kafka alternatives keep the Kafka protocol non-negotiable and swap in object storage ([[diskless-kafka-trade-off-framework]], [[warpstream-stateless-agent-architecture]]); LinkedIn concluded the Kafka protocol couldn't deliver their goals, kept local disk for latency, and paid for it with a hard migration — Xinfra, a virtualized Pub/Sub layer over both systems, using dual writes with producers migrated before consumers ([[zero-downtime-migration-dual-write]]). Northguard wins load balancing; it loses the ecosystem. That's why it likely won't replace Kafka outside LinkedIn — few companies have LinkedIn's latency and throughput requirements, or its resources.

## Related in the other wiki
- [[Implementation of Replication Logs]] — DDIA catalogs the wire formats a replication log can take (WAL shipping, logical logs, etc.); Northguard's redesign shows a real system choosing the unit of replication (segment vs. whole partition) as an equally consequential design axis.
- [[Replication]] — DDIA's Replication concept lays out why keeping copies in sync is hard in general; Northguard is a real-world redesign of that sync mechanism at finer (segment) granularity to fix Kafka's operational problems at LinkedIn scale.
