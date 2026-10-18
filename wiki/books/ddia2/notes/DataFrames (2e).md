---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Processing Models
type: subtopic
tags: [ddia2, dataframes, pandas, spark, daft, arrow]
sources:
  - raw/ch11.md
---
# DataFrames
> Data scientists already had an API they liked. Spark, Flink, and Daft adopted it — but the distributed version behaves differently in ways that surprise people.

## The Idea
**Data scientists and statisticians are generally used to the DataFrame model found in R and Pandas.** **A DataFrame is similar to a relational table: a collection of rows where all values in a column have the same type.** **Instead of writing one big SQL query, users call functions corresponding to relational operators** to filter, join, sort, aggregate, and so on.

**Originally DataFrame manipulation typically occurred locally, in memory, so DataFrames were limited to datasets fitting on a single machine.** **Data scientists wanted to work with the large datasets found in batch environments using the API they knew, since SQL and MapReduce are not well suited to their needs.** **Spark, Flink, and Daft have adopted DataFrame APIs to meet this need.**

## How It Works
- **The implementations behave somewhat differently: local DataFrames are usually indexed and ordered, while distributed DataFrames generally are not.** **This can lead to performance surprises when migrating to batch frameworks.**
- **DataFrame APIs appear similar to dataflow APIs, but implementations vary.** **Pandas executes operations immediately when DataFrame methods are called; Spark first translates all the API calls into a query plan and runs query optimization before executing on its distributed dataflow engine.**
- **Frameworks such as Daft even support both client- and server-side computation**: **smaller in-memory operations execute on the client, larger datasets on a server.** **Columnar formats such as Apache Arrow offer a unified data model that both client- and server-side engines can share.**

## Trade-offs & Pitfalls
- **The indexed-and-ordered difference is the practical trap.** Code written against Pandas that relies on row order or index-based access **may be silently wrong or unexpectedly slow** on a distributed DataFrame.
- **Eager versus lazy execution is the other.** Pandas' immediate execution makes debugging straightforward; **Spark's deferred, optimized plan means an error may only surface when the plan is finally executed.**

## Examples & Systems
R and Pandas (local); Spark, Flink, Daft (distributed); Apache Arrow as the shared columnar model.

## Since the 1st Edition
**Entirely new as a subtopic.** The 1st edition had no treatment of DataFrames anywhere — the API existed but was not part of the book's picture of batch processing. Its inclusion here, alongside [[DataFrames, Matrices, and Arrays (2e)]] in the data models chapter, reflects **data scientists becoming a first-class audience** for a data systems book.

## Related
- up: [[Batch Processing Models (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[DataFrames, Matrices, and Arrays (2e)]] — the data model, in Chapter 3
- [[Query Languages (2e)]] — the other high-level interface
- [[Machine Learning (2e)]] — the workload DataFrames mostly serve
