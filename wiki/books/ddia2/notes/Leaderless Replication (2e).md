---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
type: topic
tags: [ddia2, leaderless, dynamo, quorum, cassandra, riak]
sources:
  - raw/ch06.md
---
# Leaderless Replication
Single-leader and multi-leader replication both rest on the idea that **a client sends a write to one node and the database copies it to the other replicas**, with a leader determining the order in which writes are processed and followers applying them in that order.

Some systems abandon the concept of a leader entirely and **allow any replica to directly accept writes from clients**. Some of the earliest replicated data systems were leaderless, but the idea was mostly forgotten during the era of relational dominance. It became fashionable again after **Amazon used it for its in-house Dynamo system in 2007**. **Riak, Cassandra, and ScyllaDB** are open source datastores with leaderless models inspired by Dynamo, so this kind of database is also called **Dynamo-style**.

> **Dynamo is not DynamoDB.** The original Dynamo architecture was described in a paper but never released outside Amazon. **The similarly named DynamoDB, a more recent cloud database from Amazon, has a completely different architecture: single-leader replication based on the Multi-Paxos consensus algorithm.**

In some leaderless implementations the client sends writes directly to several replicas; in others a **coordinator node** does this on the client's behalf. **But unlike a leader, that coordinator does not enforce a particular ordering of writes** — a difference with profound consequences for how the database is used.

## Subtopics
- [[Writing to the Database When a Node Is Down (2e)]] — read repair, hinted handoff, anti-entropy, and the quorum condition.
- [[Single-Leader Versus Leaderless Replication Performance (2e)]] — where leaderless wins, and where its quorums cost you.
- [[Multi-Region Operation (2e)]] — coordinator nodes and configurable consistency levels across regions.
- [[Detecting Concurrent Writes (2e)]] — happens-before, siblings, version numbers, and version vectors.

## Key Takeaways
- **No failover exists**, because all replicas are equal and there are no leaders. That single fact drives most of the family's behaviour, good and bad.
- Writes go to all replicas in parallel and **a configurable number of acknowledgements makes the write successful** — the client simply ignores that some replicas missed it.
- Because replicas can be stale, **reads also go to several nodes in parallel**, and **every written value is tagged with a version number or timestamp** so the client can tell which responses are up to date.
- The absence of a total order on writes is the deep difference. It is why leaderless systems need conflict detection and resolution, why staleness is hard to monitor, and why they tolerate gray failures gracefully.

## Since the 1st Edition
The 1st edition's [[Leaderless Replication]] covered the same model with the same Dynamo lineage. **New:** ScyllaDB added; the **explicit warning that DynamoDB is not Dynamo-style** but single-leader Multi-Paxos; and a restructured subtopic set — the 1st edition had [[Writing to the Database When a Node Is Down]], [[Limitations of Quorum Consistency]], and [[Detecting Concurrent Writes]], while the 2nd edition folds quorum limitations into the first subtopic and adds two new ones: [[Single-Leader Versus Leaderless Replication Performance (2e)]] and [[Multi-Region Operation (2e)]].

## Related
- chapter: [[Ch 06 - Replication (2e)]]
- [[Single-Leader Replication (2e)]] and [[Multi-Leader Replication (2e)]] — the ordered alternatives
- [[Dealing with Conflicting Writes (2e)]] — the resolution mechanisms this family reuses
- 1st edition: [[Leaderless Replication]] — the same topic
