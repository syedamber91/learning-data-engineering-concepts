---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
type: topic
tags: [ddia, request-routing, service-discovery, zookeeper]
sources:
  - raw/ch06.md
---
# Request Routing
> With data spread across a shifting set of nodes, some component — a node, a routing tier, or the client itself — must always know which machine owns the key being requested.

Once a dataset is partitioned and rebalancing moves partitions around, a client asking "which IP and port holds key foo?" faces a moving target. This is an instance of the broader *service discovery* problem, which afflicts any highly available networked software; many companies have built (and open-sourced) in-house solutions. Three architectures answer it: (1) let clients contact any node, which serves the request if it owns the partition or forwards it and relays the reply; (2) interpose a dedicated routing tier that acts as a partition-aware load balancer without handling data itself; (3) make clients partition-aware so they connect directly to the right node. All three reduce to one hard question — how does the routing decision-maker learn about assignment changes, and how do all participants stay in agreement? Disagreement means requests land on wrong nodes. Distributed [[Consensus]] protocols solve agreement in principle but are hard to implement (Chapter 9), so most systems either outsource the problem to a coordination service like [[ZooKeeper]] or gossip among themselves.

## Subtopics
- [[Parallel Query Execution]] — beyond single-key routing: how MPP databases decompose analytic queries across partitions.

## Key Takeaways
- Three routing topologies: any-node forwarding, dedicated routing tier, partition-aware client — all needing an authoritative view of partition assignment.
- [[ZooKeeper]]-style coordination: nodes register themselves; the service holds the authoritative partition→node map and notifies subscribers (routing tier or clients) on every change. Used by HBase, SolrCloud, and [[Apache Kafka]]; LinkedIn's Espresso uses Helix (itself on ZooKeeper); MongoDB does the equivalent with its own config servers plus `mongos` routing daemons.
- Cassandra and Riak avoid the external dependency via a gossip protocol: nodes share cluster-state changes among themselves and any node can forward a request (approach 1), at the cost of more complexity inside the database.
- Couchbase pairs its no-automatic-rebalance design with a `moxi` routing tier that learns changes from cluster nodes.
- Finding the routing tier or entry nodes themselves is a slower-moving problem — plain DNS usually suffices.

## Related
- up: chapter [[Ch 06 - Partitioning]] · part [[Part II - Distributed Data]]
- [[Rebalancing Partitions]] — the churn that makes routing hard
- [[Membership and Coordination Services]] — Chapter 9's deep dive on ZooKeeper-style services
- [[Fault-Tolerant Consensus]] — the agreement problem underneath routing metadata
