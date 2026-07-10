---
persona: vutr
kind: concept
sources:
- raw/kafka/how-to-choose-the-right-diskless.md
- raw/kafka/how-automq-reduces-nearly-100-of.md
- raw/kafka/bufstream-stream-kafka-messages-to.md
- raw/kafka/i-spent-8-hours-researching-warpstream.md
last_updated: '2026-07-10'
qc: passed
slug: diskless-kafka-trade-off-framework
topics:
- kafka
---

Start with the misconception: "diskless Kafka" is not one product category where every vendor made the same choices, and it is not [[tiered-storage-kip-405]] under a new name. Tiered storage keeps hot data on the broker's local disk, so brokers stay stateful and every cloud problem — coupled compute/storage scaling, cross-AZ replication fees — is still present. Diskless means all messages move off the brokers entirely into object storage, and once you accept that, a set of trade-offs opens up on which WarpStream, Bufstream, and AutoMQ each landed differently.

First, why the shift at all. Kafka's design — [[leader-follower-replication]] over local disks — was built for on-prem data centers. In a three-AZ cloud deployment, producers hit a leader in another zone roughly two-thirds of the time, and the leader then replicates to followers in the other two AZs, so multi-AZ Kafka generates at least (2/3 + 2) times the unit price of cross-AZ traffic ($0.01/GB on AWS, ingress and egress charged separately). Confluent's observation: cross-AZ transfer can exceed 50% of the total infrastructure bill. Vu's worked example: three r6i.large brokers at 30MiB/s cost ~$272/month in VMs but ~$4,050/month in cross-AZ traffic. Object storage flips this — durability (eleven nines, via erasure coding and multi-AZ replication) is handled by the storage layer, so broker-level replication and its traffic disappear, and brokers become stateless compute that scales independently of storage. Bufstream's benchmark makes it concrete: 1 GiB/s with 7-day retention costs $42,025/month in Kafka EBS volumes vs $4,625 in Bufstream storage, and $34,732/month in Kafka cross-AZ fees vs $226 (metadata only).

The trade-offs, then:

**Latency vs cost.** Writing to object storage is slower than disk. WarpStream and Bufstream ack the producer only after the batch (buffered ~250ms or 8MiB) lands in object storage and metadata is committed — WarpStream's produce p99 is ~400ms and end-to-end p99 ~1s; Bufstream's median end-to-end is 260ms, p99 500ms. The tuning knob is the buffer: shorter buffer, lower latency, but more PUT requests and higher cost. AutoMQ refuses this trade — its [[automq-wal-shared-storage]] acks once the message persists in a small (default 10GB) WAL on a disk service like EBS/FSx, then flushes to object storage asynchronously. Even AutoMQ exposes the same dial internally: EBS WAL for latency-sensitive work (anti-fraud, finance), S3 WAL — which needs more VMs because reading temp files from S3 eats network bandwidth — for log collection where latency doesn't matter.

**Protocol reimplementation vs codebase reuse.** WarpStream and Bufstream built new engines that speak the Kafka protocol; the cost is keeping up with the community — WarpStream took quite some time to support transactions. AutoMQ reuses Kafka's code and swaps only the storage layer, which is why it can claim 100% compatibility and, currently, the only open-source production-ready diskless option (the Diskless Topics KIP is still under discussion).

**Leader-based vs leaderless.** Leaderless ([[warpstream-stateless-agent-architecture]], Bufstream) lets any broker take any write, so same-AZ routing is trivial — but it demands an external coordinator to re-implement what partition leaders did, fragments a partition's data across small objects written by many brokers (low data locality, more S3 GETs), and forces per-batch metadata in a separate transactional store (DynamoDB/Spanner/etcd/Postgres). WarpStream's consistent-hashing cache assignment effectively falls back to the leader idea, with extra complexity. AutoMQ keeps leaders and KRaft metadata (size independent of batch count), and solves same-AZ writes differently: a same-zone broker writes temp files to shared object storage, RPCs the real leader, and the leader appends them to the partition — nearly 100% of cross-AZ cost gone, minus small RPC traffic. See [[producer-send-path-and-acks]] for the baseline path being modified.

**Deployment and sovereignty.** WarpStream's BYOC keeps data in your VPC but routes metadata to WarpStream Cloud; Bufstream runs entirely in your VPC (Kubernetes + object storage + a metadata store), sends nothing back to Buf, and adds broker-side value on top — [[broker-side-schema-and-semantic-validation]] and [[kafka-iceberg-zero-etl]].

The money framing: Stanislav Kozlovski's 256 MiB/s comparison — Kafka $1,077,922, optimized Kafka $554,958, Bufstream $128,136 (at $0.002 per uncompressed GiB written). The framework is not "which is cheapest" but which trade you can afford: if your workload tolerates ~1s p99, diskless cuts streaming cost 5–10x per GiB; if it can't, you need a WAL-style design that pays for lower latency with a leader-based, disk-touching path.
