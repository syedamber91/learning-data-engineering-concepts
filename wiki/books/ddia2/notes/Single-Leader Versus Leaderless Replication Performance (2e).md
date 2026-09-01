---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Leaderless Replication
type: subtopic
tags: [ddia2, request-hedging, gray-failure, tail-latency, sloppy-quorum]
sources:
  - raw/ch06.md
---
# Single-Leader Versus Leaderless Replication Performance
> Leaderless systems are resilient because they don't distinguish between the normal case and the failure case. There is no "is it bad enough to fail over?" decision to get wrong.

## The Idea
A single-leader system can provide strong consistency guarantees that are difficult or impossible in a leaderless one. **But reads in a leader-based system can also return stale values** if made on an asynchronously updated follower — so reading from the leader is what ensures up-to-date responses, and that has performance problems:
- **Read throughput is limited by the leader's capacity**, in contrast with read scaling across asynchronously updated replicas.
- **If the leader fails you must wait for detection and failover** before requests continue. Even a very quick failover is noticeable to users through temporarily increased response times; a slow one means the system is unavailable for its duration.
- **The system is very sensitive to performance problems on the leader.** If the leader is slow — overload, resource contention — the increased response times immediately affect users.

## How It Works
**A leaderless architecture is more resilient against all of these.** Because **there is no failover, and requests go to multiple replicas in parallel anyway**, one replica becoming slow or unavailable has very little impact on response times: **the client simply uses the responses from the replicas that are faster to respond.** Using the fastest responses is called **request hedging**, and it can **significantly reduce tail latency**.

**At its core, the resilience of a leaderless system comes from the fact that it doesn't distinguish between the normal case and the failure case.** This is especially helpful for **gray failures**, where a node isn't completely down but is running in a degraded state, unusually slow to handle requests — or when a node is simply overloaded (recovery via hinted handoff after being offline can itself cause a lot of load). **A leader-based system has to decide whether the situation is bad enough to warrant a failover, which can itself cause further disruption; in a leaderless system that question doesn't even arise.**

## Trade-offs & Pitfalls
**Leaderless systems have their own performance problems:**
- **Failure detection is still needed**, even without failover: one replica must detect when another is unavailable so it can store hints for the writes that replica missed, and send them on recovery. **This puts additional load on the replicas at a time when the system is already under strain.**
- **Quorum size costs latency.** The more replicas you have, the bigger your quorums and the more responses you must wait for. **Even waiting only for the fastest r or w replicas, and even making requests in parallel, a bigger r or w raises the chance of hitting a slow replica**, increasing overall response time. **In practice, quorums are seldom more than four out of seven nodes or five out of nine.**
- **A large-scale network interruption** disconnecting a client from many replicas can make it **impossible to form a quorum**. Some leaderless databases offer a configuration allowing **any reachable replica to accept writes, even if it isn't one of the usual replicas for that key** — Riak and Dynamo call this a **sloppy quorum**; Cassandra and ScyllaDB call it **consistency level ANY**. **There is no guarantee subsequent reads will see the written value**, but depending on the application it may still be better than the write failing.

**The three-way ranking.** **Multi-leader replication can offer even greater resilience against network interruptions than leaderless replication**, since reads and writes require communication with only one leader, which can be co-located with the client — **but since a write on one leader propagates asynchronously, reads can be arbitrarily out of date.** **Quorum reads and writes provide a compromise: good fault tolerance and a high likelihood of reading up-to-date data.**

## Examples & Systems
Request hedging for tail-latency reduction; sloppy quorums (Riak, Dynamo) and consistency level ANY (Cassandra, ScyllaDB).

## Since the 1st Edition
Substantially new as a subtopic. The 1st edition discussed sloppy quorums and hinted handoff inside its quorum sections but had **no systematic performance comparison** between single-leader and leaderless replication, and did not use the terms **request hedging** or **gray failure**. The framing — that leaderless resilience comes from not distinguishing normal from failure cases — is a new argument, as is the closing three-way ranking of the replication families by resilience.

## Related
- up: [[Leaderless Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Use of Response Time Metrics (2e)]] — why a bigger quorum hurts the tail
- [[Handling Node Outages (2e)]] — the failover decision leaderless systems avoid
- [[Fault Detection (2e)]] — detecting an unavailable node, which is still required
