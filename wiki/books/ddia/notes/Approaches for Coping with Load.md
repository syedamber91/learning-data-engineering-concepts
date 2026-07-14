---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
topic: Scalability
type: subtopic
tags: [ddia, scaling-up, scaling-out, elasticity, shared-nothing]
sources:
  - raw/ch01.md
---
# Approaches for Coping with Load
> There is no magic scaling sauce — architectures are rebuilt roughly every order of magnitude of growth, mixing scale-up and scale-out around assumptions about which operations dominate.

## The Idea
Once load is quantified and performance measured, the practical question is how to keep performance good as load parameters climb. The sobering baseline: an architecture suited to one level of load will likely fail at ten times that level, so fast-growing services should expect to rethink their architecture at every order-of-magnitude jump — sometimes more often.

## How It Works
The classic dichotomy is **scaling up** (vertical: a beefier machine) versus **scaling out** (horizontal: spreading load across many smaller machines, also called a *shared-nothing* architecture — the foundation for [[Partitioning]]/[[Sharding]]). Single-machine systems are simpler, but high-end hardware gets disproportionately expensive, so heavy workloads are usually forced outward. Good real-world architectures are pragmatic hybrids — a few powerful machines can beat a swarm of small VMs on both simplicity and cost.

Orthogonally, systems differ in **elasticity**: elastic systems add resources automatically when they detect rising load; manually scaled systems rely on a human reading capacity and adding machines. Elasticity helps when load is unpredictable, but manual scaling is simpler and springs fewer operational surprises (a tension developed in [[Rebalancing Partitions]]).

A crucial asymmetry: distributing *stateless* services is easy; making *stateful* data systems distributed introduces real complexity. Hence the long-standing convention: keep the database on one node and scale up until cost or high-availability needs force distribution. Kleppmann suggests this wisdom may expire as distributed abstractions improve — distributed data systems might become the default even for modest workloads.

## Trade-offs & Pitfalls
- **No generic scalable architecture exists** ("magic scaling sauce"). The binding constraint may be read volume, write volume, data volume, data complexity, response-time needs, access patterns — usually a mix. Vivid illustration: 100,000 requests/sec at 1 kB each and 3 requests/minute at 2 GB each have the *same* throughput but demand utterly different designs.
- **Architectures encode load assumptions.** Scale-specific designs bet on which operations are common and which rare; if the bet is wrong, the scaling effort is wasted at best, counterproductive at worst.
- **Premature scaling is a startup trap.** In an unproven product, iterating fast on features beats engineering for hypothetical future load.
- Even bespoke architectures are assembled from general-purpose building blocks in familiar patterns — which is what the rest of the book catalogs.

## Related
- up: [[Scalability]] · chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Describing Load]] — the load parameters an architecture bets on
- [[Describing Performance]] — the metrics that tell you when to re-architect
- [[Rebalancing Partitions]] — Ch 6 on automatic vs. manual scaling operations
- [[Replication]] — with partitioning, the machinery of scale-out
