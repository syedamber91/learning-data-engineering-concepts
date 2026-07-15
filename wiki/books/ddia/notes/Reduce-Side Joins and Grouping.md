---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
topic: MapReduce and Distributed Filesystems
type: subtopic
tags: [ddia, joins, sort-merge-join, skew]
sources:
  - raw/ch10.md
---
# Reduce-Side Joins and Grouping
> The shuffle acts as a message-delivery system: emit the join key as the "address" and all related records land in the same reducer call, enabling sort-merge joins and GROUP BY at scale.

## The Idea
Records reference other records — foreign keys, document references, graph edges — and code that needs both sides of the association needs a join. [[Denormalization]] reduces but rarely eliminates that need. A batch join is different in character from an OLTP join: rather than an indexed lookup for one user, it resolves *every* occurrence of the association across the whole dataset in one sweep. [[MapReduce]] has no indexes; it always does the equivalent of a full table scan, which is only sensible because the scan is parallelized and the query is aggregate-oriented anyway (compare [[Transaction Processing or Analytics]]).

Canonical example: a clickstream of user activity events (the fact table, in [[Stars and Snowflakes - Schemas for Analytics]] terms) joined with a user-profile database (a dimension) to correlate page popularity with viewer age. Querying the live user database per event would throttle throughput to network round-trips, risk crushing the database, and make the job nondeterministic as the remote data changes. Better: snapshot the user database into [[HDFS]] via ETL (see [[Data Warehousing]]) and join file against file.

## How It Works
- **Sort-merge join**: one mapper set keys activity events by user ID; another keys user records by user ID. The shuffle brings both to the same reducer, sorted. A *secondary sort* can guarantee the reducer sees the user record before that user's events, so it holds just one profile in a local variable while streaming the events — high throughput, tiny memory, zero network calls from user code.
- **Mappers "send messages"**: the emitted key works like a destination address. This cleanly separates physical data movement (framework) from application logic (your code), and the framework retries failed tasks transparently.
- **GROUP BY**: choose the grouping key as the map output key and the shuffle assembles the groups; then count, sum, or take top-k per group. *Sessionization* — reassembling one user's events scattered across many web servers' logs to analyze their session (A/B tests, marketing attribution) — is grouping by session cookie or user ID.

## Trade-offs & Pitfalls
- **Skew / hot keys**: a celebrity with millions of followers funnels a flood of records into one reducer, and the whole workflow waits on that straggler (see [[Skewed Workloads and Relieving Hot Spots]] and [[Hot Spots]]). Mitigations: Pig's skewed join samples first, then scatters hot-key records across random reducers while replicating the other side to all of them; Crunch's sharded join does the same with hot keys declared manually; Hive stores hot-key records in separate files and switches to a map-side join for them; hot-key aggregation can run in two stages (random pre-aggregation, then final combine).
- All the sorting, copying, and merging is expensive; when input assumptions allow, [[Map-Side Joins]] skip it entirely.

## Examples & Systems
Pig (skewed join), Crunch (sharded join), Hive (skewed-key metadata), LinkedIn-style recommendation pipelines built on clickstream joins.

## Related
- up: [[MapReduce and Distributed Filesystems]] · chapter: [[Ch 10 - Batch Processing]]
- [[Map-Side Joins]] — the faster alternative with stronger preconditions
- [[Skewed Workloads and Relieving Hot Spots]] — same hot-key problem in partitioned stores
- [[Stars and Snowflakes - Schemas for Analytics]] — fact/dimension framing of the join
- [[Stream Joins]] — the streaming counterpart of these algorithms
