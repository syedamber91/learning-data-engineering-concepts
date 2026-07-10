---
persona: alex
kind: concept
sources:
- vutr/message-batching-and-compression
last_updated: '2026-07-10'
qc: passed
slug: message-batching-and-compression
topics:
- kafka
learner: alex
source_note: message-batching-and-compression
mastery: mastered
---

Wait, so let me see if I've got this. Batching is like carpooling for messages. If every kid took a separate car to school, that's a ton of trips clogging the road — same as firing one network request per message. So instead the producer runs a little waiting area: when I send a record, it doesn't leave right away, it gets serialized, sorted by which topic-partition it's going to, and dropped into a bucket with everyone else headed to that same destination. There's one worker filling the buckets and a *separate* worker who drives the full bucket to the broker — two different jobs so they don't block each other. And there are two rules for when a bucket leaves: either it's full (`batch.size`), or it's waited long enough (`linger.ms`) — whichever comes first. So the cost is that my message might sit in the waiting area for a bit, which is the latency price I pay for making fewer trips. The clever part is the broker side. Because a batch is one big chunk, the broker can append it to the file in one long smooth write instead of a bunch of tiny scattered pokes — and disks love long smooth writes. And compression: instead of shrinking each message alone, Kafka zips the *whole bucket* together, which packs tighter. Then — this is the bit I think is the real trick — the broker never unzips it. It keeps the exact same packed-up format from producer, to disk, to consumer, so it never has to unzip-and-rezip, and it can just fling the raw bytes to the consumer with `sendfile()`. And consumers pull batches too, so the carpool works in both directions.

*Source: [[message-batching-and-compression]] (vutr)*
