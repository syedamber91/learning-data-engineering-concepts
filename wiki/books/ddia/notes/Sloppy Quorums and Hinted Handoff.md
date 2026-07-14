---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Leaderless Replication
type: subtopic
tags: [ddia, sloppy-quorum, hinted-handoff, availability, multi-datacenter]
sources:
  - raw/ch05.md
---
# Sloppy Quorums and Hinted Handoff

> When a partition cuts you off from a value's home nodes, accept the write on whatever nodes you *can* reach — durability now, delivery later.

## The Idea

Well-configured quorums already avoid failover and tolerate slow nodes (you wait for `w` or `r` responses, not all `n`). But a network interruption can strand a client from the specific nodes where a value lives, even while those nodes are alive and serving other clients. With fewer than `w` or `r` designated nodes reachable, the strict answer is to fail the request. The alternative: accept the write anyway on reachable nodes *outside* the value's usual home set. That is a **sloppy quorum** — like being locked out of your house and sleeping on the neighbor's couch. When connectivity returns, the temporary hosts forward the stashed writes to the proper home nodes: **hinted handoff** (the neighbor sends you home once you find your keys).

## How It Works

A sloppy quorum still demands `w` write acks and `r` read responses, but the responders need not belong to the designated `n` home nodes. This maximizes write availability — any `w` reachable nodes suffice — while quietly changing what the [[Quorum]] means: it is now only a *durability* promise (the data exists on `w` nodes somewhere), not an overlap guarantee. Until hinted handoff completes, a read of `r` home nodes can entirely miss the latest write even though `w + r > n`. In the traditional sense, a sloppy quorum isn't a quorum at all.

**Multi-datacenter operation.** [[Leaderless Replication]] suits geo-distribution since it already tolerates conflicts, interruptions, and latency spikes. Two patterns: Cassandra and Voldemort count nodes across all datacenters in `n` (configurable per-datacenter split), send every write everywhere, but wait only for a local-datacenter quorum, letting cross-datacenter traffic complete asynchronously. Riak instead keeps client-node traffic within one datacenter (`n` is local) and replicates between clusters asynchronously in the background, resembling [[Multi-Leader Replication]] across sites.

## Trade-offs & Pitfalls

- Write availability up, read-freshness guarantee gone — one of the headline caveats in [[Limitations of Quorum Consistency]].
- Optional everywhere: enabled by default in Riak, disabled by default in Cassandra and Voldemort. Know your database's setting before reasoning about consistency.
- Hinted handoff and read repair can themselves surface write conflicts — see [[Detecting Concurrent Writes]].

## Examples & Systems

Dynamo introduced the technique; Riak, Cassandra, and Voldemort all implement it with differing defaults and differing multi-datacenter models.

## Related

- up: [[Leaderless Replication]] · chapter: [[Ch 05 - Replication]]
- [[Limitations of Quorum Consistency]] — sloppy quorums as a staleness loophole
- [[Use Cases for Multi-Leader Replication]] — the multi-leader view of multi-datacenter writes
- [[Writing to the Database When a Node Is Down]] — strict quorums, the baseline being loosened
