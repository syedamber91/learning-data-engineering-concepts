---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
topic: Relational Versus Document Models
type: subtopic
tags: [ddia2, many-to-many, join-table, secondary-index, document-model]
sources:
  - raw/ch03.md
---
# Many-to-One and Many-to-Many Relationships
> One-to-many fits in a document. Many-to-one and many-to-many don't, and that is the document model's real boundary.

## The Idea
The `positions` and `education` tables are **one-to-many** (or one-to-few): one résumé has several positions, but each position belongs to only one résumé. The `region_id` field is **many-to-one**: many people live in the same region, but each person lives in only one region at a time. Introduce entities for organizations and schools and reference them by ID from the résumé, and you also have **many-to-many** relationships — one person may have worked for several organizations, and an organization has many past or present employees.

## How It Works
- In the relational model, a many-to-many relationship is usually an **associative table** (or **join table**): each position row associates one user ID with one organization ID.
- Many-to-one and many-to-many relationships **do not fit easily within one self-contained JSON document**; they lend themselves to a normalized representation. In a document model, the résumé's own data can be one document while links to organizations and schools are references to other documents.
- Many-to-many relationships often need querying **in both directions** — all organizations a person has worked for, and all people who have worked at an organization. One way to support this is to **store ID references on both sides**: the résumé lists each organization's ID, and the organization document lists the IDs of résumés mentioning it. This is denormalized, because the relationship is stored in two places, which can become inconsistent.
- A **normalized** representation stores the relationship in only one place and relies on **secondary indexes** to query it efficiently in both directions. In the relational schema you index both the `user_id` and `org_id` columns of the `positions` table. In the document model you need the database to index the `org_id` field of objects *inside* the `positions` array — and many document databases, and relational databases with JSON support, can create such indexes on values inside a document.

## Trade-offs & Pitfalls
- The bidirectional-query requirement is what forces the choice. Storing references on both sides is the tempting shortcut and the classic source of drift between two copies of one relationship.
- Indexing inside a nested array is the capability that makes normalized many-to-many workable in a document store; without it, the document model pushes you toward duplication.

## Examples & Systems
Associative/join tables in the relational model; indexes on `positions[].org_id` in document databases and JSON-capable relational databases.

## Since the 1st Edition
The 1st edition's [[Many-to-One and Many-to-Many Relationships]] made the same distinctions with the same résumé example. **New here:** the explicit both-directions query requirement, the both-sides-references denormalization and its inconsistency risk, and the observation that indexing values inside a document array is what makes the normalized option viable in document databases. The 1st edition instead spent this subtopic on the historical hierarchical/network-model comparison, which the 2nd edition compresses and moves.

## Related
- up: [[Relational Versus Document Models (2e)]] · chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[Graph-Like Data Models (2e)]] — what to reach for when many-to-many dominates
- [[Multicolumn and Secondary Indexes (2e)]] — the index machinery this depends on
- 1st edition: [[Many-to-One and Many-to-Many Relationships]] — the same subtopic
