---
persona: vutr
kind: entity
sources:
- raw/linkedin-data-infrastructure/diving-deep-into-linkedins-data-infrastructure.md
last_updated: '2026-07-15'
qc: passed
slug: voldemort
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Voldemort is a highly available, low-latency distributed key-value store LinkedIn built in 2008 to serve products like "Who viewed my profile?" — the "live storage" tier in [[linkedin-three-tier-service-architecture]]. It was later improved to support adding nodes without downtime, scaling to tens of thousands of requests per second.

A Voldemort cluster is a set of uniquely-IDed nodes; a table is called a store, each store lives in a single cluster, and a store's partitions are distributed across all the cluster's nodes. Each store carries its own configuration — replication factor, schema, and the number of nodes required to participate in a read or write. Partitions are allocated to nodes via consistent hashing. The whole architecture is explicitly pluggable, inspired by Amazon's Dynamo paper: every module implements the same interface, which is what makes modules interchangeable and independently testable. Client API and conflict resolution: unlike a master-slave system, any replica of a partition can accept a write, so LinkedIn uses vector clocks to version each tuple and lets the application resolve conflicts between concurrent versions. Repair: Voldemort reconciles inconsistent key versions using two mechanisms taken from the Dynamo paper — read repair (detecting inconsistency at read time) and hinted handoff (triggered at write time). A failure detector marks a node down once its success ratio — successful operations over total operations — drops below a threshold, and a routing module applies the same consistent hashing to replicate data across nodes.

The storage engine differs by workload: BerkeleyDB Java Edition backs read-write traffic, while a custom read-only engine serves static offline data — built specifically for applications running multi-stage algorithms on systems like Hadoop. On disk, each node lays out a compact index plus data files inside versioned directories per store; every data deployment produces a new directory, which is what makes an instant rollback possible if a deployment goes wrong. A controller coordinates the full pipeline that gets that static data into Voldemort in the first place. An admin service runs on each node for privileged operations — adding or deleting stores, and rebalancing the cluster by moving partition ownership from one node to another — and keeps the system consistent mid-rebalance by redirecting requests to a partition's new destination as it moves.

At LinkedIn, Voldemort runs as ten clusters: nine handle read-write traffic and one handles read-only traffic through the custom engine. The largest read-write cluster serves a 60/40 read/write split at roughly 10,000 queries per second with 3ms average latency; the read-only cluster serves 9,000 reads per second at under 1ms latency. Store sizes range from 8KB up to 2.8TB for read-only stores, and up to 1.4TB for read-write stores.

*See also: [[databus]] · [[espresso]] · [[linkedin-three-tier-service-architecture]] · [[linkedin-data-infrastructure]]*

## Related in the other wiki
- [[Vector Clocks]] — DDIA's general causality-tracking concept is exactly the mechanism Voldemort uses to version tuples and let the application resolve concurrent-write conflicts, rather than picking a winner automatically.
- [[Read Repair]] — DDIA's concept of opportunistically fixing stale replicas during a read is one of the two repair mechanisms Voldemort borrows directly from the Dynamo paper, alongside hinted handoff.
