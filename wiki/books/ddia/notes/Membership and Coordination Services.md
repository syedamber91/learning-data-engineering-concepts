---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
topic: Distributed Transactions and Consensus
type: subtopic
tags: [ddia, zookeeper, etcd, coordination, service-discovery]
sources:
  - raw/ch09.md
---
# Membership and Coordination Services
> ZooKeeper and etcd are "outsourced consensus": a small, fixed voting cluster holding slow-changing coordination data, exposing linearizable atomic operations, fencing tokens, session-based failure detection (ephemeral nodes), and change notifications.

## The Idea
[[ZooKeeper]] and [[Etcd]] look like key-value databases, so why do they bother with a consensus algorithm? Because their job isn't general data storage — application developers rarely use them directly; they arrive indirectly through HBase, [[Hadoop]] YARN, OpenStack Nova, and [[Apache Kafka]], which lean on them for coordination. They hold small, memory-resident (though disk-durable) datasets replicated via fault-tolerant [[Total Order Broadcast]], the exact primitive database replication needs: same writes, same order, consistent replicas.

## How It Works
ZooKeeper, modeled on Google's Chubby lock service, combines features whose *combination* is the point:
- **Linearizable atomic operations.** An atomic compare-and-set builds a distributed lock: of several concurrent claimants, exactly one wins, guaranteed atomic and linearizable through node failures and interruptions. Locks are usually **leases** with expiry, so a crashed client eventually releases ([[Process Pauses]] is why expiry matters).
- **Total ordering of operations.** Every operation receives a monotonically increasing transaction ID (`zxid`) and version number (`cversion`) — precisely the [[Fencing Tokens]] needed to stop a paused, zombie lock-holder from clobbering a successor's work.
- **Failure detection.** Clients hold long-lived sessions kept alive by heartbeats; transient interruptions survive, but when heartbeats stop past the session timeout, the session dies — and locks configured as **ephemeral nodes** vanish automatically with it.
- **Change notifications.** Clients can *watch* keys, learning when another client joins (writes a value) or fails (its ephemeral nodes disappear) without polling.

Of these, only the linearizable atomic operations truly require [[Consensus]].

**Allocating work to nodes.** The model shines for [[Leader Election]] (databases, job schedulers, any stateful primary/standby service) and for assigning partitions of a resource to nodes — as members join, partitions rebalance onto them; as they fail, others take over ([[Rebalancing Partitions]]). Atomic ops + ephemeral nodes + notifications, carefully composed (libraries like Apache Curator help), give automatic fault recovery with no human in the loop. Critically, ZooKeeper runs its majority votes over a *fixed small* cluster (three or five nodes) while serving potentially thousands of clients — consensus work is outsourced. Its data changes on the timescale of minutes or hours ("node 10.1.1.23 leads partition 7"), never millions of times per second (fast-changing replicated app state belongs elsewhere, e.g., Apache BookKeeper).

**Service discovery** — finding the IP for a service name as VMs come and go — is a common ZooKeeper/etcd/Consul use, but arguably doesn't *need* consensus: DNS, the traditional answer, is deliberately non-linearizable, cached, and stale-tolerant, prioritizing availability. Leader election, by contrast, does need it — hence some consensus systems add read-only caching replicas that receive the decision log asynchronously without voting, serving non-linearizable discovery reads cheaply.

**Membership services** (a lineage back to 1980s air-traffic-control research) couple failure detection with consensus so nodes *agree* on the current live membership. The verdict can be wrong — a live node declared dead — but agreement itself is the value: "choose the lowest-numbered member as leader" only works if everyone agrees who the members are.

## Trade-offs & Pitfalls
- ZooKeeper is not a general-purpose database; storing high-churn application state in it is a misuse.
- Using these APIs correctly is still hard — but far better than reimplementing consensus, which fails routinely in the wild.

## Examples & Systems
ZooKeeper (Zab), etcd (Raft), Consul, Google Chubby, Apache Curator, Apache BookKeeper; HBase/YARN/Nova/Kafka as indirect consumers.

## Related
- up: [[Distributed Transactions and Consensus]] · chapter: [[Ch 09 - Consistency and Consensus]]
- [[Fault-Tolerant Consensus]] — the algorithms these services package
- [[The Truth Is Defined by the Majority]] — fencing tokens and lease pitfalls from Ch 8
- [[Detecting Faults]] — why timeout-based liveness needs agreement on top
- [[Request Routing]] — Ch 6's use of ZooKeeper for partition-to-node maps
