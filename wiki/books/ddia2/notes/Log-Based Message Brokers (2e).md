---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
topic: Transmitting Event Streams
type: subtopic
tags: [ddia2, kafka, offset, partition, log-compaction, tiered-storage, ring-buffer]
sources:
  - raw/ch12.md
---
# Log-Based Message Brokers
> Combine a database's durable storage with messaging's low-latency notification. Reading a message doesn't delete it, so you can replay.

## The Idea
**Sending a packet or making a request is normally a transient operation leaving no permanent trace, and AMQP/JMS-style brokers inherited this transient mindset** — **even when they write to disk, they quickly delete messages after delivery.** **Databases and filesystems take the opposite approach: everything written is expected to be permanently recorded until someone explicitly deletes it.**

**This difference has a big impact on how derived data is created.** **A key feature of batch processes is that you can run them repeatedly, experimenting with the steps, without risk of damaging the read-only input.** **This is not the case with AMQP/JMS messaging: receiving a message is destructive if the acknowledgment deletes it, so you cannot run the same consumer again and expect the same result.** **Add a new consumer and it typically receives only messages sent after registration; prior messages are gone and cannot be recovered** — **contrast files and databases, where a new client can read data written arbitrarily far in the past.**

**Why can we not have a hybrid, combining the durable storage of databases with the low-latency notification of messaging? That is the idea behind log-based message brokers.**

## How It Works
**A log is simply an append-only sequence of records on disk.** **A producer sends a message by appending it to the end of the log; a consumer receives messages by reading sequentially, and on reaching the end waits for notification of a new append.** **The Unix tool `tail -f` essentially works like this.**

**To scale beyond a single disk, the log can be sharded**, with **different shards on different machines, each a separate log read and written independently**, and **a topic defined as a group of shards carrying messages of the same type.**

**Within each shard — which Kafka calls a partition — the broker assigns a monotonically increasing sequence number, or offset, to every message.** **This makes sense because a partition is append-only, so messages within it are totally ordered.** **There is no ordering guarantee across different partitions.**

**Apache Kafka and Amazon Kinesis Streams work this way; Google Cloud Pub/Sub is architecturally similar but exposes a JMS-style API rather than a log abstraction.** **Even though these brokers write all messages to disk, they achieve throughput of millions of messages per second by sharding across machines, and fault tolerance by replicating messages.**

**Logs compared to traditional messaging.** **The log-based approach trivially supports fan-out, because several consumers can independently read the log without affecting one another — reading does not delete.** **To load balance across a consumer group, the broker assigns entire shards to nodes rather than individual messages to clients**, and **each client then consumes all messages in its assigned shards, typically sequentially and single-threaded.**

**This coarse-grained load balancing has downsides:**
- **The number of nodes sharing the work can be at most the number of log shards in the topic**, since messages in a shard go to the same node. (**You could have two consumers split a shard by even and odd offsets, or use a thread pool — but that complicates offset management. In general single-threaded processing of a shard is preferable, and parallelism increases by using more shards.**)
- **If a single message is slow to process, it holds up subsequent messages in that shard — head-of-line blocking.**

**So: when messages are expensive to process, you want message-by-message parallelism, and ordering is not important, the JMS/AMQP style is preferable.** **In situations with high throughput, where each message is fast to process and ordering is important, the log-based approach works very well.** **The distinction is blurring, though, since Kafka now supports JMS/AMQP-style consumer groups allowing multiple consumers to receive from the same partition.**

**Since sharded logs preserve ordering only within a shard, all messages needing consistent ordering must be routed to the same shard.** **If events for one user must appear in a fixed order, choose the shard based on the user ID — making the user ID the partition key.**

**Consumer offsets.** **Consuming a shard sequentially makes it easy to tell which messages have been processed**: everything below the current offset is done, everything above is unseen. **So the broker needn't track acknowledgments for every message, only periodically record consumer offsets** — **and the reduced bookkeeping plus opportunities for batching and pipelining help increase throughput.** **If a consumer fails, it resumes from the last recorded offset rather than the last offset it actually saw, so it may see some messages twice.**

**The offset is very similar to the log sequence number in single-leader database replication**, which lets a follower reconnect and resume without skipping writes. **Exactly the same principle: the broker behaves like a leader database and the consumer like a follower.** **If a consumer node fails, another node in the group takes its shards and starts at the last recorded offset** — **so messages processed but whose offsets weren't recorded are processed a second time.**

## Trade-offs & Pitfalls
**Disk space usage.** **If you only ever append, you eventually run out of disk.** **To reclaim space, the log is divided into segments and old segments are periodically deleted or archived.** **So if a slow consumer falls so far behind that its offset points to a deleted segment, it will miss messages** — **effectively the log implements a bounded-size buffer discarding old messages when full, a circular or ring buffer.** **But since that buffer is on disk it can be quite large.**

**The back-of-the-envelope:** a typical large hard drive has **20 TB capacity and 250 MB/s sequential write throughput**, so **writing at the fastest possible rate it takes about 22 hours to fill and start deleting.** **So a disk-based log can always buffer at least 22 hours' worth of messages**, even across many disks and machines. **In practice deployments rarely use the full write bandwidth, so the log can typically keep several days' or even weeks' worth.**

**Many log brokers now store messages in object storage to increase capacity.** **Kafka and Redpanda serve older messages from object storage as tiered storage; WarpStream, Confluent Freight, and Bufstream store all their data there.** **Besides cost efficiency, this makes data integration easier: messages in object storage are stored as Iceberg tables, enabling batch and data warehouse jobs to execute directly on the data without copying it into another system.**

**When consumers cannot keep up.** In the drop/buffer/backpressure taxonomy, **the log-based approach is buffering with a large but fixed-size buffer limited by available disk space.** **If a consumer falls behind the retained window it cannot read those messages — so the broker effectively drops old messages beyond the buffer size.** **You can monitor how far a consumer is behind the head of the log.**

## Examples & Systems
Apache Kafka, Amazon Kinesis Streams, Google Cloud Pub/Sub; Kafka and Redpanda tiered storage; WarpStream, Confluent Freight, Bufstream storing everything in object storage as Iceberg tables.

## Since the 1st Edition
The 1st edition's [[Log-Based Message Brokers]] covered the same log structure, partitions and offsets, the fan-out and coarse load-balancing comparison, consumer offsets as replication log sequence numbers, and the ring-buffer disk-space calculation. **New: tiered and object-storage-backed log brokers** — Kafka and Redpanda serving old messages from object stores, and **WarpStream, Confluent Freight, and Bufstream storing everything there as Iceberg tables**, which makes the same data readable by batch and warehouse jobs. **Also new:** the note that **Kafka now supports JMS/AMQP-style consumer groups**, blurring the distinction the subtopic is built around.

## Related
- up: [[Transmitting Event Streams (2e)]] · chapter: [[Ch 12 - Stream Processing (2e)]]
- [[Messaging Systems (2e)]] — the transient alternative
- [[Change Data Capture (2e)]] — what log brokers are used to transport
- [[The Many Faces of Consensus (2e)]] — shared logs as consensus
- 1st edition: [[Log-Based Message Brokers]] — the same subtopic
