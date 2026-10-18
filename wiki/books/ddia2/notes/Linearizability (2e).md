---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
type: topic
tags: [ddia2, linearizability, strong-consistency, recency-guarantee]
sources:
  - raw/ch10.md
---
# Linearizability
**If you want a replicated database to be as simple as possible to use, make it behave as if it were a consistent single-node database.** Then users don't have to worry about replication lag, conflicts, and other inconsistencies — **you get fault tolerance without the complexity of thinking about multiple replicas.**

**That is the idea behind linearizability**, also known as **atomic consistency**, **strong consistency**, **immediate consistency**, or **external consistency**. The exact definition is subtle, but **the basic idea is to make a system appear as if there is only one copy of the data and all operations on it are atomic.**

**In a linearizable system, as soon as one client successfully completes a write, all clients reading must be able to see the value just written.** Maintaining the illusion of a single copy means **guaranteeing the value read is the most recent, up-to-date value and doesn't come from a stale cache or replica.** In other words, **linearizability is a recency guarantee.**

**The nonlinearizable sports website.** Aaliyah and Bryce sit in the same room checking their phones for a game result. Just after the final score is announced, **Aaliyah refreshes, sees the winner, and excitedly tells Bryce.** Bryce incredulously hits reload, **but his request goes to a lagging replica, so his phone shows the game is still ongoing.**

**If they had hit reload at the same time it would be less surprising to get different results** — they wouldn't know exactly when their requests were processed. **But Bryce knows he initiated his query *after* hearing Aaliyah exclaim the score, so he expects a result at least as recent as hers. His stale result is a violation of linearizability.**

## Subtopics
- [[What Makes a System Linearizable (2e)]] — the register model, and the difference from serializability.
- [[Relying on Linearizability (2e)]] — the three cases where you genuinely need it.
- [[Implementing Linearizable Systems (2e)]] — which replication methods deliver it.
- [[The Cost of Linearizability (2e)]] — CAP, and the latency argument that matters more.

## Key Takeaways
- **Linearizability is the strongest consistency model in common use.** It includes read-after-write consistency, monotonic reads, and consistent prefix reads — **and more.**
- **The Aaliyah-and-Bryce shape recurs throughout the chapter**: it is the pattern of an out-of-band communication channel outrunning replication, and it appears again in cross-channel timing dependencies and in the nonlinearizable quorum example.
- **It is possible, though computationally expensive, to test whether a system's behaviour is linearizable** by recording the timings of all requests and responses and checking whether they can be arranged into a valid sequential order.

## Since the 1st Edition
The 1st edition's [[Linearizability]] topic used the same sports-website example and the same four subtopics. Substantively stable; the changes are in [[The Cost of Linearizability (2e)]] (a harsher verdict on CAP) and in what surrounds the topic — the 1st edition followed it with [[Ordering Guarantees]], while the 2nd follows it with [[ID Generators and Logical Clocks (2e)]].

## Related
- chapter: [[Ch 10 - Consistency and Consensus (2e)]]
- [[Problems with Replication Lag (2e)]] — the weaker guarantees this subsumes
- [[Consensus (2e)]] — how to get linearizability with fault tolerance
- 1st edition: [[Linearizability]] — the same topic
