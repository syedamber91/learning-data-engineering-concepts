---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Multi-Leader Replication
type: subtopic
tags: [ddia2, geo-replication, multi-region, latency, consistency]
sources:
  - raw/ch06.md
---
# Geographically Distributed Operation
> A leader in every region. Writes get local latency and survive an inter-region link failure — and you give up the ability to guarantee a bank account can't go negative.

## The Idea
**It rarely makes sense to use a multi-leader setup within a single region**, because the benefits rarely outweigh the added complexity. But consider a database with replicas in several regions — to tolerate the failure of an entire region, or for proximity to users. This is a **geographically distributed**, **geo-distributed**, or **geo-replicated** setup. With single-leader replication the leader must live in one region and **all writes must go through that region**.

In a multi-leader configuration you can have **a leader in each region**: within each region, regular leader–follower replication (with followers perhaps in a different availability zone), and between regions, each region's leader replicates its changes to the leaders in the others.

## How It Works
The book compares the two configurations on four axes:

**Performance.** Single-leader: **every write must go over the internet to the leader's region**, adding significant latency and possibly defeating the purpose of having multiple regions. Multi-leader: **every write is processed in the local region and replicated asynchronously**, so inter-region network delay is hidden from users and perceived performance may be better.

**Tolerance of regional outages.** Single-leader: if the leader's region becomes unavailable, **failover can promote a follower in another region**. Multi-leader: **each region continues operating independently**, and replication catches up when the offline region returns.

**Tolerance of network problems.** Even with dedicated connections, **inter-region traffic is less reliable than traffic within a region or zone**. Single-leader is **very sensitive** to problems on that link, because a client in one region writing to a leader in another must send its request over the link and wait for the response. **Multi-leader with asynchronous replication tolerates network problems better** — during a temporary interruption each region's leader keeps processing writes independently.

**Consistency.** Single-leader **can provide strong consistency guarantees, such as serializable transactions**. This is the **biggest downside of multi-leader systems**: the consistency they can achieve is **much weaker**. You **can't guarantee that a bank account won't go negative, or that a username is unique** — it is always possible for different leaders to process writes that are individually fine (paying out some of the money in an account, registering a particular username) **but violate the constraint when taken together**.

## Trade-offs & Pitfalls
- **This is a fundamental limitation of distributed systems, not an implementation gap.** If you need to enforce such constraints, **you are better off with a single-leader system.** But multi-leader systems can still achieve consistency properties useful in a wide range of apps that don't need them.
- The four axes don't resolve to a single winner — three favour multi-leader, and the fourth, consistency, is often the one that decides.

## Examples & Systems
A bank account going negative and a duplicate username as the two constraints multi-leader cannot enforce.

## Since the 1st Edition
This is the 1st edition's "multi-datacenter operation" use case, **renamed to reflect region/zone vocabulary** and restructured into the explicit four-axis comparison. The substance — local write latency, independent regional operation, link-failure tolerance, and the constraint-enforcement limitation — carries over. The 2nd edition states the consistency limitation more sharply as a fundamental limit rather than a practical caveat.

## Related
- up: [[Multi-Leader Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Multi-Region Operation (2e)]] — the leaderless answer to the same problem
- [[Dealing with Conflicting Writes (2e)]] — the cost of accepting local writes
- [[Enforcing Constraints (2e)]] — the constraint problem examined properly
