---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
topic: ID Generators and Logical Clocks
type: subtopic
tags: [ddia2, timestamp-oracle, percolator, spanner, linearizability, consensus]
sources:
  - raw/ch10.md
---
# Linearizable ID Generators
> A user sets their account to private, then uploads a photo. With a non-linearizable ID generator, a stranger can see the photo. That's the whole argument.

## The Idea
**Lamport and hybrid logical clocks give useful ordering, but weaker than a linearizable single-node ID generator.** **Linearizability requires that if request A completed before request B began, B must have the higher ID, even if A and B never communicated.** **Lamport clocks can ensure only that a node generates timestamps greater than any it has seen — no guarantee about timestamps it hasn't seen.**

**The worked failure.** On a social media site, **user A wants to share an embarrassing photo privately with friends.** Their account is initially public, so **using their laptop they change the account settings to private. Then they use their phone to upload the photo.** **Since A performed these in sequence, they reasonably expect the upload to be subject to the new restricted permissions. This is not necessarily the case.**

**The account permission and the photo are stored in two separate databases (or shards), each assigning timestamps from a Lamport or hybrid logical clock.** **Since the photos database didn't read from the accounts database, its local counter may be slightly behind — so the photo upload gets a lower timestamp than the settings update.**

**Now a viewer who is not A's friend looks at A's profile, and their read uses MVCC snapshot isolation.** **The read's timestamp could be greater than the photo upload's but less than the account settings update's** — so **the system determines the account is still public at read time and shows the viewer the embarrassing photo they were not supposed to see.**

**Possible fixes:** maybe **the photos database should read the user's account status before writing — but it's easy to forget such a check.** If A's actions had been on the same device, **the app could track the latest timestamp of that user's writes — but with a laptop and a phone that's not so easy.** **The simplest solution is a linearizable ID generator**, ensuring the photo upload gets a greater ID than the permissions change.

## How It Works
**The simplest implementation is actually using a single node.** It needs to do only three things: **atomically increment a counter and return its value**, **persist the counter** (so a crash and restart doesn't produce duplicates), and **replicate it for fault tolerance** using single-leader replication. **This is used in practice — TiDB/TiKV calls it a timestamp oracle, inspired by Google's Percolator.**

**As an optimization, avoid a disk write and replication on every request**: the generator can **write a record describing a batch of IDs**; once persisted and replicated, it hands them out in sequence, and **before running out it persists the record for the next batch.** **Some IDs will be skipped on a crash or failover, but you won't issue any duplicate or out-of-order IDs.**

**You can't easily shard the ID generator**, since multiple shards independently handing out IDs **can no longer guarantee linearizable order.** **You also can't easily distribute it across regions** — in a geographically distributed database **all ID requests must go to a node in a single region.** **On the upside, the generator's job is very simple, so a single node can handle a large request throughput.**

**The alternative is what Spanner does**: rely on a physical clock returning **not a single timestamp but a range indicating the uncertainty**, and **wait for the duration of that interval to elapse before returning.** **Assuming the interval is correct, this also guarantees that if one request completes before another begins, the later one has a greater timestamp** — **and it does so without any communication, so even requests in different regions are ordered correctly without cross-region round trips.** **The downside is needing hardware and software support for tightly synchronized clocks and computing the uncertainty interval.**

## Trade-offs & Pitfalls
**Enforcing constraints using logical clocks — and why they aren't enough.** A linearizable CAS can implement locks, uniqueness constraints, and similar constructs. **Is a logical clock or linearizable ID generator also sufficient? Not quite.**

**When several nodes try to acquire the same lock or register the same username, you could assign timestamps and pick the lowest as the winner.** **If the clock is linearizable, you know future requests will get greater timestamps, so no future request will beat the winner.**

**But part of the problem is unsolved: how does a node know whether its own timestamp is the lowest?** **To be sure, it needs to hear from every other node that might have generated a timestamp.** **If one of those nodes has failed or cannot be reached, the system grinds to a halt, because we can't be sure that node's timestamp isn't lower.** **This is not the kind of fault-tolerant system we need.**

**To implement locks, leases, and similar constructs fault-tolerantly, we need something stronger than logical clocks or ID generators. We need consensus.**

## Examples & Systems
TiDB/TiKV's timestamp oracle; Google Percolator as its inspiration; Spanner's uncertainty-interval approach.

## Since the 1st Edition
**New as a subtopic.** The 1st edition's [[Ordering Guarantees]] made a structurally similar argument — that Lamport timestamps aren't sufficient for uniqueness constraints because you must hear from every node — but framed it around total order broadcast rather than ID generation, and used a username-registration example rather than the privacy scenario. **New here:** the **embarrassing-photo cross-shard MVCC scenario**, which makes the consequence concrete and security-relevant; **timestamp oracles** with TiDB/TiKV and Percolator named; and the **batch-of-IDs optimization** with its skipped-IDs trade-off.

## Related
- up: [[ID Generators and Logical Clocks (2e)]] · chapter: [[Ch 10 - Consistency and Consensus (2e)]]
- [[Consensus (2e)]] — the stronger primitive this argument demands
- [[Relying on Synchronized Clocks (2e)]] — Spanner's TrueTime approach
- [[Relying on Linearizability (2e)]] — the constraints being enforced
- 1st edition: [[Ordering Guarantees]] — the closest predecessor
