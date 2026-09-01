---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
type: topic
tags: [ddia2, scalability, load, premature-optimization]
sources:
  - raw/ch02.md
---
# Scalability
A system working reliably today may not work reliably in the future, and a common reason for degradation is **increased load** — from 10,000 concurrent users to 100,000, or 1 million to 10 million, or simply much larger data volumes. **Scalability** is the term for a system's ability to cope with increased load.

The book takes the standard dismissal seriously before disagreeing with it. People often say "you're not Google or Amazon, stop worrying about scale and just use a relational database." Whether that applies depends on what you are building. If you have a new product with few users, perhaps at a startup, the overriding engineering goal is usually to keep the system **as simple and flexible as possible** so you can adapt features as you learn what customers need. In that environment, worrying about hypothetical future scale is counterproductive: at best it is wasted effort and premature optimisation, at worst it locks you into an inflexible design that makes the application harder to evolve.

But **scalability is not a one-dimensional label**. It is meaningless to say "X is scalable" or "Y doesn't scale." Discussing scalability means asking questions like: if the system grows in a particular way, what are our options for coping? How can we add computing resources to handle additional load? Based on current growth projections, when will we hit the limits of our current architecture? If your application does become popular and load grows, you will learn where your bottlenecks are and along which dimensions you need to scale — and *that* is when to start worrying about scalability techniques.

## Subtopics
- [[Understanding Load (2e)]] — measure the current load, in the right units, before arguing about growth.
- [[Shared-Memory, Shared-Disk, and Shared-Nothing Architectures (2e)]] — the three hardware architectures behind scaling up and scaling out.
- [[Principles for Scalability (2e)]] — no magic scaling sauce; decompose, and don't over-plan.

## Key Takeaways
- Scalability is a question about *a specific growth direction*, not a property. Always name the dimension.
- The startup counterargument is legitimate and the book endorses it — simplicity and flexibility beat speculative scale work when you don't yet know your bottleneck.
- Two ways to frame the growth question: with resources held constant, how does performance change as load grows? Or, to keep performance constant, how much must resources grow?
- **Linear scalability** — double the resources, handle twice the load, same performance — is the good case. Occasionally you do better than linear thanks to economies of scale or better peak-load distribution. Much more likely, cost grows *faster* than linearly: with a lot of data, processing a single write request may involve more work than with a small amount of data, even for the same request size.
- The usual goal is keeping performance within SLA requirements while minimising running cost; more computing resources means higher cost, and which hardware is most cost-effective changes over time as new types become available.

## Since the 1st Edition
The 1st edition's [[Scalability]] made the same "not a one-dimensional label" argument and asked similar questions. The 2nd edition adds the explicit startup/premature-optimisation counterargument, tightens the two framings of the growth question, and — most significantly — replaces the 1st edition's [[Approaches for Coping with Load]] subtopic with the proper **shared-memory / shared-disk / shared-nothing** taxonomy, which the 1st edition mentioned only in passing.

## Related
- chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Describing Performance (2e)]] — the metrics scalability is defined against
- [[Ch 07 - Sharding (2e)]] — the core technique for shared-nothing scaling
- 1st edition: [[Scalability]] — the same framing, different subtopics
