---
persona: vutr
kind: concept
sources:
- raw/kafka/apache-kafka-important-designs.md
- raw/kafka/if-youre-learning-kafka-this-article.md
- raw/kafka/how-do-we-run-kafka-100-on-the-object.md
- raw/kafka/stream-kafka-topic-to-the-iceberg.md
last_updated: '2026-07-10'
qc: passed
slug: page-cache-sequential-io-and-zero-copy
topics:
- kafka
---

Start with the obvious objection: "the disk is always slower than RAM, so isn't writing everything to the filesystem going to kill Kafka's performance?" The answer hinges on the access pattern. With random access, yes, disk loses to RAM — no argument. But with sequential access, disk can outperform memory slightly. Kafka's entire storage design is built to make both writes and reads sequential, and then to let the OS, not the JVM, do the caching.

## The page cache, not a Kafka cache

Modern operating systems borrow unused RAM for the page cache: frequently used disk data is populated into this cache so the system avoids touching the disk directly too often, mitigating disk-seek latency. If an application needs that memory, the kernel takes the pages back — so the cache never hurts the rest of the system.

Kafka deliberately does **not** build its own in-memory buffer of messages. Rather than keeping as much data as possible in JVM memory and flushing when RAM runs out, it hands everything to the OS, which moves all data through the page cache before flushing to disk. Every message write and read goes through the page cache. This buys two things:

1. **A simpler codebase** — the kernel handles the cache logic.
2. **Escape from JVM pain points** — Java objects carry high memory overhead, and garbage collection slows down as the number of in-heap objects grows. Keeping messages out of the heap sidesteps both.

## How writes and reads stay sequential

On the write side, each topic partition is a logical log implemented as segment files of roughly the same size (e.g., 1GB). The broker **appends** every incoming message to the single active segment; full segments are closed and a new one opened. Appending at the end of a file is, by construction, sequential I/O (see [[log-segments-and-offset-addressing]]).

On the read side, a consumer always consumes a partition sequentially. Messages have no message ID — only a logical offset — so there's no ID-to-location index to maintain; the consumer computes the next offset by adding the current message's length to its offset. Two index files (offset→position in segment, timestamp→offset) let the broker locate a segment quickly, and Kafka memory-maps these index files so it reads them as if they lived in memory. The pull loop itself is covered in [[pull-based-consumption-and-offset-commit]].

## Zero-copy: fewer copies, not no copies

The common misreading first: a zero-copy operation doesn't mean there are no data copies — it means no *unnecessary* copies. And Kafka didn't invent it; it leverages an existing OS technique.

The ordinary read-file-and-send-it-over-the-network flow copies data **four times with four context switches** between user and kernel mode: disk → page cache (switch to kernel mode), page cache → application buffer (switch back to user mode), application buffer → socket buffer (kernel mode again), socket buffer → NIC (back to user mode), then the NIC transmits.

With zero-copy — the `sendfile()` system call on Unix-based systems — data moves directly from one file descriptor to another without a round trip through user space. Kafka's flow collapses to: disk → page cache, page cache → network controller via `sendfile()`, NIC → consumer. Context switches drop **from four to two**, and the data never has to be copied into the Kafka application at all. Better still, data lands in the page cache exactly once and is reused for every subsequent read instead of being copied out to user space each time.

One precondition makes this work: Kafka keeps the on-disk data format identical from producer to broker to consumer. The same message format end to end is what lets `sendfile()` ship bytes untouched, and it avoids decompressing and recompressing messages (which is also why batching and compression compose cleanly — see [[message-batching-and-compression]]).

## The trade-off this design bakes in

Relying on the page cache means the storage layer *is* the broker's local machine: compute and storage are tightly coupled, so scaling storage always means adding machines — more CPU and RAM you may not need. That was a sound bet when networks were slow and local data centers were the norm, but in the cloud it blocks pay-as-you-go scaling and racks up cross-AZ replication costs. That tension is exactly what [[tiered-storage-kip-405]], [[automq-wal-shared-storage]], and the broader [[diskless-kafka-trade-off-framework]] set out to resolve — AutoMQ, notably, replaces the page-cache dependence with its own off-heap log/block caches plus a WAL precisely because the original design leaves the OS in charge.
