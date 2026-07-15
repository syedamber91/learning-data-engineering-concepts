---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, data-modeling]
sources:
  - raw/ch02.md
  - raw/ch07.md
---
# Denormalization

Deliberately duplicating data (precomputed joins, redundant columns, cached
aggregates) so reads are fast at the cost of harder writes — every copy must be
updated when the source changes. The opposite instinct of relational normalization,
where each fact lives exactly once.

In the book: document models encourage it ([[Relational Model Versus Document Model]]), warehouses embrace it ([[Stars and Snowflakes - Schemas for Analytics]]),
and Part III reframes it: a denormalized value is just [[Derived Data]], safe as
long as a reliable pipeline ([[Change Data Capture]], stream processing) keeps it in
sync with the system of record.

## Referenced In
- [[Aggregation - Data Cubes and Materialized Views]]
- [[Ch 02 - Data Models and Query Languages]]
- [[Ch 07 - Transactions]]
- [[Many-to-One and Many-to-Many Relationships]]
- [[Other Indexing Structures]]
- [[Reduce-Side Joins and Grouping]]
- [[Relational Model Versus Document Model]]
- [[Relational Versus Document Databases Today]]
- [[Single-Object and Multi-Object Operations]]
- [[Stars and Snowflakes - Schemas for Analytics]]
- [[State, Streams, and Immutability]]
- [[The Slippery Concept of a Transaction]]
