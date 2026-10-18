---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Leaderless Replication
type: subtopic
tags: [ddia2, quorum, read-repair, hinted-handoff, anti-entropy, staleness]
sources:
  - raw/ch06.md
---
# Writing to the Database When a Node Is Down
> w + r > n. Write to enough replicas, read from enough replicas, and the two sets must overlap — which is a guarantee right up until you read the list of edge cases where it isn't.

## The Idea
Three replicas, one currently unavailable — perhaps rebooting for a system update. In a single-leader configuration you might need a failover to keep processing writes. **In a leaderless configuration there is no such thing as failover, since all replicas are equal.**

The client sends the write to all three replicas in parallel; the two available ones accept it and the unavailable one misses it. If **two out of three acknowledgements** are sufficient, the write is considered successful after the client receives two OKs — **the client simply ignores that one replica missed the write.**

When the unavailable node comes back and clients read from it, **writes that happened while it was down are missing, so reads may return stale values**. To solve this, **read requests are also sent to several nodes in parallel**. The client may get different responses — an up-to-date value from one node, a stale one from another — so **every written value is tagged with a version number or timestamp**, and the client uses the one with the greatest timestamp, **even if only one replica returned it**.

## How It Works
**Catching up on missed writes.** Three mechanisms in Dynamo-style stores:
- **Read repair.** When a client reads from several nodes in parallel it can detect stale responses — seeing a version 6 value from replica 3 and version 7 from replicas 1 and 2 — and **writes the newer value back to the stale replica**. Works well for **values that are read often**.
- **Hinted handoff.** If one replica is unavailable, another may store writes on its behalf as **hints**. When the intended replica returns, the storing replica sends the hints and deletes them. This brings replicas up to date **even for values that are never read** and therefore not covered by read repair.
- **Anti-entropy.** A background process periodically looks for differences between replicas and copies missing data across. **Unlike a replication log, this process does not copy writes in any particular order, and there may be a significant delay before data is copied.**

**Quorums.** Generally, with **n** replicas, every write must be confirmed by **w** nodes and every read must query at least **r** nodes. **As long as w + r > n**, we expect an up-to-date value when reading, because **at least one of the r nodes read from must be up to date** — the read and write sets must overlap. These are **quorum reads and writes**; think of r and w as the minimum votes required for the operation to be valid.

The parameters are typically configurable. A common choice makes **n an odd number (commonly 3 or 5) and sets w = r = (n + 1) / 2** rounded up. But you can vary them: a workload with few writes and many reads may benefit from **w = n, r = 1**, making reads faster — **at the cost that just one failed node causes all writes to fail**.

The quorum condition lets the system tolerate unavailable nodes: **if w < n you can still process writes with a node down; if r < n you can still process reads.** With n = 3, w = 2, r = 2 you tolerate one unavailable node; with n = 5, w = 3, r = 3 you tolerate two. **Normally reads and writes are sent to all n replicas in parallel, and w and r determine how many you wait for.** If fewer than w or r are available, the operation returns an error — and the system **doesn't need to distinguish between kinds of fault** (crash, disk full, network interruption); it cares only whether a node returned success.

> There may be **more than n nodes in the cluster**, but any given value is stored on only n nodes — which is what allows the dataset to be sharded across more machines than one value's replica set.

**Quorums are not necessarily majorities.** r and w are often chosen as a majority (more than n/2) because that ensures w + r > n while tolerating up to n/2 failures — **but what actually matters is only that the read and write sets overlap in at least one node**, and other assignments are possible, allowing flexibility in distributed algorithm design.

You can also set **w + r ≤ n**, not satisfying the quorum condition. Reads and writes are still sent to n nodes but fewer successful responses are required. **You are then more likely to read stale values**, but you get **lower latency** and **higher availability**: during a network interruption where many replicas become unreachable, there is a higher chance you can keep processing — the database becomes unavailable only when reachable replicas fall below w or r.

## Trade-offs & Pitfalls
**Even with w + r > n, consistency can be confusing in edge cases:**
- **If a node carrying a new value fails and its data is restored from a replica carrying an old value**, the number of replicas storing the new value may fall below w, **breaking the quorum condition**.
- **During rebalancing**, nodes may have inconsistent views of which nodes hold the n replicas for a value, so **read and write quorums may no longer overlap**.
- **If a read is concurrent with a write**, it may or may not see the concurrently written value — and **it's possible for one read to see the new value and a subsequent read to see the old one**.
- **If a write succeeded on some replicas but failed overall** (succeeding on fewer than w), **it is not rolled back on the replicas where it succeeded** — so a write reported as failed may or may not appear in subsequent reads.
- **If timestamps come from a real-time clock** (as in Cassandra and ScyllaDB), **writes might be silently dropped if another node with a faster clock wrote to the same key.**
- **If two writes occur concurrently**, one may be processed first on one replica and the other first on another — a conflict, exactly as in multi-leader replication.

**So although quorums appear to guarantee that a read returns the latest written value, in practice it is not so simple.** Dynamo-style databases are generally **optimised for use cases that can tolerate eventual consistency**; w and r let you **adjust the probability of reading stale values**, but **it is wise not to take them as absolute guarantees.**

**Monitoring staleness** is also harder here. For leader-based replication the database typically exposes **replication lag** metrics, possible because writes are applied in the same order everywhere and each node has a position in the log — subtract the follower's position from the leader's. **In leaderless systems there is no fixed order in which writes are applied, which makes monitoring more difficult.** The number of hints stored for handoff is one measure of health but **is difficult to interpret usefully**. Eventual consistency is deliberately vague, **but for operability it's important to be able to quantify "eventual."**

## Examples & Systems
Cassandra, ScyllaDB, Riak as Dynamo-style stores; read repair, hinted handoff, and anti-entropy as the three catch-up mechanisms.

## Since the 1st Edition
Merges the 1st edition's [[Writing to the Database When a Node Is Down]] and [[Limitations of Quorum Consistency]] into one subtopic. The three catch-up mechanisms, the w + r > n condition, and the edge-case list carry over. **Added:** the explicit note that **quorums need not be majorities**, only overlapping; the ScyllaDB clock-skew case; and a fuller treatment of **monitoring staleness** as an operability problem.

## Related
- up: [[Leaderless Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Detecting Concurrent Writes (2e)]] — resolving the conflicts quorums permit
- [[The Majority Rules (2e)]] — quorums as a distributed-systems primitive
- [[Single-Leader Versus Leaderless Replication Performance (2e)]] — what quorum size costs
- 1st edition: [[Writing to the Database When a Node Is Down]], [[Limitations of Quorum Consistency]] — the two notes this merges
