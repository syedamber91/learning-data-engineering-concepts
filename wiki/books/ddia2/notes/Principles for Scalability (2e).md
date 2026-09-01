---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Scalability
type: subtopic
tags: [ddia2, scalability, architecture, decomposition, autoscaling]
sources:
  - raw/ch02.md
---
# Principles for Scalability
> There is no generic scalable architecture — informally, no *magic scaling sauce*. Two systems with identical total throughput can need completely different designs.

## The Idea
The architecture of large-scale systems is usually **highly specific to the application**. The book's illustration is precise: a system handling 100,000 requests per second of 1 kB each looks very different from one handling 3 requests per minute of 2 GB each — even though both move 100 MB/second.

## How It Works
- An architecture appropriate for one level of load is unlikely to cope with ten times that load. On a fast-growing service you will probably need to **rethink your architecture on every order of magnitude** of load increase. Since application needs also evolve, it is usually not worth planning scaling needs more than one order of magnitude ahead.
- **Decompose.** The best general principle is to break a system into smaller components that can operate largely independently of one another. This is the principle underlying microservices, sharding, stream processing, and shared-nothing architectures alike. The challenge is knowing where to draw the line between what belongs together and what belongs apart.
- **Don't over-complicate.** If a single-machine database will do the job, it is probably preferable to a complicated distributed setup. Autoscaling systems — automatically adding or removing resources with demand — are cool, but **if your load is fairly predictable, a manually scaled system may have fewer operational surprises**. A system with 5 services is simpler than one with 50. Good architectures usually involve a pragmatic mixture of approaches.

## Trade-offs & Pitfalls
- The decomposition principle and the simplicity principle pull against each other, and the book does not pretend otherwise — it says the challenge *is* drawing the line, and that good architectures are mixtures.
- Autoscaling's appeal is aesthetic as much as economic; predictable load is the condition under which it stops paying for itself.

## Examples & Systems
Microservices, sharding, stream processing, and shared-nothing architectures as four expressions of the same decomposition principle.

## Since the 1st Edition
New as a standalone subtopic. The 1st edition made the "no magic scaling sauce" point and the "architecture is application-specific" point inside [[Approaches for Coping with Load]]; the 2nd edition separates them out and adds the order-of-magnitude planning rule and the autoscaling-versus-predictability caution.

## Related
- up: [[Scalability (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Simplicity - Managing Complexity (2e)]] — the same instinct, applied to code
- [[Operations - Automatic Versus Manual Rebalancing (2e)]] — the autoscaling argument in its sharding form
- [[Microservices and Serverless (2e)]] — decomposition's best-known instance
