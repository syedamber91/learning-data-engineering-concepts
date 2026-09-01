---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
type: topic
tags: [ddia2, serializability, isolation, concurrency-control]
sources:
  - raw/ch08.md
---
# Serializability
Some race conditions are prevented by read committed and snapshot isolation; **others are not**, and write skew and phantoms are particularly tricky. The book calls the resulting situation **sad**, for three reasons:

- **Isolation levels are hard to understand and inconsistently implemented** — the meaning of "repeatable read" varies significantly between databases.
- **It can be difficult to tell by looking at application code whether it is safe at a particular isolation level**, especially in a large application where you might not know everything happening concurrently.
- **There are no good tools to detect race conditions.** Static analysis may help in principle, **but research techniques have not yet found their way into practical use**, and testing for concurrency issues is hard because they are **nondeterministic — problems occur only if you get unlucky with the timing.**

**This is not a new problem.** It has been like this since the 1970s, when weak isolation levels were introduced. **All along, the answer from researchers has been simple: use serializable isolation.**

**Serializable isolation is the strongest level.** It guarantees that even though transactions may execute in parallel, **the end result is the same as if they had executed one at a time, serially.** So **if transactions behave correctly when run individually, they continue to do so when run concurrently — the database prevents all possible race conditions.**

**So why isn't everyone using it?** Because of how the implementations perform. Most databases providing serializability use one of three techniques.

## Subtopics
- [[Actual Serial Execution (2e)]] — literally run one transaction at a time, on one thread.
- [[Two-Phase Locking (2e)]] — for several decades the only viable option.
- [[Serializable Snapshot Isolation (2e)]] — optimistic concurrency control, and the newest of the three.

## Key Takeaways
- The three techniques map onto a **pessimism spectrum**: serial execution is pessimism taken to the extreme (an exclusive lock on the whole database, compensated by making transactions very fast), 2PL is conventionally pessimistic, and SSI is optimistic.
- **Serializability is a property, not an implementation.** The same guarantee arrives by three completely different routes with completely different performance profiles — which is why "is it serializable?" and "will it perform?" are separate questions.
- The historical answer — *just use serializable isolation* — was correct all along and impractical until recently; **SSI is what changed the calculation.**

## Since the 1st Edition
The 1st edition's [[Serializability]] topic made the same three-point complaint and named the same three implementation techniques. Substantively unchanged — the notable difference is the surrounding context, since the 2nd edition's chapter now continues into distributed transactions rather than ending here.

## Related
- chapter: [[Ch 08 - Transactions (2e)]]
- [[Weak Isolation Levels (2e)]] — everything this prevents
- [[Write Skew and Phantoms (2e)]] — the anomaly that requires this level
- 1st edition: [[Serializability]] — the same topic
