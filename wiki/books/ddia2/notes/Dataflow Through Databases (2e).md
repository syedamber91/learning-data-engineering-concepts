---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 5
chapter_title: Encoding and Evolution
topic: Modes of Dataflow
type: subtopic
tags: [ddia2, database, data-outlives-code, migration, archival, parquet]
sources:
  - raw/ch05.md
---
# Dataflow Through Databases
> "Data outlives code." Your five-year-old rows are still in their original encoding, and something running today has to read them.

## The Idea
In a database, the process that writes encodes the data and the process that reads decodes it. If just one process accesses the database, the reader is simply a later version of the same process — **storing something in the database is like sending a message to your future self**, and backward compatibility is clearly necessary, or your future self can't decode what you wrote.

More commonly several processes access a database at once: different applications or services, or multiple instances of the same service running in parallel for scalability or fault tolerance. In such an environment **some processes will be running newer code and some older** — because a new version is being deployed in a rolling upgrade, for instance. So a value may be **written by a newer version and subsequently read by an older version that is still running**, which means **forward compatibility is also often required for databases**.

## How It Works
**Different values written at different times.** A database generally allows any value to be updated at any time, so within one database you may have values written five milliseconds ago and others written five years ago. When you deploy a new application version you may replace the old version entirely within minutes — **but the same is not true of database contents**. The five-year-old data is still there in its original encoding unless you have explicitly rewritten it. This is summed up as **data outlives code**.

Rewriting (migrating) data into a new schema is possible but **expensive on a large dataset**, so most databases defer the operation, performing it **asynchronously and on a best-effort basis**:
- **LSM-tree storage engines rewrite data using the latest format during compaction** — the maintenance work is already happening, so the migration rides along.
- Most relational databases allow simple schema changes, such as **adding a new column with a null default, without rewriting existing data**. When an old row is read, the database fills in nulls for columns missing from the encoded data on disk.

**Schema evolution thus allows the entire database to appear as if encoded with a single schema, even though the underlying storage contains records encoded with various historical versions.**

## Trade-offs & Pitfalls
- **The easy cases are the ones the database can fake.** More complex schema changes — changing a single-valued attribute to multivalued, or moving data into a separate table — **still require data to be rewritten, often at the application level**. And the book is candid that **maintaining forward and backward compatibility across such migrations remains a research problem.**
- **Archival storage** is the clean case. When you snapshot a database for backup or for loading into a data warehouse, the dump is typically **encoded using the latest schema**, even though the source contained a mixture of schema versions from different eras — since you are copying the data anyway, you might as well encode the copy consistently. Because the dump is written in one go and is thereafter immutable, **Avro object container files are a good fit**, and it is also a good opportunity to encode in an analytics-friendly **column-oriented format such as Parquet**.

## Examples & Systems
LSM compaction as an opportunistic migration path; `ALTER TABLE ... ADD COLUMN ... DEFAULT NULL` as the cheap relational schema change; Avro object container files and Parquet for archival dumps.

## Since the 1st Edition
Close to the 1st edition's [[Dataflow Through Databases]] — the message-to-your-future-self framing, "data outlives code," the null-default column trick, and archival storage all carry over. **Added:** the explicit note that **LSM-tree compaction is where format rewriting actually happens**, tying this back to Chapter 4, and the acknowledgement that compatibility across complex migrations is an open research problem.

## Related
- up: [[Modes of Dataflow (2e)]] · chapter: [[Ch 05 - Encoding and Evolution (2e)]]
- [[Log-Structured Storage (2e)]] — where the opportunistic rewrite happens
- [[When to Use Which Model (2e)]] — the schema-migration comparison in Chapter 3
- [[Avro (2e)]] — object container files for archival dumps
- 1st edition: [[Dataflow Through Databases]] — the same subtopic
