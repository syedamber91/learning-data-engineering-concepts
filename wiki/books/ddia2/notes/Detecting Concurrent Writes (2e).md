---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Leaderless Replication
type: subtopic
tags: [ddia2, happens-before, concurrency, version-vector, siblings, vector-clock]
sources:
  - raw/ch06.md
---
# Detecting Concurrent Writes
> Two operations are concurrent if neither happens before the other. Not "at the same time" — *neither knew about the other*. That definition is the whole algorithm.

## The Idea
Like multi-leader replication, leaderless databases allow concurrent writes to the same key, producing conflicts that need resolving. **Such conflicts might be detected as the writes happen, but not always** — they could also surface later, during read repair, hinted handoff, or anti-entropy.

The problem is that **events may arrive in a different order at different nodes**, because of variable network delays and partial failures. Two clients A and B write to key X in a three-node store: node 1 receives A's write but never B's because of a transient outage; node 2 receives A then B; node 3 receives B then A. **If each node simply overwrote the value on each incoming write, the nodes would become permanently inconsistent** — node 2 thinking the final value is B while the others think it is A.

To become eventually consistent, replicas must **converge toward the same value**, using any of the conflict resolution mechanisms already covered: **LWW** (used by Cassandra and ScyllaDB), manual resolution, or **CRDTs** (used by Riak). LWW is easy to implement — each write tagged with a timestamp, higher timestamp wins — **but a timestamp doesn't tell you whether two values are actually conflicting** (written concurrently) or not (written one after another). **To resolve conflicts explicitly, the system must take more care to detect concurrent writes.**

## How It Works
**The happens-before relation.** Consider two examples. When A inserts a row and B increments that row's value, **the two are not concurrent**: B's operation builds upon A's — the value B incremented is the value A inserted — so B must have happened later. **B is causally dependent on A.** When two clients each write a key without knowing the other is also writing it, the operations **are concurrent**: there is no causal dependency.

**An operation A happens before another operation B if B knows about A, or depends on A, or builds upon A in some way.** And then the definition that matters: **two operations are concurrent if neither happens before the other.** So for any two operations there are exactly three possibilities: A happened before B, B happened before A, or they are concurrent. **If one happened before the other, the later should overwrite the earlier; if they are concurrent, we have a conflict to resolve.**

> **Concurrency, time, and relativity.** It may seem two operations should be called concurrent if they occur "at the same time" — **but it is not important whether they literally overlap in time.** Because of clock problems in distributed systems it is actually quite difficult to tell whether two things happened at exactly the same moment. **For defining concurrency, exact time doesn't matter: two operations are concurrent if they are both unaware of each other, regardless of physical time.** People sometimes connect this to special relativity, where information cannot travel faster than light, so two events far enough apart in space and close enough in time cannot affect each other. **In computer systems two operations might be concurrent even though the speed of light would have allowed one to affect the other** — if the network was slow or interrupted, operations can occur some time apart and still be concurrent, because the network prevented one from knowing about the other.

**Capturing the happens-before relationship — single replica first.**
- The server **maintains a version number for every key**, increments it on every write, and stores the new version number with the value written.
- When a client reads a key, the server returns **all siblings** — all values not overwritten — **plus the latest version number**. **A client must read a key before writing.**
- When a client writes, it **must include the version number from the prior read**, and **must merge together all values it received in that read**. The write response also returns all siblings, allowing several writes to be chained.
- When the server receives a write with a particular version number, it can **overwrite all values with that version number or below** (knowing they have been merged into the new value) **but must keep all values with a higher version number**, because those are concurrent with the incoming write.

**The server can determine concurrency purely from version numbers — it does not need to interpret the value itself**, so the value can be any data structure. Including a version number tells the server which previous state the write is based on; **a write without a version number is concurrent with all other writes, so it overwrites nothing and just becomes another sibling.**

The book's worked shopping-cart example runs five writes across two clients: client 1 adds milk (v1); client 2 adds eggs unaware of milk, so the server stores `eggs` and `milk` as siblings and returns both at v2; client 1, still unaware, sends `[milk, flour]` at v1, which supersedes `[milk]` but is concurrent with `[eggs]`, so the server assigns v3 and keeps `[eggs]`; client 2 merges what it saw and sends `[eggs, milk, ham]` at v2, overwriting `[eggs]` but concurrent with `[milk, flour]`; finally client 1 merges and sends `[milk, flour, eggs, bacon]` at v3, overwriting `[milk, flour]` but concurrent with `[eggs, milk, ham]`. **In this example the clients are never fully up to date, since there is always another operation going on concurrently — but old versions do get overwritten eventually, and no writes are lost.**

**Version vectors — multiple replicas.** A **single** version number is not sufficient when multiple replicas accept writes concurrently. Instead you need **a version number per replica as well as per key**: each replica increments its own version number when processing a write **and also tracks the version numbers it has seen from each of the other replicas**. This information indicates which values to overwrite and which to keep as siblings.

**The collection of version numbers from all replicas is called a version vector.** Several variants exist; **the most interesting is probably the dotted version vector**, used in Riak 2.0. Like single version numbers, **version vectors are sent from replicas to clients on reads and must be sent back on subsequent writes** — Riak encodes the version vector as a string it calls **causal context**. The version vector lets the database **distinguish between overwrites and concurrent writes**, and **ensures it is safe to read from one replica and write back to another**: doing so may create siblings, **but no data is lost as long as siblings are merged correctly.**

## Trade-offs & Pitfalls
- **Version vectors are not vector clocks**, though the terms get conflated. The difference is subtle; **in brief, when comparing the state of replicas, version vectors are the right data structure to use.**
- The requirement that **a client must read before it writes** is a real API constraint, and the reason leaderless conflict handling leaks into application code.

## Examples & Systems
Riak 2.0's dotted version vectors and "causal context" string; Cassandra and ScyllaDB using LWW instead; the shopping-cart worked example.

## Since the 1st Edition
Very close to the 1st edition's [[Detecting Concurrent Writes]] — the same happens-before definition, the same relativity aside, the same five-step shopping cart, and the same version vector treatment including dotted version vectors and the vector-clock terminology note. One of the most stable sections in the chapter, which fits the book's own observation that replication principles haven't changed much since the 1970s.

## Related
- up: [[Leaderless Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Dealing with Conflicting Writes (2e)]] — what to do once a conflict is detected
- [[Causality (2e)]] — the cross-cutting concept note
- [[Logical Clocks (2e)]] — the same ordering problem in Chapter 10
- 1st edition: [[Detecting Concurrent Writes]] — the same subtopic
