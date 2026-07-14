---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
topic: Relational Model Versus Document Model
type: subtopic
tags: [ddia, orm, document-model, json]
sources:
  - raw/ch02.md
---
# The Object-Relational Mismatch
> Application code thinks in objects while relational databases think in rows — the translation layer between them is friction that document models try to remove.

## The Idea
Most modern applications are written in object-oriented languages, but a relational database stores flat rows in tables. Every read and write therefore crosses a boundary where object graphs must be disassembled into rows and reassembled again. Kleppmann calls this disconnect an *impedance mismatch* — a metaphor borrowed from electronics, where mismatched circuit impedances waste power at the connection point. ORM frameworks (ActiveRecord, Hibernate) shrink the boilerplate but cannot make the two models identical.

## How It Works
The running example is a résumé (a LinkedIn-style profile). Scalar fields (name) map cleanly to columns, but a person has *many* jobs, *several* education entries, and *variable* contact details — one-to-many relationships. A relational schema has three ways to hold these:

1. **Classic normalization (pre-SQL:1999):** separate `positions`, `education`, and `contact_info` tables, each carrying a foreign key back to `users`.
2. **Structured column types:** later SQL standards added XML (and several vendors added JSON) columns that can hold multi-valued data inside a single row *and* remain queryable/indexable.
3. **Opaque blob:** serialize the nested parts as JSON/XML text in a string column, leaving interpretation entirely to the application — the database can't see inside.

Because a résumé is a mostly self-contained tree of one-to-many relationships, a single JSON document captures it naturally. That gives the document version *locality*: one query retrieves the whole profile, whereas the normalized version needs several queries or a multi-way join. The nested arrays make the implicit tree structure of the data explicit.

## Trade-offs & Pitfalls
- Reduced impedance mismatch is a genuine but partial win — JSON has its own encoding problems (taken up in [[JSON, XML, and Binary Variants]]).
- Schemalessness is often advertised as a benefit, but it is better understood as *schema-on-read* (see [[Relational Versus Document Databases Today]]).
- The document advantage holds for tree-shaped, load-it-all-at-once data; it erodes as soon as records need to reference each other (see [[Many-to-One and Many-to-Many Relationships]]).

## Examples & Systems
ORMs: ActiveRecord, Hibernate. Vendors with structured XML/JSON column support: Oracle, IBM DB2, SQL Server, PostgreSQL, MySQL. Document databases built around this model: MongoDB, RethinkDB, CouchDB, and LinkedIn's Espresso.

## Related
- up: [[Relational Model Versus Document Model]] · chapter: [[Ch 02 - Data Models and Query Languages]]
- [[Many-to-One and Many-to-Many Relationships]] — where the document tree breaks down
- [[The Birth of NoSQL]] — schema frustration as a NoSQL driver
- [[Formats for Encoding Data]] — serialization side of the same boundary
