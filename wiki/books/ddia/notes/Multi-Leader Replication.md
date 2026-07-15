---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
type: topic
tags: [ddia, multi-leader, write-conflicts, multi-datacenter]
sources:
  - raw/ch05.md
---
# Multi-Leader Replication

Single-leader replication has one choke point: every write must reach the one leader, so losing your connection to it means losing the ability to write. Multi-leader replication (master–master, active/active) lets several nodes accept writes; each leader forwards its changes to all other nodes and simultaneously acts as a follower of the other leaders. The freedom to write anywhere buys latency, datacenter fault tolerance, and offline operation — and pays for it with the defining problem of the model: **concurrent writes to the same data on different leaders produce conflicts that must be resolved**. Because multi-leader support is often retrofitted onto databases, it interacts badly with autoincrement keys, triggers, and integrity constraints, and is widely treated as dangerous territory to avoid unless the use case demands it.

## Subtopics

- [[Use Cases for Multi-Leader Replication]] — multi-datacenter deployments, offline-capable clients (calendar sync), and real-time collaborative editing.
- [[Handling Write Conflicts]] — detection is asynchronous and late; strategies span avoidance, convergent resolution (LWW, merge), custom handlers, and CRDTs.
- [[Multi-Leader Replication Topologies]] — circular, star, and all-to-all layouts for propagating writes, and their failure/ordering pathologies.

## Key Takeaways

- Rarely worth it inside a single datacenter; shines when leaders are separated by unreliable, high-latency links (datacenters, devices, browser replicas).
- Writes complete locally and replicate asynchronously, hiding inter-datacenter latency — but the same asynchrony means conflicts surface too late to ask the user.
- Conflict avoidance (route all writes for a record to one home leader) is the most practical strategy, and it degrades exactly when leadership must move.
- Convergence requires deterministic resolution: last-write-wins is popular and silently lossy; CRDTs, mergeable data structures, and operational transformation are the principled alternatives.
- Topology choice matters: sparse topologies (circle, star) have single points of failure; dense (all-to-all) topologies suffer causal ordering violations that timestamps cannot fix — [[Version Vectors]] can.

## Related

- chapter: [[Ch 05 - Replication]]
- [[Leaders and Followers]] — the single-leader baseline this generalizes
- [[Leaderless Replication]] — the other conflict-embracing architecture
- [[Detecting Concurrent Writes]] — shared machinery for concurrency detection
- [[Consistent Prefix Reads]] — the causality anomaly that reappears between leaders
