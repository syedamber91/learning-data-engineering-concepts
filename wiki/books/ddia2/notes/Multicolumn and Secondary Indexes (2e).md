---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
topic: Storage and Indexing for OLTP
type: subtopic
tags: [ddia2, secondary-index, primary-key, postings-list]
sources:
  - raw/ch04.md
---
# Multicolumn and Secondary Indexes
> A secondary index is a key-value index whose keys aren't unique. That one difference is the whole design problem.

## The Idea
Everything so far has been **key-value indexes**, equivalent to primary-key indexes in the relational model. A **primary key** uniquely identifies one row in a relational table, one document in a document database, or one vertex in a graph database; other records refer to it by primary key (or ID), and the index resolves such references.

**Secondary indexes** are also very common. In relational databases you create several on the same table with `CREATE INDEX`, letting you search by columns other than the primary key. In the résumé schema from Chapter 3, you would most likely have a secondary index on the `user_id` columns so you can find all the rows belonging to one user in each table.

## How It Works
A secondary index is easily constructed from a key-value index. **The main difference is that the indexed values are not necessarily unique** — there might be many rows, documents, or vertices under the same index entry. Two ways to solve this:
- Make each **value in the index a list of matching row identifiers**, like a postings list in a full-text index.
- Make each **entry unique by appending a row identifier** to it.

**Both storage-engine families can implement an index**: in-place-update engines like B-trees and log-structured storage both work.

## Trade-offs & Pitfalls
- The postings-list approach and the append-row-ID approach make different trade-offs between entry size and update cost; the book notes both without declaring a winner, because the right choice depends on the engine.
- Indexes on multiple columns simultaneously are a different problem, deferred to [[Multidimensional and Full-Text Indexes (2e)]] — the indexes described here still map a single key to a value.

## Examples & Systems
`CREATE INDEX` in relational databases; postings lists borrowed conceptually from full-text indexing.

## Since the 1st Edition
This is the first half of the 1st edition's [[Other Indexing Structures]], separated into its own subtopic. The content — non-unique index entries, postings lists versus appended row IDs — is essentially unchanged; the 2nd edition simply gives it room and defers multi-column querying to a proper topic later in the chapter rather than covering it in passing.

## Related
- up: [[Storage and Indexing for OLTP (2e)]] · chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Storing Values Within the Index (2e)]] — what the index entry actually points at
- [[Multidimensional and Full-Text Indexes (2e)]] — querying several columns at once
- [[Sharding and Secondary Indexes (2e)]] — the same structures once the data is sharded
- 1st edition: [[Secondary Indexes]] and [[Other Indexing Structures]] — the closest predecessors
