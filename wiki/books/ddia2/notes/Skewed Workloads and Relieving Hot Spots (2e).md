---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 7
chapter_title: Sharding
topic: Sharding of Key-Value Data
type: subtopic
tags: [ddia2, hot-key, skew, key-salting, heat-management, celebrity]
sources:
  - raw/ch07.md
---
# Skewed Workloads and Relieving Hot Spots
> Consistent hashing distributes *keys* evenly. It does nothing about a single key that a million people are hitting at once.

## The Idea
**Consistent hashing ensures keys are uniformly distributed across nodes, but that doesn't mean the actual load is uniformly distributed.** If the workload is highly skewed — much more data under some partition keys than others, or a much higher request rate to some keys — **you can still end up with some servers overloaded while others sit almost idle.**

The canonical case: on a social media site, **a post by a celebrity with millions of followers may cause a storm of activity**, resulting in a large volume of reads and writes to the same key — the celebrity's user ID, or the ID of the action people are commenting on.

## How It Works
- **A more flexible sharding policy helps.** A system defining shards by ranges of keys (or of hashes) **makes it possible to put an individual hot key in a shard by itself, perhaps even assigning it a dedicated machine.**
- **Or compensate at the application level.** If one key is known to be very hot, **add a random number to the beginning or end of the key**. Adding just two random digits **splits the writes evenly across 100 keys**, which can then be distributed to different shards.

## Trade-offs & Pitfalls
The salting technique has three costs, and the book states all of them:
- **Reads get more expensive.** Having split writes across 100 keys, **reads must read all 100 and combine them.** The volume of reads to each shard of the hot key is not reduced — **only the write load is split.**
- **It requires bookkeeping.** It only makes sense to salt the small number of hot keys; doing it for the vast majority of low-throughput keys would be unnecessary overhead. So **you need a way to track which keys are being split, and a process for converting a regular key into a specially managed hot key.**
- **Load changes over time.** A post that has gone viral may be hot for a couple of days and then calm down. And **some keys may be hot for writes while others are hot for reads**, needing different strategies.

**Some systems automate this**, especially cloud services designed for large scale. **Amazon calls it heat management or adaptive capacity**; the details are beyond the book's scope.

## Examples & Systems
The celebrity-post storm as the canonical hot key; Amazon's heat management / adaptive capacity as the automated response.

## Since the 1st Edition
The 1st edition's [[Skewed Workloads and Relieving Hot Spots]] described the same celebrity problem and the same random-suffix salting with the same read-amplification and bookkeeping caveats. **Added:** putting an individual hot key in its own shard or on a dedicated machine as a first-class option; the observation that **read-hot and write-hot keys need different strategies**; and **Amazon's heat management / adaptive capacity** as an example of automated hot-shard handling — the 1st edition closed by saying such automation didn't yet exist in mainstream systems.

## Related
- up: [[Sharding of Key-Value Data (2e)]] · chapter: [[Ch 07 - Sharding (2e)]]
- [[Materializing and Updating Timelines (2e)]] — the celebrity problem at the application layer
- [[Operations - Automatic Versus Manual Rebalancing (2e)]] — whether the system fixes this itself
- 1st edition: [[Skewed Workloads and Relieving Hot Spots]] — the same subtopic
