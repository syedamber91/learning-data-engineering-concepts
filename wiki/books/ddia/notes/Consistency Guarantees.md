---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
type: topic
tags: [ddia, consistency-models, eventual-consistency, distributed-systems]
sources:
  - raw/ch09.md
---
# Consistency Guarantees
> Replicated databases offer a spectrum of consistency models, from the weak promise of eventual convergence up to strong models that behave like a single copy of the data.

## The Idea
Any replicated database — single-leader, multi-leader, or leaderless — will show different data on different nodes if you inspect them at the same instant, because writes reach replicas at different times. The question is what promise, if any, the system makes about these discrepancies. Chapter 9 exists to map out that space of promises and to show that the strongest ones ultimately depend on [[Consensus]].

## How It Works
The floor of the spectrum is [[Eventual Consistency]]: if writes stop, all replicas will *eventually* return the same value. A more honest name would be *convergence*, because the guarantee says only that replicas drift toward agreement — it says nothing about *when*. Before convergence, a read may return stale data or fail entirely; even read-your-own-write behavior is not promised (see [[Reading Your Own Writes]]).

This is treacherous for developers because a database superficially resembles a variable in a single-threaded program, yet behaves nothing like one. Code written against an eventually consistent store tends to work in testing and fail subtly under concurrency or network faults — exactly the conditions that are hardest to reproduce.

Stronger models exist, at a price: [[Linearizability]] (the strongest common model, a recency guarantee), and causal consistency (a middle ground built on [[Causality]]). Systems with stronger guarantees are easier to program against but tend to be slower or less fault-tolerant.

A useful distinction: distributed consistency models are *not* the same as transaction [[Isolation Levels]]. Isolation (e.g., [[Serializability]]) is about race conditions between concurrent transactions on possibly one node; distributed consistency is about coordinating replica state under delay and failure. The two hierarchies overlap slightly but address different problems.

## Trade-offs & Pitfalls
- Weak guarantees push complexity onto the application: every read must be treated as possibly stale.
- Bugs from eventual consistency hide until a fault or high concurrency exposes them — testing rarely catches them.
- Strong guarantees cost latency and availability (see [[The Cost of Linearizability]] and the [[CAP Theorem]]).
- Choosing a model is an engineering decision, not a default: many applications need less than linearizability but more than "eventually."

## Examples & Systems
Most replicated stores (Dynamo-style leaderless systems, asynchronously replicated leader-based databases) default to eventual consistency. Coordination services like [[ZooKeeper]] and [[Etcd|etcd]] sit at the strong end, using consensus to offer linearizable operations.

## Related
- chapter: [[Ch 09 - Consistency and Consensus]]
- [[Linearizability]] — the strongest model this chapter examines
- [[Problems with Replication Lag]] — where the weak-consistency symptoms first appeared
- [[Ordering Guarantees]] — causality as a cheaper middle ground
- [[Weak Isolation Levels]] — the analogous (but distinct) transaction hierarchy
