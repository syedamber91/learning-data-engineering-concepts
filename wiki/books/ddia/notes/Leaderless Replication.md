---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
type: topic
tags: [ddia, leaderless, dynamo, quorums, eventual-consistency]
sources:
  - raw/ch05.md
---
# Leaderless Replication

Single-leader and multi-leader replication both funnel each write through a node that decides write order. Leaderless systems abandon that idea entirely: any replica accepts writes directly from clients (or via a coordinator node that enforces no ordering). The style is old — some of the earliest replicated systems worked this way — but it was revived when Amazon built its in-house Dynamo store, which is why Riak, Cassandra, and Voldemort are called *Dynamo-style* databases (confusingly, AWS's hosted DynamoDB is single-leader). Without a leader there is no failover: availability comes from [[Quorum]] arithmetic — write to `w` of `n` replicas, read from `r`, and if `w + r > n` the read set must overlap the write set. Stale copies heal via [[Read Repair]] and [[Anti-Entropy]]; concurrent writes are inevitable and must be detected and merged rather than prevented. The result is a database that stays writable through node failures and network partitions, at the price of weak, probabilistic consistency that the application must consciously handle.

## Subtopics

- [[Writing to the Database When a Node Is Down]] — no failover, just quorum reads/writes over `n` replicas, plus the two catch-up mechanisms (read repair, anti-entropy).
- [[Limitations of Quorum Consistency]] — why `w + r > n` still doesn't guarantee fresh reads: sloppy quorums, concurrent writes, partial failures, and the difficulty of even monitoring staleness.
- [[Sloppy Quorums and Hinted Handoff]] — trading read-freshness guarantees for write availability during partitions, and how leaderless multi-datacenter operation works.
- [[Detecting Concurrent Writes]] — happens-before, last-write-wins and its data loss, sibling merging, and version vectors.

## Key Takeaways

- No leader means no failover and no single write choke point; tolerance of node failure, slowness, and network glitches is the design goal.
- The quorum condition `w + r > n` (commonly `n` odd, `w = r = (n+1)/2`) gives overlap, not certainty — treat stale reads as tunable probability, not impossibility.
- [[Eventual Consistency]] here is genuinely vague: with only read repair and no anti-entropy process, a rarely-read value can stay stale indefinitely.
- You usually do *not* get read-your-writes, monotonic reads, or consistent-prefix guarantees; those require the machinery of [[Ch 07 - Transactions]] or [[Consensus]].
- Concurrency is embraced, not avoided: clients may receive siblings and must merge them, ideally with [[Version Vectors]] tracking causality and CRDTs automating the merge.

## Related

- chapter: [[Ch 05 - Replication]]
- [[Leaders and Followers]] — the ordering-by-leader approach this abandons
- [[Multi-Leader Replication]] — the other architecture that must resolve concurrent writes
- [[Linearizability]] — the strong guarantee quorums fail to provide
- [[Problems with Replication Lag]] — the anomalies that resurface here without their fixes
