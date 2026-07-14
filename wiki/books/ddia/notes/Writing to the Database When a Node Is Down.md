---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Leaderless Replication
type: subtopic
tags: [ddia, quorums, read-repair, anti-entropy]
sources:
  - raw/ch05.md
---
# Writing to the Database When a Node Is Down

> Leaderless systems shrug off a dead replica: write to the nodes that answer, read from several in parallel, and repair stragglers after the fact.

## The Idea

Suppose one of three replicas is rebooting for maintenance. A leader-based system might need a failover to keep accepting writes. A leaderless one needs nothing: the client sends the write to all three replicas in parallel, two acknowledge it, and that's declared success — the offline node simply misses the write. The catch appears later: when that node returns, it holds stale data. Reading from a single replica is therefore unsafe; instead reads also go to several nodes in parallel, and version numbers reveal which response is newest (see [[Detecting Concurrent Writes]]).

## How It Works

**Quorums.** With `n` replicas, a write needs `w` acknowledgments and a read queries `r` nodes. If `w + r > n`, every read set must overlap every successful write set in at least one node, so at least one queried replica is up to date — these are [[Quorum]] reads and writes, with `w` and `r` acting like minimum vote counts. Typical configuration: `n` odd (3 or 5), `w = r = (n+1)/2` rounded up, all tunable — a read-heavy workload might use `w = n, r = 1` (fast reads, but one dead node blocks all writes). With `n = 3, w = 2, r = 2` you tolerate one unavailable node; `n = 5, w = 3, r = 3` tolerates two. Requests still go to all `n` replicas in parallel; `w`/`r` only set how many responses you wait for. Fewer reachable nodes than `w` or `r` means the operation returns an error — and the cause (crash, full disk, network cut) doesn't matter, only whether a success response arrived. A cluster can hold more than `n` nodes; each value lives on just `n` of them, which is what lets the dataset be partitioned.

**Catching up.** Two mechanisms restore missed writes: [[Read Repair]] (a client noticing a stale response during a parallel read writes the newer value back — great for hot keys) and an [[Anti-Entropy]] background process that continuously diffs replicas and copies missing data, in no particular order and possibly with delay.

## Trade-offs & Pitfalls

- Without anti-entropy (e.g., Voldemort lacks it), rarely-read values may never be repaired — reduced durability for cold data.
- The overlap guarantee is weaker than it looks; see [[Limitations of Quorum Consistency]].

## Examples & Systems

Dynamo-style stores — Riak, Cassandra, Voldemort — all expose configurable `n`, `w`, `r`.

## Related

- up: [[Leaderless Replication]] · chapter: [[Ch 05 - Replication]]
- [[Handling Node Outages]] — how leader-based systems handle the same failure, via failover
- [[Limitations of Quorum Consistency]] — the fine print on `w + r > n`
- [[Sloppy Quorums and Hinted Handoff]] — relaxing which nodes may count toward `w`
