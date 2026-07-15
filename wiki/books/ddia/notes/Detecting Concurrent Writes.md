---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Leaderless Replication
type: subtopic
tags: [ddia, version-vectors, last-write-wins, siblings, happens-before]
sources:
  - raw/ch05.md
---
# Detecting Concurrent Writes

> Since concurrent writes have no true order, replicas converge either by discarding data (last write wins) or by tracking causality with version numbers and merging siblings.

## The Idea

Dynamo-style stores let several clients write the same key at once, so conflicts occur even with strict quorums — and can also arise via [[Read Repair]] or hinted handoff. Network delays deliver events to replicas in different orders; if each node blindly overwrote on arrival, replicas would diverge *permanently*. [[Eventual Consistency]] demands convergence, and most implementations handle it poorly enough that developers must understand the machinery themselves.

## How It Works

**Last write wins (LWW).** Force an arbitrary order: stamp every write with a timestamp, keep the biggest, discard the rest. Convergent, but "recent" is a fiction — concurrent writes have no meaningful order — and durability suffers: writes acknowledged to clients (having reached `w` replicas) are silently dropped, and [[Clock Skew]] can even kill *non-concurrent* writes. LWW is Cassandra's only conflict-resolution method and optional in Riak. Fine for caches; otherwise the only safe pattern is write-once immutable keys (Cassandra's recommended UUID keys).

**Happens-before.** Operation A *happens before* B if B knows about, depends on, or builds upon A; two operations are **concurrent** iff neither happens before the other. Physical time is irrelevant — mutual unawareness is what counts. Every pair is thus A-before-B, B-before-A, or concurrent; ordered pairs let the later overwrite the earlier, concurrent pairs are genuine conflicts.

**Version numbers (single replica).** The server keeps a per-key version, incremented on every write. Reads return *all* not-yet-overwritten values plus the latest version; a client must read before writing, merge what it received, and send the version back with its write. The server then overwrites everything at or below that version but keeps higher-versioned values as **siblings** — concurrent values the writer couldn't have known about (Riak's term). The chapter's shopping-cart walkthrough interleaves five writes from two clients with nothing ever silently lost.

**Merging siblings.** The burden shifts to clients: for a cart, union the siblings. But removals break unions — a deleted item resurfaces unless deletion leaves a versioned **tombstone** marker. Hand-written merges being error-prone, CRDTs (Riak datatypes) merge automatically, deletions included.

**[[Version Vectors]].** With multiple leaderless replicas, one counter isn't enough: keep a version number *per replica* per key; each replica increments its own and tracks the versions it has seen from the others. This collection — the version vector — distinguishes overwrite from concurrency, making it safe to read from one replica and write back to another (siblings may result, but nothing is lost if merged correctly). Riak 2.0 uses the dotted version vector variant, shipped to clients as an opaque *causal context* string. Version vectors are loosely called [[Vector Clocks]], but they differ subtly; for comparing replica states, version vectors are the right structure.

## Trade-offs & Pitfalls

- LWW = convergence purchased with silent data loss; version vectors = no loss, but clients must merge.
- Forgetting tombstones turns every merge into a resurrection bug.

## Examples & Systems

Cassandra (LWW-only), Riak (optional LWW, siblings, CRDTs, dotted version vectors), Amazon's Dynamo cart example.

## Related

- up: [[Leaderless Replication]] · chapter: [[Ch 05 - Replication]]
- [[Handling Write Conflicts]] — the multi-leader twin of this problem
- [[Multi-Leader Replication Topologies]] — where causal ordering first broke down
- [[Ordering and Causality]] — happens-before generalized in Chapter 9

## Related in the other wiki
- [[message-key-partitioning-strategies]] — Kafka sidesteps this note's concurrent-write problem by construction rather than detection: routing every message for a given key to one partition, consumed by exactly one consumer, gives that key a single sequential writer, so there is no concurrent write to reconcile with version vectors in the first place.
