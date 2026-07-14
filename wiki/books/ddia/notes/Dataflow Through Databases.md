---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 4
chapter_title: Encoding and Evolution
topic: Modes of Dataflow
type: subtopic
tags: [ddia, databases, data-outlives-code, migrations]
sources:
  - raw/ch04.md
---
# Dataflow Through Databases
> Writing to a database is sending a message to your future self — and because data outlives code, both backward and forward compatibility are required, plus care not to drop fields you don't understand.

## The Idea
The first mode of [[Dataflow]]: one process encodes a value into the database, another decodes it later. Even with a single process, the reader is a *future* version of the writer, so backward compatibility is non-negotiable — otherwise you can't read your own history. In realistic deployments many processes hit the database concurrently, and during a rolling upgrade some run new code while others run old. A value written by the *new* version can be read by *old* code, so forward compatibility is usually needed too.

## How It Works
The subtle hazard is the **read-modify-write round trip** (the book's Figure 4-7): new code writes a record containing a freshly added field; old code then reads the record, updates something else, and writes it back. The encoding formats from this chapter can preserve unknown fields — but if the application decodes into model objects that have no slot for the new field and then re-encodes those objects, the field silently vanishes. Not hard to solve, but you must know to solve it at the application layer.

**Data outlives code.** Deploying a new application version takes minutes; the data it wrote five years ago is still sitting on disk in its original encoding. Rewriting (migrating) a large dataset into a new schema is expensive, so databases avoid it: most relational systems let you add a column with a `null` default without touching existing rows, filling in nulls at read time when old rows lack the column. (MySQL is the exception — it often rewrites the whole table anyway.) LinkedIn's Espresso stores data as [[Avro]] precisely so Avro's resolution rules do this work. The net effect: [[Schema Evolution]] makes a database *appear* to have one schema even though the underlying bytes span many historical schema versions.

## Trade-offs & Pitfalls
- Forward compatibility is easy to forget for databases because it only bites during mixed-version windows — exactly when it's most confusing to debug.
- Migration cost pushes teams toward additive, default-valued changes; destructive changes deserve real hesitation.
- **Archival dumps are different**: a snapshot for backup or for a warehouse (see [[Data Warehousing]]) is written once and immutable, so encode it uniformly in the latest schema — Avro object container files fit well, or a column-oriented analytics format like Parquet (see [[Column Compression]]).

## Examples & Systems
Relational `ALTER TABLE` with null defaults, MySQL's table rewrites, LinkedIn Espresso (Avro storage), Avro object container files, Parquet for analytics dumps.

## Related
- up: [[Modes of Dataflow]] · chapter: [[Ch 04 - Encoding and Evolution]]
- [[Avro]] — the writer/reader resolution machinery Espresso relies on
- [[Data Warehousing]] — destination for latest-schema archival dumps
- [[Column Compression]] — why Parquet suits the analytics copy
