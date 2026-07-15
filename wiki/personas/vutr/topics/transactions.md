---
persona: vutr
kind: topic
sources:
- raw/transactions
last_updated: '2026-07-15'
qc: passed
topic: transactions
---

Related: [[isolation-levels-and-mvcc]]

## Overview
This topic covers the OLTP transaction-isolation ladder — read committed, snapshot isolation, and serializability — and the MVCC (multi-version concurrency control) mechanism that makes snapshot isolation possible, grounded in vutr's own posts on ACID for data engineers and OLTP-vs-OLAP data mutation. It's a deliberately narrow topic: two posts, one concept note, filling a gap that nothing else in this wiki covered (the rest of the wiki's ACID coverage is OLAP-flavored — see [[acid-in-olap]] and [[cap-vs-acid-consistency]] — not classic OLTP concurrency control).

## Open questions
- **source gap**: the two source posts don't cover the anomaly PostgreSQL calls "write skew" beyond the meeting-room example, nor do they touch two-phase locking's practical throughput cost or how serializable snapshot isolation (SSI) actually detects a conflicting read-write pattern at commit time — [[isolation-levels-and-mvcc]] names these mechanisms but the sources stop short of their implementation detail.
- Neither post discusses distributed transactions (2PC, cross-shard atomicity) at all — this topic is scoped to single-node isolation semantics only. See [[raft-backed-coordination]] and [[cap-vs-acid-consistency]] for the distributed-systems side of consistency this wiki does cover.

## Synthesis
The throughline across both sources is that isolation strength and locking cost trade off directly: read committed's row-locks-plus-two-versions is cheap but leaves non-repeatable reads open; snapshot isolation's full version lineage (MVCC) closes that at the cost of write locks and a background vacuum/garbage-collection job; serializability closes the last gap (write skew) either pessimistically (2PL, which stalls reads behind writes) or optimistically (SSI, which aborts and retries instead of blocking). PostgreSQL's UPDATE-as-insert-new-version-mark-old-dead mechanics are what make MVCC concrete rather than abstract — every one of these guarantees is paid for in extra row versions that something eventually has to clean up.

## Related topics
- [[consensus]] — a different axis of "which answer is the true one under concurrency": that topic covers agreement across machines (Raft, leader election); this topic covers agreement across concurrent transactions on one machine (isolation levels, MVCC).
- [[acid-in-olap]] — the OLAP-world version of the same ACID acronym, where the mechanisms (MVCC-based transactions in Snowflake/DuckDB) turn out to overlap with the OLTP mechanics this topic covers in depth.
- [[cap-vs-acid-consistency]] — untangles ACID consistency (constraints not violated) from CAP consistency (linearizability), the confusion this topic's own MVCC/isolation-level material sits adjacent to.
- [[Weak Isolation Levels]] (DDIA book) — the same read-committed/snapshot-isolation ladder from the book's-eye view, with the formal anomaly taxonomy (dirty reads/writes, non-repeatable reads, write skew, phantoms) this topic's sources name but don't fully catalog.
- [[Serializability]] (DDIA book) — the book's treatment of 2PL and SSI as the two paths to serializability, matching the mechanisms [[isolation-levels-and-mvcc]] names from vutr's own posts.
