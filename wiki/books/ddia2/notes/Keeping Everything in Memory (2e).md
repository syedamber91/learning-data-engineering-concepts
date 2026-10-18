---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
topic: Storage and Indexing for OLTP
type: subtopic
tags: [ddia2, in-memory-database, redis, voltdb, durability]
sources:
  - raw/ch04.md
---
# Keeping Everything in Memory
> In-memory databases are not fast because they avoid reading from disk. They're fast because they avoid *encoding* data for disk.

## The Idea
Every data structure in the chapter so far is an answer to the limitations of disks. Compared to main memory, disks are awkward: with both magnetic disks and SSDs, data must be laid out carefully for good read and write performance. We tolerate that awkwardness because disks are **durable** (contents survive power loss) and have a **lower cost per gigabyte** than RAM.

As RAM gets cheaper the cost-per-gigabyte argument erodes. Many datasets simply aren't that big, so keeping them entirely in memory — potentially spread across several machines — is quite feasible. Hence **in-memory databases**.

## How It Works
- Some in-memory key-value stores such as **Memcached** are intended for caching only, where losing data on restart is acceptable. Others aim for **durability**, achieved with special hardware (battery-powered RAM) or, more commonly, by writing a log of changes to disk, writing periodic snapshots, or replicating the in-memory state to other machines. That lets the database reload its state from disk or over the network from a replica on restart.
- Despite writing to disk, these are still in-memory databases, because **the disk is merely an append-only log for durability and reads are served entirely from memory**. Writing to disk also has operational advantages: files can be backed up, inspected, and analysed by external utilities.
- **VoltDB, SingleStore, and Oracle TimesTen** are in-memory databases with a relational model whose vendors claim big performance improvements from removing the overheads of managing on-disk data structures. **RAMCloud** is an open source in-memory key-value store with durability, using a log-structured approach for both memory and disk. **Redis and Couchbase** provide weak durability by writing to disk asynchronously.

## Trade-offs & Pitfalls
- **The performance advantage is counterintuitive.** It is *not* that they avoid reading from disk — even a disk-based engine may never read from disk if you have enough memory, because the operating system caches recently used blocks anyway. They are faster because they **avoid the overheads of encoding in-memory data structures into a form that can be written to disk**.
- **The other reason to use one is expressiveness, not speed.** In-memory databases can provide data models that are difficult to implement with disk-based indexes. Redis offers a database-like interface to structures such as priority queues and sets, and its implementation is comparatively simple precisely because everything is in memory.

## Examples & Systems
Memcached (cache only); VoltDB, SingleStore, Oracle TimesTen (relational, in-memory); RAMCloud (durable, log-structured); Redis and Couchbase (weak durability, rich data structures).

## Since the 1st Edition
Close to the 1st edition's treatment inside [[Other Indexing Structures]], including the same counterintuitive-performance explanation and the same system roster. It is promoted to a subtopic of its own here. The 1st edition also speculated about anti-caching and non-volatile memory as future directions; the 2nd edition drops that, and instead the single-node-engine argument has moved up to [[Distributed Versus Single-Node Systems (2e)]] in Chapter 1.

## Related
- up: [[Storage and Indexing for OLTP (2e)]] · chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Distributed Versus Single-Node Systems (2e)]] — the wider case for not distributing
- [[Actual Serial Execution (2e)]] — the transaction model in-memory databases enable
- 1st edition: [[Other Indexing Structures]] — where this material used to live
