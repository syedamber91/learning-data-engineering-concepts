---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
type: topic
tags: [ddia, isolation-levels, concurrency, race-conditions]
sources:
  - raw/ch07.md
---
# Weak Isolation Levels

Serializable isolation would let every transaction pretend it runs alone, but its performance cost means most databases ship weaker [[Isolation Levels]] that block *some* race conditions and quietly permit others. That gap is dangerous precisely because concurrency bugs are timing-dependent: they evade testing, resist reproduction, and have caused real money loss, auditor investigations, and corrupted customer data — and "just use an ACID database" is no defense, since even flagship relational databases run weak isolation by default. This topic builds a taxonomy of the anomalies, from the ones read committed stops (dirty reads, dirty writes) through the ones snapshot isolation stops (read skew), to the write-write conflicts that survive both: lost updates, and the subtler write skew, where phantoms make even row locking insufficient. Knowing exactly which anomaly each level does and doesn't prevent is what lets you choose a level deliberately instead of by folklore.

## Subtopics

- [[Read Committed]] — the baseline: no dirty reads (you never see uncommitted data) and no dirty writes (you never overwrite uncommitted data), via row locks for writers and old-value memory for readers.
- [[Snapshot Isolation and Repeatable Read]] — each transaction reads a frozen, consistent snapshot, fixing read skew for backups and analytics; implemented with MVCC under the mantra "readers never block writers, writers never block readers," and sold under wildly inconsistent names.
- [[Preventing Lost Updates]] — the read-modify-write clobbering problem and its toolbox: atomic operations, explicit `FOR UPDATE` locks, automatic detection, compare-and-set, and why none of these survive multi-leader replication unchanged.
- [[Write Skew and Phantoms]] — two transactions read the same data and update *different* objects, invalidating each other's premise (the on-call doctors); phantoms extend this to rows that don't exist yet, defeating `SELECT FOR UPDATE`.

## Key Takeaways

- Weak isolation levels are not a theoretical concern — the anomalies they permit have produced concrete production losses, and popular "ACID" databases default to them.
- Each level is best understood by the anomaly it rules out: read committed kills dirty reads/writes; snapshot isolation additionally kills read skew; lost updates need extra machinery even under snapshot isolation; write skew and phantoms fall only to true [[Serializability]].
- Write skew generalizes the lost update: same reads, disjoint writes, so neither dirty-write locks nor lost-update detection fire — the conflict is invisible at the level of individual objects.
- The phantom pattern (check a condition, then write something that changes that condition's result set) underlies double-booking, username races, and double-spending; materializing conflicts as lock rows is a last-resort workaround.
- Naming is treacherous: Oracle calls snapshot isolation "serializable," PostgreSQL/MySQL call it "repeatable read," DB2 uses "repeatable read" for serializability — the SQL standard's definitions are too ambiguous to arbitrate, so nobody really knows what repeatable read means.
- On replicated databases with multiple writers, single-copy techniques (locks, compare-and-set) stop applying; commutative atomic operations and sibling-merging take their place, while last-write-wins silently drops updates.

## Related

- chapter: [[Ch 07 - Transactions]]
- [[The Slippery Concept of a Transaction]] — the ACID isolation promise these levels water down
- [[Serializability]] — the strong level that eliminates every anomaly catalogued here
- [[Detecting Concurrent Writes]] — the leaderless-replication version of the same write-conflict problem
- [[Handling Write Conflicts]] — multi-leader conflict resolution, where lost-update prevention must be rethought
- [[Transaction Processing or Analytics]] — the long-scan workloads that make consistent snapshots essential
- [[transactions]] (vutr wiki) — the same read-committed/snapshot-isolation/MVCC ladder from a working data engineer's real posts, including PostgreSQL's concrete UPDATE-as-new-row-version mechanics this chapter describes more abstractly
