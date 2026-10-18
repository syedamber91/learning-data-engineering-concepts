---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
topic: Consensus
type: subtopic
tags: [ddia2, zookeeper, etcd, consul, chubby, ephemeral-nodes, service-discovery]
sources:
  - raw/ch10.md
---
# Coordination Services
> They look like key-value stores. They are not for storing your data — they are for holding the small, slow-changing facts that let a large cluster agree on who does what.

## The Idea
**Consensus algorithms are useful in any distributed database wanting linearizable operations**, and many modern distributed databases use them for replication. **But one family is a particularly prominent user: coordination services such as ZooKeeper, etcd, and Consul.**

**Although they look superficially like any other key-value store, they are not designed for high write volumes or general-purpose data storage.** **They are designed to coordinate among nodes of another distributed system** — **Kubernetes relies on etcd; Spark and Flink in high-availability mode rely on ZooKeeper running in the background.** **They hold small amounts of data that fit entirely in memory** (though still written to disk for durability), **replicated across multiple nodes via a fault-tolerant consensus algorithm.**

**They are modeled after Google's Chubby lock service**, and combine consensus with several other features that turn out to be particularly useful:
- **Locks and leases.** Consensus gives an atomic, fault-tolerant CAS; coordination services use it so that **if several nodes concurrently try to acquire the same lease, only one succeeds.**
- **Support for fencing.** When a resource is protected by a lease, **fencing prevents clients from interfering during a process pause or large network delay.** Consensus systems generate fencing tokens **by giving each log entry a monotonically increasing ID** — `zxid` and `cversion` in ZooKeeper, revision number in etcd.
- **Failure detection.** **Clients maintain a long-lived session and periodically exchange heartbeats.** **Even if the connection is temporarily interrupted or a server fails, leases held by the client remain active** — **but if there is no heartbeat for longer than the lease timeout, the service assumes the client is dead and releases the lease** (ZooKeeper calls these **ephemeral nodes**).
- **Change notifications.** **A client can request notification whenever certain keys change** — letting it find out when another client joins the cluster (from the value it writes) **or fails (because its session times out and its ephemeral nodes disappear)** — **saving the client from frequently polling.**

**Failure detection and change notifications do not require consensus, but they are useful alongside the atomic operations and fencing support that do.**

## How It Works
**Allocating work to nodes.** A coordination service is useful when **several instances of a process exist and one must be chosen as leader**, with another taking over on failure. **Necessary for single-leader databases, but also appropriate for job schedulers and similar stateful systems.**

**Another use case is a sharded resource** — database, message streams, file storage, distributed actor system — **needing decisions about which shard goes to which node.** **As new nodes join, some shards move to rebalance load; as nodes are removed or fail, others take over their work.**

**These tasks can be achieved by judicious use of atomic operations, ephemeral nodes, and notifications.** **Done correctly, the application automatically recovers from faults without human intervention.** **It's not easy, despite libraries like Apache Curator providing higher-level tools on top of the ZooKeeper client API — but it is still much better than implementing the consensus algorithms from scratch, which would be very prone to bugs.**

**A key architectural advantage: a dedicated coordination service can run on a fixed set of nodes (usually three or five), regardless of how many nodes are in the system relying on it.** **In a storage system with thousands of shards, running consensus over thousands of nodes would be terribly inefficient — it's much better to "outsource" consensus to a small number of nodes.**

**The data is normally quite slow-changing**: things like "the node at 10.1.1.23 is the leader for shard 7," **changing on a timescale of minutes or hours.** **Coordination services are not intended for data changing thousands of times per second** — **use a conventional database for that, or tools like Apache BookKeeper to replicate fast-changing internal state.**

**Service discovery.** ZooKeeper, etcd, and Consul are **also often used to find which IP address to connect to for a service.** **In cloud environments, where VMs continually come and go, you often don't know service IP addresses ahead of time** — so **services register their network endpoints in a registry at startup**, where other services find them. **Convenient, because failure detection and change notification make it easy to track instances as they come and go — and if you're already using the service for leases, locking, or leader election, it makes sense to use it for discovery too, since it already knows which node should receive requests.**

## Trade-offs & Pitfalls
- **Using consensus for service discovery is often overkill.** **This use case generally doesn't require linearizability**, and other properties matter more.
- **Managing configuration with coordination services.** Applications have parameters — timeouts, thread pool sizes — that are sometimes stored as key-value pairs in a coordination service, with **processes loading settings at startup and subscribing to change notifications.** **Configuration management doesn't need the consensus aspect**, but it's convenient **if you are already running the service anyway.** **Alternatively a process could periodically poll a file or URL, avoiding a specialized service.**
- The recurring theme: **several of the features people use coordination services for don't actually need consensus.** Knowing which parts do — locks, leases, fencing tokens, leader election — tells you when you genuinely need one.

## Examples & Systems
ZooKeeper, etcd, Consul; Google Chubby as the model; Kubernetes on etcd, Spark and Flink HA on ZooKeeper; Apache Curator; Apache BookKeeper for fast-changing state.

## Since the 1st Edition
Close to the 1st edition's [[Membership and Coordination Services]] — the same four features, the same work-allocation and service-discovery use cases, the same "outsource consensus to three or five nodes" argument, and the same Curator recommendation. **Updated:** **Consul** added alongside ZooKeeper and etcd; **Kubernetes-on-etcd and Spark/Flink-on-ZooKeeper** named as the canonical dependents; and **etcd revision numbers** added alongside ZooKeeper's `zxid`/`cversion` as fencing tokens.

## Related
- up: [[Consensus (2e)]] · chapter: [[Ch 10 - Consistency and Consensus (2e)]]
- [[Distributed Locks and Leases (2e)]] — the fencing these services provide
- [[Request Routing (2e)]] — shard assignment via ZooKeeper and etcd
- [[Dataflow Through Services - REST and RPC (2e)]] — service discovery in its own right
- 1st edition: [[Membership and Coordination Services]] — the same subtopic
