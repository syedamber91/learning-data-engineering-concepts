---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Problems with Replication Lag
type: subtopic
tags: [ddia, causality, replication-lag, partitioning]
sources:
  - raw/ch05.md
---
# Consistent Prefix Reads

> A guarantee that writes are observed in the order they happened, so no one ever sees an answer before its question.

## The Idea

This anomaly is a violation of [[Causality]]. Picture a two-line exchange: Mr. Poons asks Mrs. Cake a question, and she replies. Her reply causally depends on his question. Now suppose an observer receives the conversation through replicas: her words travel through a low-lag follower, his through a high-lag one. The observer hears the *answer first, then the question* — the speaker appears psychic. Nothing is lost; the order is simply scrambled for the observer.

## How It Works

**Consistent prefix reads** guarantees: if writes occur in some order, anyone reading them sees them appear in that same order — a reader always observes a *prefix* of the write sequence, never a shuffled subset.

Why it happens: in a single-leader database, all writes pass through one node and followers apply them in the leader's order, so any single replica's state is always a valid prefix and the anomaly cannot occur. But in **partitioned (sharded) databases** ([[Partitioning]], Chapter 6), each partition is replicated independently — there is *no global ordering of writes*. A reader can see partition A in a new state and partition B in an old state, interleaving causally-ordered events out of order.

Remedies:
- Write causally related data to the **same partition**, so one replication stream preserves their order — but some applications can't shard that way efficiently.
- Use algorithms that **track causal dependencies explicitly**, the machinery developed in [[Detecting Concurrent Writes]] (the happens-before relation, [[Version Vectors]]) and later in [[Ordering and Causality]].

## Trade-offs & Pitfalls

- Fundamentally a cross-partition problem — single-partition or single-leader deployments get it for free.
- Co-locating causal data conflicts with load-spreading goals of partitioning.
- Full causal tracking adds metadata and complexity; most sharded stores simply don't provide the guarantee.
- The same message-overtaking effect appears inside all-to-all multi-leader topologies — see [[Multi-Leader Replication Topologies]].

## Examples & Systems

The Poons/Cake dialog (borrowed from Terry Pratchett) is the canonical example; the underlying situation is any sharded store where an observer reads two partitions with unequal replication lag.

## Related

- up: [[Problems with Replication Lag]] · chapter: [[Ch 05 - Replication]]
- [[Ordering and Causality]] — Chapter 9's deep treatment of causal order
- [[Multi-Leader Replication Topologies]] — writes overtaking each other between leaders
- [[Partitioning of Key-Value Data]] — why independent partitions lose global order
- [[Detecting Concurrent Writes]] — happens-before machinery for tracking causality
