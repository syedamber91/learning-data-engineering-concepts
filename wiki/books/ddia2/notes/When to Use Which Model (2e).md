---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
topic: Relational Versus Document Models
type: subtopic
tags: [ddia2, schema-on-read, schema-on-write, locality, convergence, aggregation-pipeline]
sources:
  - raw/ch03.md
---
# When to Use Which Model
> Document if your data is a tree you load whole; relational if you need to reference things directly. And increasingly, both — in the same database.

## The Idea
The main arguments for the document model are **schema flexibility**, **better performance due to locality**, and that for some applications it is **closer to the object model** the application uses. The relational model counters with **better support for joins and many-to-one and many-to-many relationships**.

If your data has a document-like structure — a tree of one-to-many relationships where the entire tree is typically loaded at once — a document model is probably a good idea. The relational technique of **shredding** (splitting a document-like structure into multiple tables) can lead to cumbersome schemas and unnecessarily complicated application code.

## How It Works
**Document model limitations.** You cannot refer directly to a nested item within a document; you have to say something like "the second item in the list of positions for user 251." If you need to reference nested items, relational works better, since anything can be referred to directly by ID. On the other hand, some applications let users choose item order — a to-do list or issue tracker with drag-and-drop reordering — and the document model supports this well, because items or their IDs simply sit in a JSON array that determines order. Relational databases have **no standard way** to represent reorderable lists, and various tricks are used: sorting by an integer column (requiring renumbering on insert into the middle), maintaining a linked list of IDs, or **fractional indexing**.

**Schema flexibility.** Most document databases and JSON support in relational databases enforce no schema (XML support usually comes with optional schema validation). No schema means arbitrary keys and values can be added, and readers have no guarantees about which fields a document contains. Calling document databases **schemaless** is misleading, since the reading code usually assumes some structure — there is an *implicit* schema, just not one the database enforces. The accurate term is **schema-on-read** (structure implicit, interpreted at read time) in contrast to **schema-on-write** (the traditional relational approach: schema explicit, database enforces conformance at write time). Schema-on-read resembles dynamic runtime type checking; schema-on-write resembles static compile-time checking — and just as with types, this is a contentious topic with no clear winner.

The difference shows most when changing data format. To split a single `name` field into `first_name` and `last_name`: in a document database you just start writing new documents with the new fields and add read-time code handling old documents (`if (user && user.name && !user.first_name) { user.first_name = user.name.split(" ")[0]; }`). The downside is that every part of the application reading from the database now has to handle old formats, possibly written long ago. In a schema-on-write database you run a migration (`ALTER TABLE users ADD COLUMN first_name text DEFAULT NULL;` then an `UPDATE`). Adding a column with a default is fast and unproblematic in most relational databases even on large tables, but the `UPDATE` is likely slow on a large table since every row is rewritten, and other schema operations such as changing a column's datatype typically require copying the whole table. Tools exist to do such changes in the background without downtime, but large-database migrations remain operationally challenging — and complicated migrations can be avoided by adding the column with a `NULL` default (fast) and **filling it in at read time, exactly as a document database would**.

Schema-on-read is advantageous when items in the collection **don't all have the same structure**: there are many types of object and it isn't practical to give each its own table, or the structure is determined by external systems you don't control and that may change at any time. In those situations a schema may hurt more than it helps. When all records are expected to have the same structure, schemas are a useful mechanism for documenting and enforcing it.

**Data locality for reads and writes.** A document is usually stored as a single continuous string encoded as JSON, XML, or a binary variant such as MongoDB's BSON. If the application often needs the whole document — to render a web page — this storage locality is a performance advantage; data split across tables requires multiple index lookups, which may mean more disk seeks and more time. But **the advantage applies only if you need large parts of the document at once**: the database typically loads the entire document, which is wasteful if you need a small part of a large one, and updates usually rewrite the whole document. Hence the recommendation to keep documents fairly small and avoid frequent small updates. Locality is also **not exclusive to the document model**: Google's Spanner offers the same properties in a relational model by letting the schema declare that a table's rows be interleaved (nested) within a parent table; Oracle does it with multi-table index cluster tables; and the wide-column model popularised by Bigtable and used in HBase and Accumulo has **column families** for the same purpose.

**Query languages for documents.** Most relational databases use SQL; document databases vary — some allow only key-value access by primary key, others offer secondary indexes into document values, and some provide rich query languages. XML databases use **XQuery** and **XPath**, designed for complex queries including joins across documents, formatting results as XML; **JSON Pointer** and **JSONPath** are the JSON equivalents of XPath. MongoDB's **aggregation pipeline** is a query language for JSON document collections. The book's comparison: a shark-sightings-per-month report is a `SELECT date_trunc('month', …) … GROUP BY` in PostgreSQL and a `$match` + `$group` pipeline in MongoDB. The aggregation pipeline is similar in expressiveness to a subset of SQL but uses JSON-based syntax rather than SQL's English-sentence style — the difference is perhaps a matter of taste.

## Trade-offs & Pitfalls
**Convergence of document and relational databases.** They started as very different approaches and have grown more similar. Relational databases added JSON types and query operators and the ability to index properties inside documents; some document databases — MongoDB, Couchbase, RethinkDB — added joins, secondary indexes, and declarative query languages. This is good news for developers, because **the two models work best when you can combine both in the same database**: many document databases need relational-style references between documents, and many relational databases have sections where schema flexibility helps. Relational–document hybrids are a powerful combination.

## Examples & Systems
BSON; Spanner's interleaved tables; Oracle's multi-table index cluster tables; Bigtable/HBase/Accumulo column families; XQuery, XPath, JSON Pointer, JSONPath, MongoDB's aggregation pipeline; fractional indexing for reorderable lists.

## Since the 1st Edition
This subtopic consolidates several 1st-edition sections — [[Relational Versus Document Databases Today]], the schema-flexibility and locality discussions, and [[Are Document Databases Repeating History]] — into one decision-focused note. **New material:** reorderable lists and fractional indexing, the worked schema-migration comparison with actual SQL and JavaScript, the observation that you can get document-style read-time filling in a relational database too, and Spanner/Oracle/column-family locality as non-document ways to get locality. The convergence argument is stated far more confidently than in 2017, when it was still a prediction.

## Related
- up: [[Relational Versus Document Models (2e)]] · chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[The Merits of Schemas (2e)]] — schema evolution treated properly, in the encoding chapter
- [[Storing Values Within the Index (2e)]] — locality at the storage-engine level
- 1st edition: [[Relational Versus Document Databases Today]] — the closest predecessor
