---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
topic: Beyond MapReduce
type: subtopic
tags: [ddia, hive-pig, declarative-queries, query-optimization]
sources:
  - raw/ch10.md
---
# High-Level APIs and Languages
> As raw [[MapReduce]] programming proved laborious, relational-flavoured APIs with cost-based optimizers took over — making batch frameworks converge on MPP-database performance while keeping arbitrary-code flexibility.

## The Idea
With petabyte-scale execution on 10,000-machine clusters a solved problem, attention moved to programmer productivity and machine efficiency. Hive, Pig, Cascading, and Crunch grew as abstractions over MapReduce because hand-writing jobs (including your own join code) was painful; when Tez arrived they gained a free upgrade path — same job code, new [[Dataflow]] engine underneath. Spark and Flink ship their own high-level APIs, drawing on FlumeJava.

## How It Works
These APIs express computations from relational building blocks — join on a field, group by key, filter by predicate, aggregate by count or sum — implemented internally with the chapter's join and grouping algorithms. Less code is one win; *interactive* use is another: writing analysis incrementally in a shell and running it as you go suits exploratory work, echoing [[The Unix Philosophy]].

**The declarative turn.** Specify a join as a relational operator rather than as code, and the framework can inspect input properties and choose among sort-merge, broadcast hash, and partitioned hash strategies itself (see [[Map-Side Joins]]). Hive, Spark, and Flink carry cost-based query optimizers that even reorder joins to shrink intermediate state — sparing humans the algorithm catalogue, the same idea as [[Query Languages for Data]]. Yet these systems stop short of full SQL: they stay built on callback functions free to run arbitrary code and lean on ecosystem libraries (parsing, NLP, image analysis, numerics) — historically their key edge over MPP databases, whose user-defined functions are clunky and disconnected from package managers like Maven or npm. Declarative-ness pays elsewhere too: when a callback is a mere filter or column projection, per-record function calls burn CPU; expressed declaratively, the optimizer can exploit [[Column-Oriented Storage]] to read only needed columns and use vectorized execution in cache-friendly loops. Spark compiles such inner loops to JVM bytecode; Impala uses LLVM to emit native code.

**Specialization.** Reusable building blocks are colonizing domains beyond business intelligence: Mahout packages ML algorithms over MapReduce/Spark/Flink while MADlib does the same inside an MPP database; spatial nearest-neighbour search and approximate genome-sequence matching push batch engines further afield.

## Trade-offs & Pitfalls
- Declarative operators optimize well but constrain expression; callbacks express anything but hide structure from the optimizer — these APIs deliberately mix the two.
- Convergence cuts both ways: batch frameworks gain MPP-like performance, MPP databases gain programmability — ultimately all are "systems that store and process data."

## Examples & Systems
Hive, Pig, Cascading, Crunch; Spark DataFrames/Spark SQL, Flink, Tez, Impala; Mahout, MADlib.

## Related
- up: [[Beyond MapReduce]] · chapter: [[Ch 10 - Batch Processing]]
- [[Comparing Hadoop to Distributed Databases]] — the two camps this convergence unites
- [[Materialization of Intermediate State]] — the engines these APIs compile onto
- [[MapReduce Querying]] — the Chapter 2 first look at MapReduce as a query idiom
