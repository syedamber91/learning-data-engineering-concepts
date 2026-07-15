---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
topic: MapReduce and Distributed Filesystems
type: subtopic
tags: [ddia, batch-output, search-indexes, immutability]
sources:
  - raw/ch10.md
---
# The Output of Batch Workflows
> Batch jobs produce neither OLTP lookups nor analyst reports but *derived structures* — search indexes, bulk-built databases — and the immutable-input, replaceable-output philosophy is what makes them safe to operate.

## The Idea
Batch processing is neither transaction processing nor classic analytics (see [[Transaction Processing or Analytics]]): it scans large inputs like an analytic query, but its result is usually a data structure that serves other systems rather than a report for a manager. Asking "what is all this computation *for*?" reveals two archetypes — search indexes and machine-learning/recommendation outputs served as key-value stores — and a shared operating philosophy inherited from [[The Unix Philosophy]].

## How It Works
**Search indexes.** Google's original [[MapReduce]] use case was building its search index as a workflow of 5–10 jobs. Building a full-text index is a natural fit: mappers partition the documents, each reducer builds the term dictionary→postings-list files for its partition, and the immutable index files land on the distributed filesystem — document-partitioned [[Secondary Indexes]] that parallelize beautifully (see [[Partitioning and Secondary Indexes]]). When documents change you can either rerun the whole workflow (expensive but trivially easy to reason about: documents in, indexes out) or index incrementally, Lucene-style, with background segment merging and [[Compaction]].

**Key-value stores as output.** Classifiers (spam, anomaly, image) and recommenders need their results queryable by the web application. Writing from mappers/reducers straight into a production database is a bad idea three times over: per-record network requests destroy batch throughput; massively parallel tasks can overwhelm the database and degrade live queries; and side-effectful writes leak partial results from failed or speculatively executed tasks, breaking MapReduce's all-or-nothing output guarantee. The better pattern: build a brand-new immutable database *inside* the job, write its files to [[HDFS]], then bulk-load them into read-only serving nodes. Voldemort, Terrapin, ElephantDB, and HBase bulk loading all work this way. Because the files are write-once, the structures stay simple — no [[Write-Ahead Log]] needed — and Voldemort even serves old files until the new ones finish copying, switching atomically and falling back if anything breaks.

## Trade-offs & Pitfalls
- Full index rebuilds waste work when few documents changed; incremental indexing trades that for more moving parts.
- Immutability buys *human fault tolerance*: buggy code? Roll back and rerun, or just re-point at the previous output directory — unlike a read-write database, where bad writes outlive the bad deploy.
- Minimized irreversibility speeds feature development; automatic task retry is only safe because inputs are immutable and failed output is discarded.
- Unlike untyped Unix text, Hadoop jobs favour structured formats — [[Avro]] and Parquet ([[Column-Oriented Storage]]) — killing low-value parsing work and allowing [[Schema Evolution]].

## Examples & Systems
Google search indexing; Lucene/Solr index builds on Hadoop; LinkedIn's Voldemort; Pinterest's Terrapin; ElephantDB; HBase bulk loads.

## Related
- up: [[MapReduce and Distributed Filesystems]] · chapter: [[Ch 10 - Batch Processing]]
- [[Comparing Hadoop to Distributed Databases]] — where such workflows sit versus MPP warehouses
- [[Materialization of Intermediate State]] — the same output discipline inside multi-job workflows
- [[State, Streams, and Immutability]] — immutability elevated to a system-design principle
