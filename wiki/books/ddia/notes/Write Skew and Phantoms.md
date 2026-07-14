---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
topic: Weak Isolation Levels
type: subtopic
tags: [ddia, write-skew, phantoms, race-conditions]
sources:
  - raw/ch07.md
---
# Write Skew and Phantoms
> Two transactions read the same data, make decisions on it, then write to *different* objects — invalidating each other's premise; when the check is for *absent* rows, the anomaly is a phantom and even row locks can't catch it.

## The Idea
**Anomaly: write skew.** The doctor on-call example: a hospital requires at least one doctor on call per shift. Alice and Bob, both on call and both ill, click "go off call" simultaneously. Each transaction checks the on-call count under snapshot isolation, sees 2, and proceeds; Alice updates *her* row, Bob updates *his*. Both commit — now zero doctors are on call. It's neither a dirty write nor a lost update, because they modified different rows; serially, the second request would have been refused. Write skew generalizes lost updates: same-object updates give lost update/dirty write, different-object updates give write skew.

**Anomaly: phantom.** Common pattern behind write-skew bugs: (1) a SELECT checks a requirement (enough doctors, room free, username untaken, balance positive); (2) app logic decides to proceed; (3) a write is made and committed — and that write changes what step 1 would return. When one transaction's write alters the *result set of another's search query*, that's a phantom. Snapshot isolation shields read-only queries from phantoms, but in read-write transactions phantoms enable the nastiest write-skew cases.

## How It Works
Defenses, roughly weakest to strongest:
- Atomic single-object ops: useless — multiple objects involved.
- Snapshot isolation's lost-update detection: doesn't fire (PostgreSQL repeatable read, MySQL/InnoDB, Oracle serializable, SQL Server snapshot all miss write skew).
- Multi-object constraints: most databases can't express "≥1 doctor on call"; triggers or [[Materialized Views]] may emulate it.
- `SELECT … FOR UPDATE`: works only when the rows the decision depends on *exist* to be locked (the doctors case). Checks for *absence* — a free room, an unclaimed username — return no rows, so there's nothing to lock.
- **Materializing conflicts**: manufacture lockable rows, e.g. a table of (room, 15-min slot) rows covering the next six months; a booking transaction locks the relevant slot rows first. The table stores no booking data — it's purely a lock surface. Ugly (concurrency control leaks into the schema), error-prone, and a last resort.
- True serializable isolation: the clean answer ([[Serializability]]).

## Trade-offs & Pitfalls
More write-skew scenarios: meeting-room double booking (overlap check + insert); two game figures moved onto one square (the per-figure lock from the lost-update fix doesn't help); duplicate username registration (here a unique constraint *does* save you); double-spending, where two concurrent tentative spends each see a positive balance. Write skew is easy to miss in review because each transaction looks correct in isolation.

## Examples & Systems
PostgreSQL, MySQL/InnoDB, Oracle, SQL Server (all fail to detect it at their snapshot levels); hospital on-call, meeting-room, username, multiplayer-game, double-spend examples; PostgreSQL range types for elegant overlap constraints.

## Related
- up: [[Weak Isolation Levels]] · chapter: [[Ch 07 - Transactions]]
- [[Preventing Lost Updates]] — the special case with same-object updates
- [[Two-Phase Locking (2PL)]] — predicate/index-range locks that finally stop phantoms
- [[Serializable Snapshot Isolation (SSI)]] — optimistic detection of outdated premises
