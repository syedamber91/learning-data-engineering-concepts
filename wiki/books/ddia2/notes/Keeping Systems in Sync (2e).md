---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
topic: Databases and Streams
type: subtopic
tags: [ddia2, dual-writes, race-condition, atomic-commit, derived-data]
sources:
  - raw/ch12.md
---
# Keeping Systems in Sync
> Two clients, two systems, unlucky timing, no error — and permanent inconsistency. Dual writes cannot be made safe by being careful.

## The Idea
**No single system can satisfy all data storage, querying, and processing needs.** **Most nontrivial applications combine several technologies**: an OLTP database serving user requests, a cache speeding up common requests, a full-text index for search, a data warehouse for analytics. **Each has its own copy of the data in its own representation, optimized for its own purposes.**

**As the same or related data appears in several places, they must be kept in sync.** **Update an item in the database and it must also be updated in the cache, search indexes, and warehouse.** **With warehouses this is usually done by ETL — taking a full copy, transforming it, and bulk-loading it — in other words, a batch process.**

**If periodic full dumps are too slow, an alternative sometimes used is dual writes**: **application code explicitly writes to each system when data changes** — first the database, then the search index, then invalidating cache entries, **or performing those writes concurrently.**

## How It Works
**Dual writes have serious problems.**

**The race condition.** **Two clients concurrently want to update item X: client 1 sets it to A, client 2 sets it to B.** **Both write the new value to the database, then to the search index.** **Because of unlucky timing the requests interleave: the database sees client 1's A then client 2's B, so its final value is B; the search index sees client 2 first then client 1, so its final value is A.** **The two systems are now permanently inconsistent with each other, even though no error occurred.**

**Unless you have an additional concurrency detection mechanism such as version vectors, you will not even notice that concurrent writes occurred — one value simply silently overwrites another.**

**Partial failure.** **One of the writes may fail while the other succeeds.** **This is a fault-tolerance problem rather than a concurrency problem, but also leaves the two systems inconsistent.** **Ensuring both succeed or both fail is the atomic commit problem, which is expensive to solve.**

## Trade-offs & Pitfalls
**The diagnosis is precise, and it's a multi-leader problem.** **With one replicated database and a single leader, that leader determines the order of writes, so state machine replication works among its replicas.** **But in the dual-writes scenario there isn't a single leader: the database may have a leader and the search index may have a leader, but neither follows the other, so conflicts can occur.**

**The situation would be better if there really was only one leader — the database — and if we could make the search index a follower of it.** That is exactly what the next subtopic does.

## Examples & Systems
The database-plus-search-index dual write as the canonical broken pattern.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Keeping Systems in Sync]] — the same race condition, the same partial-failure argument, and the same multi-leader diagnosis. One of the most stable sections in the chapter, which fits: the problem is structural, not technological.

## Related
- up: [[Databases and Streams (2e)]] · chapter: [[Ch 12 - Stream Processing (2e)]]
- [[Change Data Capture (2e)]] — the fix
- [[Multi-Leader Replication (2e)]] — why this is the same problem
- [[Detecting Concurrent Writes (2e)]] — the mechanism that would at least detect it
- 1st edition: [[Keeping Systems in Sync]] — the same subtopic
