---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Leaderless Replication
type: subtopic
tags: [ddia2, multi-region, coordinator-node, consistency-level, cassandra, riak]
sources:
  - raw/ch06.md
---
# Multi-Region Operation
> Leaderless replication was built to tolerate conflicting concurrent writes, network interruptions, and latency spikes. That is exactly the list of things a cross-region deployment produces.

## The Idea
Cross-region replication was already discussed as a use case for multi-leader replication. **Leaderless replication is also suitable for multi-region operation**, because it is designed to tolerate conflicting concurrent writes, network interruptions, and latency spikes.

## How It Works
**Cassandra and ScyllaDB.** A client performing a multi-region write first chooses a node in its **local** region, called the **coordinator node**, and sends the write there. The coordinator **forwards the write to all replicas in its own region and to one replica in every other region**, which then forwards it to the other replicas in that region. **This optimisation avoids making the cross-region request multiple times.**

You then choose from a variety of **consistency levels** determining how many responses a request needs:
- a **quorum across the replicas in all regions**,
- a **separate quorum in each region**, or
- a **quorum only in the client's local region**.

**A local quorum avoids waiting for slow requests to other regions, but is also more likely to return stale results.**

**Riak** takes a different approach: **all communication between clients and database nodes stays local to one region**, so **n describes the number of replicas within one region**. Cross-region replication between database clusters happens **asynchronously in the background, in a style similar to multi-leader replication**.

## Trade-offs & Pitfalls
- The consistency-level menu is the point: **the same database can be tuned per query** between local latency and cross-region freshness, which neither single-leader nor multi-leader offers as directly.
- Riak's design is worth noting as a hybrid — leaderless *within* a region, multi-leader *between* regions — which is a reminder that the three families are building blocks rather than exclusive choices.

## Examples & Systems
Cassandra and ScyllaDB coordinator nodes and consistency levels; Riak's region-local n with asynchronous inter-region replication.

## Since the 1st Edition
Substantially expanded. The 1st edition mentioned multi-datacenter operation for leaderless replication in a short paragraph inside [[Leaderless Replication]], noting the Cassandra and Riak approaches. The 2nd edition gives it its own subtopic, describes the **coordinator-node forwarding optimisation** explicitly, and enumerates the **three consistency-level options** with their trade-off — none of which the 1st edition spelled out.

## Related
- up: [[Leaderless Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Geographically Distributed Operation (2e)]] — the multi-leader answer to the same problem
- [[Writing to the Database When a Node Is Down (2e)]] — the quorum machinery being tuned
- [[Problems with Replication Lag (2e)]] — the zone/region distinction
