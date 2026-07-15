---
persona: vutr
kind: concept
sources:
- raw/duckdb-polars-single-node-engines/i-made-110-in-duckdb.md
last_updated: '2026-07-15'
qc: passed
slug: duckdb-acid-and-mvcc
topics:
- single-node-engines-duckdb-polars-vs-distributed-systems
---

ACID is the standard four-part guarantee: **Atomicity** — transactions are either fully completed or not at all, no in-between states; **Consistency** — the database moves from one valid state to another, preserving defined rules and constraints; **Isolation** — concurrent transactions don't interfere with each other and can each execute as if independent; **Durability** — committed transactions persist even through system failures.

With OLTP databases like PostgreSQL or MySQL, enforcing ACID has always been a must-have for data integrity. The claim worth sitting with is that it's the same story for OLAP: an OLAP system now acts as a critical endpoint for business data analytics, and it usually serves as a shared environment for multiple users at once — data analysts, data scientists, data engineers, business users. The rhetorical challenge that makes the point sharpest: if ACID were genuinely unnecessary in the OLAP world, why would open table formats like Delta Lake or Apache Iceberg exist specifically to make object storage more... ACID?

DuckDB's answer is a custom, bulk-optimized Multi-Version Concurrency Control (MVCC) implementation, which is how it provides transactional (ACID) guarantees despite being an embedded, single-process analytical engine rather than a client-server OLTP system.

## Related in the other wiki
- [[ACID]] — DDIA's definition of the same four-letter guarantee (atomicity, consistency, isolation, durability) that this note grounds in DuckDB's specific MVCC implementation and the broader argument that OLAP needs it too.

*See also: [[duckdb-embedded-analytics-model]] · [[vectorized-execution-engine]]*
