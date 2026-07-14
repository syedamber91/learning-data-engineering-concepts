---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
topic: Query Languages for Data
type: subtopic
tags: [ddia, mapreduce, mongodb, aggregation]
sources:
  - raw/ch02.md
---
# MapReduce Querying
> MapReduce sits between declarative and imperative — query logic as pure code snippets — and MongoDB's evolution away from it shows NoSQL reinventing SQL.

## The Idea
[[MapReduce]] is Google's programming model for bulk data processing across machine clusters (full treatment in [[MapReduce and Distributed Filesystems]]). Some NoSQL stores — MongoDB, CouchDB — adopted a restricted form of it as their mechanism for read-only queries over many documents. It's neither fully declarative nor fully imperative: you supply small code snippets that a framework invokes repeatedly, built on the `map` (a.k.a. collect) and `reduce` (a.k.a. fold/inject) functions familiar from functional programming.

## How It Works
Consider a wildlife-observation log where each document records a sighting: a timestamp, a species family, and an animal count. "Total lions seen per month" in SQL is a single statement — filter on family, group by the month extracted from the timestamp, sum the counts.

MongoDB's MapReduce version splits this across pieces: a declarative filter (a MongoDB-specific extension) selects matching documents; a JavaScript `map` function runs once per matching document with the document bound as `this`, emitting a key (e.g. a `"2019-04"` year-month string) and a value (the animal count); the framework groups emitted pairs by key; a `reduce` function then runs once per key over the collected values (e.g. receiving `[2, 5]` for one month and returning 7); output lands in a named collection.

The functions must be *pure*: input only from their arguments, no side effects, no extra database queries. That constraint is what lets the database run them anywhere, in any order, and safely re-run them after failures. Within those limits they remain expressive — string parsing, library calls, arithmetic.

Two clarifications the chapter stresses: SQL is not inherently single-machine — it can be implemented as a pipeline of MapReduce stages, but plenty of distributed SQL engines use no MapReduce at all; and embedding JavaScript in queries isn't unique to MapReduce — some SQL databases allow it too.

## Trade-offs & Pitfalls
Writing two carefully coordinated functions is harder than one query, and opaque code gives the optimizer nothing to work with. MongoDB 2.2 therefore added the *aggregation pipeline*, a declarative language expressing the same query as chained JSON-syntax stages (`$match`, then `$group` with `$sum`). Its expressiveness resembles a SQL subset in JSON clothing — the moral being that NoSQL systems tend to reinvent SQL in disguise.

## Examples & Systems
Google's MapReduce; MongoDB and CouchDB query implementations; MongoDB aggregation pipeline; PostgreSQL for the SQL comparison.

## Related
- up: [[Query Languages for Data]] · chapter: [[Ch 02 - Data Models and Query Languages]]
- [[MapReduce Job Execution]] — the full cluster-scale mechanics
- [[Declarative Queries on the Web]] — why declarative forms optimize better
- [[Batch Processing with Unix Tools]] — the philosophy MapReduce descends from
