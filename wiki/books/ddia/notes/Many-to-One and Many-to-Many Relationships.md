---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
topic: Relational Model Versus Document Model
type: subtopic
tags: [ddia, normalization, joins, relationships]
sources:
  - raw/ch02.md
---
# Many-to-One and Many-to-Many Relationships
> IDs plus joins keep shared facts in one place; document trees struggle exactly where data starts referencing other data.

## The Idea
In the résumé example, region and industry are stored as opaque IDs rather than human-readable strings. This choice is really a question about *duplication*: an ID points at a single canonical copy of the human-meaningful value, while storing the text repeats that value in every record that mentions it. Standardized, ID-referenced lists buy you consistent spelling, disambiguation of same-named places, one-spot updates when a name changes, per-language localization, and smarter search (the region list can encode that Seattle sits inside Washington, which a raw string never reveals).

## How It Works
An ID is stable precisely because it means nothing to humans — the thing it identifies can be renamed without touching any referencing record. Human-meaningful data, by contrast, may need to change, and every duplicated copy must then be updated, costing extra writes and risking divergent copies. Eliminating that duplication is the essence of normalization; [[Denormalization]] is the deliberate reverse trade, revisited with [[Derived Data]] in Part III.

Normalization inherently creates many-to-one relationships (many profiles → one region), and resolving an ID back into displayable data requires a join. Relational databases make joins routine; document databases usually don't need them for pure trees, and their join support is weak or absent — MongoDB lacks joins, CouchDB only allows them in predeclared views, RethinkDB supports them. Without database joins, the application emulates them with multiple queries (workable for small, slow-changing lookup lists held in memory, but the join effort has merely moved into your code).

Data also grows *more* interconnected over time. Two illustrative feature additions: turning employers and schools from strings into first-class entities with their own pages and logos, and letting one user write a recommendation that must always show the recommender's current photo — hence a reference to their profile, not a copy. Both changes introduce many-to-many relationships: each résumé remains a document, but the links between documents demand references resolved by joins.

## Trade-offs & Pitfalls
- Storing strings instead of IDs feels simpler initially but silently denormalizes the data.
- Application-side join emulation shifts complexity and consistency burdens onto developers.
- A join-free design rarely stays join-free; new features tend to interconnect previously independent records.

## Examples & Systems
LinkedIn-style profiles, entity pages for companies/schools, user-to-user recommendations; join support compared across RethinkDB, MongoDB, CouchDB.

## Related
- up: [[Relational Model Versus Document Model]] · chapter: [[Ch 02 - Data Models and Query Languages]]
- [[Are Document Databases Repeating History]] — the 1970s faced the same problem
- [[Graph-Like Data Models]] — the natural home for many-to-many-heavy data
- [[Stars and Snowflakes - Schemas for Analytics]] — normalization in warehouse schemas
