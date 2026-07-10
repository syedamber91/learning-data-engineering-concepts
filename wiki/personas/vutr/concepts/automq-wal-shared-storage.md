---
persona: vutr
kind: concept
sources:
- raw/kafka/how-do-we-run-kafka-100-on-the-object.md
- raw/kafka/how-automq-reduces-nearly-100-of.md
- raw/kafka/automq-achieving-auto-partition-reassignment.md
- raw/kafka/how-to-choose-the-right-diskless.md
last_updated: '2026-07-10'
qc: passed
slug: automq-wal-shared-storage
topics:
- kafka
---

Start with the misconception: [[tiered-storage-kip-405]] does not make a Kafka broker stateless. It offloads historical segments to remote storage, but the broker's local disk still receives the latest data — the coupling problem shrinks, it doesn't disappear. AutoMQ's question was different: can *all* of Kafka's data live in object storage while keeping local-disk-like performance? Their answer is to reuse Apache Kafka's code for computation and the protocol (100% compatibility, unlike WarpStream's protocol rewrite — see [[warpstream-stateless-agent-architecture]]) and replace only the storage layer with a shared-storage architecture built on three pieces: an off-heap memory cache, a small Write-Ahead Log, and object storage.

The write path is where the mechanism lives. Kafka hands persistence to the OS [[page-cache-sequential-io-and-zero-copy|page cache]]; AutoMQ implements its own cache instead. The broker places an incoming message into the **log cache** (off-heap, so the JVM doesn't garbage-collect it), then writes it to the WAL — a raw EBS device — using Direct I/O, bypassing the filesystem cache. Only when the message persists in the WAL does the broker acknowledge the producer. The upload to object storage happens asynchronously afterwards. Because the EBS volume is only a durability buffer, not the data store, it stays small: the default WAL size is 10GB.

The cache-to-WAL transfer runs through a `SlidingWindow` abstraction with three positions — Start Offset (everything before is written), Next Offset (where new records land), Max Offset (window end; reaching it triggers expansion). Records accumulate in a `currentBlock` (the smallest IO unit, aligned to 4 KiB on disk); when it hits a size or time limit, blocks move to `pendingBlocks`, then into `writingBlocks` as the IO thread pool frees up, and are removed once on disk.

The cache-to-S3 upload triggers when enough data accumulates, sorted by streamId and startOffset. Each object has three components: **DataBlocks** (the data, with each stream's data split into 1MB segments during upload so batch counts don't slow retrieval), an **IndexBlock** of 36-byte DataBlockIndex entries — one per DataBlock, sorted by (streamId, startOffset) for binary search — and a fixed 48-byte **Footer** pointing at the IndexBlock. Reads walk log cache → block cache (LRU-evicted, filled from S3 with prefetching and batch reading) → object storage; the log cache itself evicts first-in-first-out.

Recovery is what justifies calling the WAL "shared." If broker A crashes, its EBS volume is multi-attached to broker B, which identifies the orphan volume by tags, uses NVMe reservation to block unexpected writes, flushes the un-uploaded WAL data to S3, and deletes the volume. No replica catch-up — because object storage already guarantees durability, every partition has exactly one replica, dropping [[leader-follower-replication]] entirely. That statelessness is also why [[partition-reassignment-and-cluster-balancing|reassignment]] becomes a metadata-only edit in KRaft ([[zookeeper-to-kraft-metadata-management]]) rather than data movement.

The WAL is deliberately pluggable, and that's a trade-off decision, not a detail. **EBS WAL** gives low latency but leaves producer-to-leader cross-AZ traffic: Confluent observed cross-AZ transfer can exceed 50% of self-managed Kafka's infrastructure cost, and Vu's worked example — three r6i.large brokers at 30MiB/s write throughput — puts monthly cross-AZ cost at $4,050 against just $272 of VM cost, because multi-AZ Kafka generates at least (2/3 + 2)× the $0.01/GB unit price. **S3 WAL** attacks exactly that: the metadata request carries the producer's AZ, brokers are mapped across AZs by consistent hashing, and the producer is always handed a same-AZ broker — even one that doesn't own the partition. That broker buffers messages and, at 8MB or 250ms, writes them to S3 as a temporary file, then RPCs the real leader (a small residual cross-AZ cost), which reads the temp data back, appends it to the partition, and the ack chains back to the producer. Nearly 100% of cross-AZ cost disappears, but S3 WAL needs more VMs than EBS WAL — the extra S3 reads consume network bandwidth — and latency is worse. The decision rule from the sources: EBS WAL for latency-sensitive work (anti-fraud, financial transactions, real-time analysis); S3 WAL for log collection and observability ingestion. For where this sits among the other diskless designs, see [[diskless-kafka-trade-off-framework]].
