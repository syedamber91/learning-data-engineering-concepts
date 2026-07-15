---
persona: vutr
kind: concept
sources:
- raw/kafka/deep-dive-into-the-challenges-of.md
last_updated: '2026-07-15'
qc: passed
slug: automq-traffic-tiering-and-rate-limiting
topics:
- kafka
---

A classic Kafka broker gets to offload most storage work to the OS — the page cache and the filesystem handle it ([[page-cache-sequential-io-and-zero-copy]]). A stateless AutoMQ broker doesn't get that luxury: it has to buffer data in memory, upload it to object storage, compact it, and parse it back out, all itself. Left unmanaged, that extra work competes for the same limited network bandwidth as ordinary produce and consume traffic — a compaction job, for instance, can slow down the regular writes it's supposed to be running alongside.

AutoMQ's fix is to name and rank the traffic types instead of treating bandwidth as one undifferentiated pool. It identifies five kinds of network traffic: message-sending traffic (producer → AutoMQ → S3), tail-read consumption traffic (AutoMQ → consumer, i.e. reading recent data), historical consumption traffic (S3 → AutoMQ → consumer), compaction read traffic (S3 → AutoMQ), and compaction upload traffic (AutoMQ → S3). It then collapses these into four priority tiers: Tier-0 is message-sending traffic; Tier-1 is catch-up read consumption; Tier-2 is compaction read/write traffic; Tier-3 is chasing read consumption traffic.

The enforcement mechanism is an asynchronous multi-tier rate limiter combining a priority queue with a token bucket — a rate-limiting scheme that periodically refills a bucket with tokens, where each token permits one request to proceed, and an empty bucket means new requests get delayed or dropped rather than allowed to overload the system. Tier-0 requests are exempt from this control entirely — message-sending traffic is never throttled. Tier-1 through Tier-3 requests, by contrast, get queued by priority whenever available tokens run out; as the token bucket refills on its periodic schedule, a callback thread wakes up and works through the queue, serving the highest-priority waiting requests first.

The upshot is a deliberate hierarchy of who gets to starve whom: producers writing new data are protected unconditionally, catch-up reads come next, and the broker's own background housekeeping — compaction, and reads chasing far behind the log's head — are the ones held back when bandwidth runs short.

*See also: [[automq-wal-shared-storage]] · [[automq-object-batching-and-compaction]] · [[page-cache-sequential-io-and-zero-copy]]*
