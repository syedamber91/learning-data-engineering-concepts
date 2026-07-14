---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
topic: Databases and Streams
type: subtopic
tags: [ddia, dual-writes, data-integration, race-conditions]
sources:
  - raw/ch11.md
---
# Keeping Systems in Sync
> Real applications spread data across databases, caches, indexes, and warehouses — and naive "dual writes" to keep them consistent are a trap.

## The Idea
No single storage system serves every need, so an application typically pairs an OLTP database with a cache, a full-text search index, and a warehouse for analytics (see [[Data Warehousing]]). Each holds its own copy of the data, optimized differently, and every copy must reflect the same updates. Warehouses are usually synced by batch ETL dumps; when that's too slow, teams reach for dual writes — and get burned.

## How It Works
**Dual writes**: application code writes each change to every system itself (database, then index, then cache invalidation). Nothing coordinates these writes, which creates two failure modes:
1. **Race condition** — two clients update the same item concurrently; the database applies client 1 then client 2, the index applies client 2 then client 1. Both systems finish in a *permanently inconsistent* state with no error raised. Detecting this needs concurrency machinery like [[Version Vectors]] (see [[Detecting Concurrent Writes]]).
2. **Partial failure** — one write succeeds while the other fails, again diverging the copies. Making both succeed or both fail is the atomic commit problem ([[Atomic Commit and Two-Phase Commit (2PC)]]), which is expensive.

The root cause: each system has its own leader with nobody following anybody, exactly the conflict setup of [[Multi-Leader Replication]]. Within one replicated database, a single leader fixes ordering; the cure here is the same — make the database the sole leader and turn the search index, cache, and warehouse into followers of its change stream.

## Trade-offs & Pitfalls
Full-dump ETL is simple and consistent but slow to reflect changes. Dual writes are timely but silently corruptible — avoid them unless you add real concurrency control. The follower approach requires the database to expose its changes, which historically it didn't; that gap is what [[Change Data Capture]] fills.

## Examples & Systems
OLTP database + Redis-style cache + Elasticsearch-style index + warehouse is the canonical heterogeneous stack. Batch pipelines building indexes were covered in [[The Output of Batch Workflows]].

## Related
- up: [[Databases and Streams]] · chapter: [[Ch 11 - Stream Processing]]
- [[Change Data Capture]] — the stream-based fix for dual-write drift
- [[Multi-Leader Replication]] — why independent leaders conflict
- [[Total Order Broadcast]] — state machine replication needs one agreed order
