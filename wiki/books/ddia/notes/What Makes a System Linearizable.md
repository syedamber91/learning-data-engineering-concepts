---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
topic: Linearizability
type: subtopic
tags: [ddia, linearizability, registers, compare-and-set]
sources:
  - raw/ch09.md
---
# What Makes a System Linearizable?
> A system is linearizable if every operation on a register appears to take effect atomically at a single instant between its start and finish, and reads never travel backward in time.

## The Idea
"Behave like one copy of the data" sounds simple, but pinning it down takes care. The formal object of study is a *register* — one key, one row, one document. Clients issue requests and receive responses over a network with variable delay, so a client never knows exactly when the database processed its operation, only that it happened somewhere inside the request's time window. [[Linearizability]] constrains what values reads may return given those windows.

## How It Works
Three rules build up the definition:
1. **Non-overlapping operations respect real time.** A read that begins after a write completes must return the new value; a read that finishes before the write begins must return the old one.
2. **Concurrent reads may go either way — once.** A read overlapping a write may return old or new value. But the value cannot flap: the model imagines an atomic instant inside the write's window where the register flips. (A register where concurrent reads may return either value freely is merely a *regular* register — weaker.)
3. **No going backward.** The moment any client's read returns the new value, every read that *starts afterward* — on any client — must also return it, even if the write is still in flight.

Formally, you can test a history for linearizability: mark a point inside each operation's bar where it "took effect," and check that connecting those points left-to-right yields a valid sequential register history (every read returns the latest write). If no such assignment exists, the history is not linearizable. This check is possible but computationally expensive.

The model also includes atomic **compare-and-set**: cas(x, v_old, v_new) succeeds only if the register still holds v_old. Because the model assumes no transaction isolation, another client may change the value between your read and your cas — cas is how you detect that.

## Trade-offs & Pitfalls
- Requests being *sent* in some order proves nothing; only response-to-request precedence in real time constrains the order. Concurrent requests may be processed in any order.
- A client can observe a written value before the writer receives its own ok — that is legal (the ack was merely delayed).
- Do not confuse this with [[Serializability]]: linearizability orders single-object operations by recency; it does not group operations into transactions and cannot prevent [[Write Skew and Phantoms|write skew]] on its own. Strict serializability = both. Notably, [[Serializable Snapshot Isolation (SSI)]] is serializable but *not* linearizable, because snapshot reads deliberately exclude newer writes.

## Examples & Systems
The chapter's football-score story (Alice sees the result, Bob then reads a stale replica) is the archetypal violation. Kingsbury's Knossos checker tests real systems' histories this way; 2PL-based and serial-execution databases are typically linearizable.

## Related
- up: [[Linearizability]] · chapter: [[Ch 09 - Consistency and Consensus]]
- [[Serializability]] — the contrast that trips everyone up
- [[Serializable Snapshot Isolation (SSI)]] — serializable yet non-linearizable by design
- [[Ordering and Causality]] — the total order this definition induces
