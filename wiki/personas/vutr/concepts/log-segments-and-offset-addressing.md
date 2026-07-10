---
persona: vutr
kind: concept
sources:
- raw/kafka/apache-kafka-part-1-overview.md
- raw/kafka/apache-kafka-important-designs.md
- raw/kafka/if-youre-learning-kafka-this-article.md
- raw/kafka/automq-achieving-auto-partition-reassignment.md
last_updated: '2026-07-10'
qc: passed
slug: log-segments-and-offset-addressing
topics:
- kafka
---

Start with the misconception: a message stored in Kafka does **not** have an explicit message ID. If you come from the database world expecting every record to carry an identifier that some index maps to a physical location, Kafka deliberately refuses to pay for that. Each message is addressed by its **logical offset** instead. This avoids the overhead of maintaining index structures that map message IDs to the actual message locations — a real cost at the throughput Kafka was built for at LinkedIn. The trade-off: offsets are increasing but **not consecutive**, so to compute the offset of the following message, the consumer has to add the length of the current message to the current offset — the same way an array data structure handles random access.

Here is the physical layout that makes this work. Messages are organized into topics (think tables), and a topic is split into multiple partitions. **Each partition corresponds to one logical log.** Physically, that log is implemented as a set of **segment files of approximately the same size (e.g., 1GB)**. The write path is strict about this:

1. A producer publishes a message to a partition. The broker receives it, assigns the offset, and writes it to disk.
2. The broker ***appends*** the message to the **last (active) segment file**. At any point, only one active segment file accepts writes.
3. When a segment file reaches the size limit, it is closed, and Kafka opens a new segment file for subsequent writes.

Appending at the end of the segment file is what guarantees that data writing in Kafka happens sequentially — the mechanical foundation for the page-cache and sequential-I/O story in [[page-cache-sequential-io-and-zero-copy]]. It also composes with batching: instead of appending messages one by one, the broker appends a chunk of messages at once, achieving larger sequential disk operations ([[message-batching-and-compression]]).

Reading is where offset addressing earns its keep. "No message ID" does not mean "no index at all" — the correction is that Kafka indexes *offsets*, not IDs. Besides the log files containing actual data, brokers keep **two additional index files** per partition:

- The first index **maps offsets to segment files and positions within the file**, so the broker can quickly find the message for a given offset.
- The second **maps timestamps to message offsets**, used when searching for messages by timestamp.

Kafka uses **memory-mapped file** techniques for these index files, which lets the broker read them as if they were located directly in memory.

The full fetch mechanism, step by step: the consumer initially requests the broker with the **start offset** at which it wants to begin consuming. The broker uses that offset to search the index file, locates the segment file holding the requested message, seeks to the position, and sends the data back. After receiving a message, the consumer computes the offset of the following message (current offset + current message's length) and uses it in the subsequent pull request. Consumption from a partition is therefore always sequential, and acknowledging a particular offset implies the consumer has received **all** messages before that offset in the partition — the contract that [[pull-based-consumption-and-offset-commit]] builds on.

One more design consequence hides here: the Kafka data format on disk is kept the same throughout — from when the producer sends it to when the broker ships it to the consumer. Because a segment's bytes are exactly what goes out on the wire, the broker can use zero-copy transfer efficiently and avoid decompressing and recompressing messages.

Know the limits of this design, too. Segment files live on the broker's local disk, which couples compute and storage: scaling storage always requires adding more machines, and moving a partition means physically moving its segment data between brokers ([[partition-reassignment-and-cluster-balancing]]). That coupling is exactly what tiered storage ([[tiered-storage-kip-405]]) — recent segments on local disk, historical data in HDFS/S3/GCS — and shared-storage rewrites like [[automq-wal-shared-storage]] attack, while keeping the same logical-log, offset-addressed contract intact. The core abstraction — an append-only log of offset-addressed messages in fixed-size segments — has remained the same since day one; what keeps changing is where those bytes physically live.
