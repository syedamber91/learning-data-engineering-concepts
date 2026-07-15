---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
topic: MapReduce and Distributed Filesystems
type: subtopic
tags: [ddia, mapreduce, shuffle, workflows]
sources:
  - raw/ch10.md
---
# MapReduce Job Execution
> A [[MapReduce]] job runs two user callbacks — map and reduce — with an implicit distributed sort between them, parallelized across a cluster by partitioning.

## The Idea
[[MapReduce]] generalizes the log-analysis pipeline: split input into records, extract a key-value pair from each (map), sort by key, then scan groups of equal keys (reduce). You only write steps 2 and 4; the framework supplies record parsing and the sort. Because mappers and reducers are stateless per-record callbacks with no knowledge of where data lives, the framework is free to spread the work over thousands of machines without the programmer writing any parallelism code.

## How It Works
- **Mapper**: invoked once per input record; emits zero or more key-value pairs; carries no state between records.
- **Reducer**: receives one key plus an iterator over *all* values collected for that key (possibly more than fits in memory) and emits output records.
- **Parallelization by [[Partitioning]]**: the input is typically an [[HDFS]] directory; each file block becomes a map task. The scheduler tries to place each map task on a machine already holding a replica of its block — *computation near the data* — avoiding network copies. Job code (e.g. JARs) is shipped to those machines first.
- **The shuffle**: the reducer count is chosen by the job author, and each mapper hashes every output key to pick its destination reducer (see [[Partitioning by Hash of Key]]). Each mapper writes per-reducer partitions to local disk as sorted files (the same idea as [[SSTables and LSM-Trees]]). When a mapper finishes, reducers pull their partition files and merge them, preserving order — so all values for a key arrive adjacent. Despite the name, nothing is random about the shuffle.
- **Workflows**: a single job can't do everything (ranking pages by view count needs a second sort), so jobs are chained: job B reads the directory job A wrote. Hadoop itself sees them as unrelated jobs — more like commands connected by temp files than by pipes — so external schedulers (Oozie, Azkaban, Luigi, Airflow, Pinball) manage the dependency graph. Recommendation pipelines of 50–100 chained jobs are routine.

## Trade-offs & Pitfalls
- Output is all-or-nothing: partial output of failed jobs is discarded, so a downstream job can only start after every upstream task finishes.
- The mandatory sort between map and reduce costs effort even when the computation doesn't need it — a key inefficiency later removed by dataflow engines ([[Materialization of Intermediate State]]).
- Raw MapReduce APIs are laborious; higher-level layers (Pig, Hive, Cascading, Crunch, FlumeJava) generate the multi-stage plumbing.

## Examples & Systems
[[Hadoop]] MapReduce (Java classes) over [[HDFS]]; MongoDB/CouchDB run JavaScript mappers/reducers (see [[MapReduce Querying]]); Unix tools can even serve as mappers and reducers.

## Related
- up: [[MapReduce and Distributed Filesystems]] · chapter: [[Ch 10 - Batch Processing]]
- [[Simple Log Analysis]] — the single-machine ancestor of this pattern
- [[Partitioning by Hash of Key]] — how keys are routed to reducers
- [[Reduce-Side Joins and Grouping]] — what the shuffle makes possible
- [[MapReduce Querying]] — the same model inside document databases
