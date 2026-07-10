# Alex's open questions

Things the wiki didn't answer, and claims to double-check.

## log-segments-and-offset-addressing (2026-07-10)
- wiki gap: The next offset is current offset + current message's length, so there are 'holes' between valid offsets. What happens if a consumer asks the broker to start at an offset that lands in one of those holes — in the middle of a message? Does the broker snap to the nearest real message, or does the fetch just fail?

## page-cache-sequential-io-and-zero-copy (2026-07-10)
- wiki gap: If Kafka never keeps messages in its own memory and just trusts the page cache, what happens the moment a consumer asks for old messages that have already been evicted from the cache because the kernel reclaimed that RAM — does the broker just eat a slow random disk seek, and doesn't that break the 'everything is sequential/fast' promise?
- wiki gap: You said zero-copy works because the on-disk format is identical end to end and the bytes never enter Kafka's application memory — but if the bytes never pass through Kafka, how can the broker do anything that needs to actually look inside a message on the read path, like filtering or transforming it, without giving up sendfile()?

## message-batching-and-compression (2026-07-10)
- wiki gap: If the broker never unzips a compressed batch to look inside it, how does it assign or track offsets for the individual messages in that batch — doesn't it need to see them one by one to number them?
- wiki gap: With the Sticky Partitioner cramming records into one partition until the batch fills, doesn't that mean the *last* partition it's currently sticking to gets all the fresh data while others go quiet for a moment — could that make some partitions lopsided, and why doesn't that hurt?

## message-key-partitioning-strategies (2026-07-10)
- wiki gap: The same-key-same-partition guarantee gives me ordering — but what happens to that guarantee if I later add more partitions to the topic? Wouldn't the hash suddenly send an existing key somewhere new and break the ordering for that entity?

## consumer-groups-and-partition-assignment (2026-07-10)
- wiki gap: Why does Kafka deliberately wait a few seconds before declaring a silent consumer dead, instead of rebalancing the moment one heartbeat is missed?
- wiki gap: Why is Range the default assignment strategy rather than Round Robin?

## leader-follower-replication (2026-07-10)
- wiki gap: When the leader dies and a follower takes over, how does Kafka know that follower actually caught up? If the leader crashed halfway through replicating a message, couldn't the new leader be missing messages the producer thinks were saved?

## partition-reassignment-and-cluster-balancing (2026-07-10)
- wiki gap: Northguard adds a broker with zero movement by pointing the next active segment at it — but all the old segments still live on the old brokers. Doesn't the cluster stay unbalanced for reads of old data? Does old data ever get moved off a hot broker, or does it just age out?

## zookeeper-to-kraft-metadata-management (2026-07-10)
- wiki gap: What is the exact behavior of in-flight metadata writes during the window after a controller quorum leader dies and before Raft elects a new one — are they rejected, queued, or retried?
- wiki gap: Does the separate internal Kafka topic that carries load metrics itself depend on KRaft-managed partition/broker mappings, and if so how is that potential circular dependency bootstrapped or resolved?

## automq-wal-shared-storage (2026-07-10)
- wiki gap: You said the producer gets its ack the moment the message hits the WAL, and the upload to S3 happens asynchronously afterwards. But the WAL is only 10GB. If S3 uploads fall behind while producers keep blasting data and the WAL fills up, what happens — does the broker stop acking producers, or does it start dropping data?
- unverified (not in vutr wiki): The off-heap cache exists so the garbage collector 'never pauses things' — the note says off-heap memory is not garbage-collected by the JVM, but never states GC pauses as the motivation.
- unverified (not in vutr wiki): 'S3 uploads happen later, in batches' being slow relative to WAL writes — the note says upload triggers when enough data accumulates, but does not characterize upload speed.

## diskless-kafka-trade-off-framework (2026-07-10)
- wiki gap: WarpStream and Bufstream both wait for object storage before acking, but Bufstream's p99 is 500ms while WarpStream's end-to-end p99 is ~1s — almost double. If they're using the same 'wait for S3' strategy, where does WarpStream's extra latency actually come from?

## kafka-iceberg-zero-etl (2026-07-10)
- wiki gap: You said the Coordinator sits on partition 0 and centralizes all the commits so workers don't conflict — but if it's a single point funneling every commit, doesn't that partition-0 Coordinator become a bottleneck (or a single point of failure) when the topic has a huge number of partitions all trying to commit at once?
- wiki gap: For Bufstream's single-copy trick, consumers are served 'row by row' from the same Iceberg table — but Iceberg is a batch/columnar format that only becomes visible once the metadata pointer flips after manifests are written. So how does a live consumer poll for a brand-new message that's still sitting in an intake file and hasn't been committed to Iceberg yet — wouldn't it either not see it or have to wait for the whole batch?

## zero-downtime-migration-dual-write (2026-07-10)
- wiki gap: During the producer phase, everything a migrated producer sends to AutoMQ is forwarded back to Kafka, but the Fetcher is also pulling from Kafka into AutoMQ — what stops that forwarded message from being immediately re-fetched back into AutoMQ, creating a loop or duplicate?

## northguard-segment-level-replication (2026-07-10)
- wiki gap: A segment can be sealed early because it 'fails to replicate' — but if replication is failing, how does the new segment you open right after it succeed at replicating? What's different about the next one, versus just hitting the same failure again?

## linkedin-multi-tier-clusters-and-audit (2026-07-10)
- wiki gap: The audit counts themselves are just Kafka messages published into an auditing topic — if the pipeline is dropping messages, what stops it from dropping the audit-count messages too, so the books balance even though data was lost?
