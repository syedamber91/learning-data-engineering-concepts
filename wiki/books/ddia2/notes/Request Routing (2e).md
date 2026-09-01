---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 7
chapter_title: Sharding
type: topic
tags: [ddia2, request-routing, zookeeper, etcd, gossip, service-discovery]
sources:
  - raw/ch07.md
---
# Request Routing
You know how to shard a dataset and how to rebalance it. Now: **if you want to read or write a particular key, how do you know which node — which IP address and port — to connect to?**

This is **request routing**, and it is very similar to **service discovery**. **The biggest difference:** with services running application code, each instance is usually **stateless**, so a load balancer can send a request to any instance. **With sharded databases, a request for a key can be handled only by a node that is a replica for the shard containing that key** — so routing must be aware of the assignment from **keys to shards** and from **shards to nodes**.

## Key Takeaways
**Three approaches:**
1. **Allow clients to contact any node**, via a round-robin load balancer. If that node happens to own the relevant shard it handles the request directly; otherwise **it forwards the request to the appropriate node, receives the reply, and passes it back to the client.**
2. **Send all requests to a routing tier first**, which determines the right node and forwards accordingly. **The routing tier handles no requests itself; it acts only as a shard-aware load balancer.**
3. **Require clients to be aware of the sharding and the shard-to-node assignment**, so a client connects directly to the appropriate node with no intermediary.

**Each case has the same three hard problems:**
- **Who decides which shard lives on which node?** A single coordinator is simplest — **but how do you make it fault-tolerant if the coordinator's node goes down, and if the role can fail over, how do you prevent a split brain** where two coordinators make contradictory assignments?
- **How does the routing component — node, routing tier, or client — learn about changes in the assignment?**
- **While a shard is being moved there is a cutover period** during which the new node has taken over but requests to the old node may still be in flight. **How do you handle those?**

**The usual answer is a separate coordination service.** Many systems rely on **ZooKeeper or etcd**, which use **consensus algorithms to provide fault tolerance and protection against split brain**. Each node registers itself in ZooKeeper, **ZooKeeper maintains the authoritative mapping of shards to nodes**, and other actors — the routing tier or a sharding-aware client — **subscribe to that information**, being notified whenever a shard changes ownership or a node is added or removed. **HBase and SolrCloud use ZooKeeper; Kubernetes uses etcd** to track which service instance runs where; **MongoDB has a similar architecture but uses its own config server implementation and `mongos` daemons as the routing tier**; **Kafka, YugabyteDB, TiDB, and ScyllaDB use built-in implementations of the Raft consensus protocol** for this coordination.

**Riak takes a different approach: a gossip protocol among the nodes** to disseminate cluster state changes. **This provides much weaker consistency than a consensus protocol — it is possible to have split brain, where different parts of the cluster have different node assignments for the same shard. Leaderless databases can tolerate this because they generally make weak consistency guarantees anyway.**

When using a routing tier or sending requests to a random node, **clients still need IP addresses to connect to. These change far less often than shard assignments, so DNS is often sufficient for that.**

**One important scope limit:** this discussion focuses on finding the shard for an **individual key**, which is most relevant for sharded **OLTP** databases. **Analytical databases also shard, but their query execution is very different** — rather than executing in a single shard, **a query commonly needs to aggregate and join data from many shards in parallel.**

## Since the 1st Edition
The 1st edition's [[Request Routing]] presented the same three approaches, the same three hard problems, and the same ZooKeeper architecture. **Added:** the explicit comparison to service discovery (stateless instances versus shard-bound replicas); **Kafka, YugabyteDB, TiDB, and ScyllaDB using built-in Raft** rather than an external coordinator, which is the real architectural shift since 2017; the note that **DNS suffices for node addresses** because they change slowly; and the scope caveat about analytical parallel query execution. The 1st edition also covered a "parallel query execution" section here, which the 2nd edition defers to the batch processing chapter.

## Related
- chapter: [[Ch 07 - Sharding (2e)]]
- [[Dataflow Through Services - REST and RPC (2e)]] — service discovery, the sibling problem
- [[Coordination Services (2e)]] — ZooKeeper and etcd examined properly
- 1st edition: [[Request Routing]] — the same topic

## In the vutr data-engineering wiki
- [[consumer-groups-and-partition-assignment]] — the same routing question at consumer-group scope: Kafka's Group Coordinator holds authoritative membership while the group leader computes and propagates the partition assignment.
