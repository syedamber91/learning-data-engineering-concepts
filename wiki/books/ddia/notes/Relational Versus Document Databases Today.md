---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
topic: Relational Model Versus Document Model
type: subtopic
tags: [ddia, schema-on-read, data-locality, document-model]
sources:
  - raw/ch02.md
---
# Relational Versus Document Databases Today
> Choose by data shape: document wins for self-contained trees, relational wins for interconnected data — and the two are converging anyway.

## The Idea
Setting aside fault tolerance (Chapter 5) and concurrency (Chapter 7), the data-model contest comes down to: documents offer schema flexibility, locality-driven read performance, and closeness to application object structures; relational systems offer real joins and solid many-to-one/many-to-many support.

## How It Works
**Which model gives simpler code?** Depends on the relationships in your data. Tree-shaped data usually loaded whole fits documents; forcing it into tables (*shredding* into `positions`/`education`-style side tables) yields clunky schemas and extra code. But documents can't address nested items directly (you point at "position number 2 of user X" — an access-path smell), and weak join support bites once many-to-many links appear: you either denormalize and then labor to keep copies consistent, or emulate joins in application code, which is slower than the database's specialized join machinery. Rule of thumb: highly interconnected data — document awkward, relational acceptable, graph most natural.

**Schema flexibility.** "Schemaless" is a misnomer: readers always assume some structure, so the schema is implicit. The honest distinction is *schema-on-read* (structure interpreted at read time, like dynamic typing) versus *schema-on-write* (database enforces structure on ingest, like static typing) — a debate with no universal answer. Format changes illustrate it: splitting a `name` field into first/last names means, in a document store, writing new-style documents and adding read-time code that patches old ones; in a relational store, an `ALTER TABLE` plus a backfilling `UPDATE`. Most databases run `ALTER TABLE` in milliseconds (MySQL is the exception — it copies the whole table, though tools work around it); the row-rewriting `UPDATE` is slow anywhere, and you can defer it by defaulting to NULL and filling on read. Schema-on-read shines when records are genuinely heterogeneous — many object types, or structure dictated by changeable external systems; explicit schemas shine when uniformity is expected (more in [[The Merits of Schemas]]).

**Locality.** A document stored as one contiguous encoded string (JSON, XML, or a binary form like BSON) is fast to fetch whole; multi-table layouts need multiple index lookups and disk seeks. But the win only applies when you need most of the document: databases typically load — and on update rewrite — the *entire* document, so keep documents small and avoid size-growing writes. Locality isn't document-exclusive: Spanner interleaves child rows inside parent tables, Oracle offers multi-table index cluster tables, and Bigtable's column families (Cassandra, HBase) group data similarly.

**Convergence.** Relational systems added XML then JSON support (PostgreSQL 9.3+, MySQL 5.7+, IBM DB2 10.5+); RethinkDB does relational-style joins, and some MongoDB drivers resolve references client-side. Hybrid databases that do both are the likely future — the models complement each other.

## Trade-offs & Pitfalls
Document + many-to-many = complex, slow application code. Big documents waste I/O. Codd himself foresaw nested values ("nonsimple domains") — the ideas were never truly opposed.

## Related
- up: [[Relational Model Versus Document Model]] · chapter: [[Ch 02 - Data Models and Query Languages]]
- [[Schema Evolution]] — schema change handling, expanded in Chapter 4
- [[Column-Oriented Storage]] — a different locality strategy for analytics
- [[Graph-Like Data Models]] — the escape hatch for interconnected data
- [[Denormalization]] — the cost of avoiding joins
