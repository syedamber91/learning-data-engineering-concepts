---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
type: topic
tags: [ddia2, id-generation, uuid, snowflake, ordering, autoincrement]
sources:
  - raw/ch10.md
---
# ID Generators and Logical Clocks
**In many applications you need to assign a unique ID to records when they are created**, giving you a primary key. **In single-node databases it is common to use an autoincrementing integer**, which fits in 64 bits (or even 32, if you're sure you'll never exceed 4 billion records — **but that is risky**).

**Another advantage of autoincrementing IDs is that their order tells you the order in which records were created.** A chat application assigning autoincrementing IDs can **display messages in order of increasing ID and the threads make sense**: Aaliyah posts a question with ID 1, and Bryce's answer gets a greater ID, 3.

**This single-node ID generator is another example of a linearizable system.** Each ID request **atomically increments a counter and returns the old value — a fetch-and-add operation** — and **linearizability ensures that if Aaliyah's post completes before Bryce's begins, Bryce's ID must be greater.** **Messages that are concurrent may be ordered either way, as long as they are unique.**

**An in-memory single-node generator is easy** — use your CPU's atomic increment instruction. **Making the counter persistent takes a bit more effort**, so a crash and restart doesn't reset it and produce duplicates. **But the real problems are:**
- **It is not fault-tolerant** — that node is a single point of failure.
- **It's slow if you want to create a record in another region**, potentially requiring a round trip to the other side of the planet just to get an ID.
- **That single node could become a bottleneck** at high write throughput.

## Subtopics
- [[Logical Clocks (2e)]] — Lamport timestamps, hybrid logical clocks, and how they differ from vector clocks.
- [[Linearizable ID Generators (2e)]] — when weaker ordering isn't enough, and why even this isn't enough for locks.

## Key Takeaways
Four alternative ID schemes, **all unique but with much weaker ordering than a single-node counter:**
- **Sharded ID assignment.** Multiple nodes assign IDs — one generating even numbers, one odd; or reserve some bits for a shard number. **IDs stay compact, but you lose the ordering property**: with messages 16 and 17 **you don't know whether 16 was actually sent first**, since one node may have been ahead of the other.
- **Preallocated blocks of IDs.** Node A claims 1–1,000, node B claims 1,001–2,000, and each hands out IDs from its block, requesting a new one when running low. **This doesn't ensure correct ordering either** — one message may get an ID in 1,001–2,000 and a *later* message an ID in 1–1,000.
- **Random UUIDs.** **Generated locally on any node without communication**, at the cost of more space (128 bits). **Version 4 is essentially a random number long enough that collisions are vanishingly unlikely.** **But the order is also random, so comparing two IDs tells you nothing about which is newer.**
- **Wall-clock timestamp made unique.** With NTP-corrected clocks, **put a timestamp in the most significant bits and fill the rest with something ensuring uniqueness** — a shard number plus per-shard sequence, or a long random value. Used in **version 7 UUIDs, X's Snowflake, ULIDs, Hazelcast's Flake ID generator, and MongoDB ObjectIDs.**

**Wall-clock timestamps provide at best an approximate ordering.** **If an earlier write gets a timestamp from a slightly fast clock and a later write from a slightly slow one, the timestamp order is inconsistent with what actually happened.** **With clock jumps from a nonmonotonic clock, even timestamps from a single node might be ordered incorrectly.** **So wall-clock-based ID generators are unlikely to be linearizable.**

**You can reduce inconsistency with high-precision clock synchronization using atomic clocks or GPS — but it would be nice to generate IDs that are unique and correctly ordered without special hardware.** That is what logical clocks provide.

## Since the 1st Edition
**New as a topic.** The 1st edition had no treatment of ID generation as a distributed systems problem — its corresponding topic was [[Ordering Guarantees]], organised around causality and sequence numbers, which discussed **noncausal sequence number generators** briefly as a way of motivating Lamport timestamps. **The 2nd edition reframes the whole topic around the practical question of generating IDs**, which makes the connection to linearizability concrete: **the single-node autoincrement everyone reaches for is a linearizable system, and everything else trades ordering for scalability.** UUID v7, Snowflake, ULIDs, Flake IDs, and MongoDB ObjectIDs are all named here for the first time.

## Related
- chapter: [[Ch 10 - Consistency and Consensus (2e)]]
- [[Relying on Synchronized Clocks (2e)]] — why wall-clock ordering fails
- [[Linearizability (2e)]] — the property a single-node generator has
- 1st edition: [[Ordering Guarantees]] — the topic this replaces
