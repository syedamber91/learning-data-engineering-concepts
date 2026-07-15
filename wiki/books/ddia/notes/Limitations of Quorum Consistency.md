---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Leaderless Replication
type: subtopic
tags: [ddia, quorums, staleness, eventual-consistency]
sources:
  - raw/ch05.md
---
# Limitations of Quorum Consistency

> `w + r > n` promises overlap, not freshness — a catalog of edge cases where quorum reads still return stale data.

## The Idea

The quorum argument sounds airtight: if the nodes you wrote to and the nodes you read from must share at least one member, some read response carries the latest value. Note the sets only need to *overlap* — majorities are the common choice (tolerating up to `n/2` failures), but any overlapping assignment works, a flexibility some distributed algorithms exploit. You can even deliberately pick `w + r ≤ n`: reads and writes still go to all `n` nodes but wait for fewer replies, buying lower latency and higher availability during network trouble at the cost of more stale reads. The uncomfortable truth is that even a strict [[Quorum]] leaks staleness through several cracks.

## How It Works

Ways a quorum read can miss the latest write, even with `w + r > n`:

- A sloppy quorum puts the `w` writes on different nodes than the `r` reads visit — overlap gone (see [[Sloppy Quorums and Hinted Handoff]]).
- Two concurrent writes have no defined order; if the tie is broken by timestamp (last write wins), writes vanish to [[Clock Skew]]. The safe route is merging — see [[Detecting Concurrent Writes]].
- A write racing a read may have landed on only some replicas; whether the read sees it is undetermined.
- A write that succeeded on fewer than `w` replicas (say, some disks were full) reports failure but is *not rolled back* where it did land — later reads may or may not return it.
- A node holding the new value can fail and be restored from a stale replica, silently dropping the copy count below `w`.
- Even with everything healthy, unlucky timing can violate [[Linearizability]] (the Chapter 9 analysis of quorums).

**Monitoring staleness** is also harder without a leader. Leader-based [[Replication]] has a log position per node, so lag = leader position minus follower position, an easy metric. Leaderless writes have no fixed order, and a system relying only on [[Read Repair]] (no [[Anti-Entropy]]) has *no bound at all* on how ancient a rarely-read value may be. Research exists on predicting stale-read probability from `n`, `w`, `r`, but it isn't common practice — a shame, since "eventual" deserves quantifying.

## Trade-offs & Pitfalls

- Treat `w`/`r` as dials on the *probability* of stale reads, never as absolute guarantees.
- None of the [[Problems with Replication Lag]] guarantees come for free here: no read-your-writes, no monotonic reads, no consistent prefix. Stronger promises need transactions or [[Consensus]].

## Examples & Systems

Dynamo-style stores (Riak, Cassandra, Voldemort) are explicitly optimized for workloads tolerating [[Eventual Consistency]].

## Related

- up: [[Leaderless Replication]] · chapter: [[Ch 05 - Replication]]
- [[Writing to the Database When a Node Is Down]] — the quorum mechanics being qualified
- [[What Makes a System Linearizable]] — the strong guarantee quorums don't reach
- [[Monotonic Reads]] — one of the lag guarantees quorums fail to provide
