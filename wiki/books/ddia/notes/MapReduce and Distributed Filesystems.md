---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
type: topic
tags: [ddia, mapreduce, hdfs, distributed-batch]
sources:
  - raw/ch10.md
---
# MapReduce and Distributed Filesystems
[[MapReduce]] is Unix-style batch processing scaled out to thousands of machines: a job reads immutable inputs, produces output with no other side effects, and composes into workflows. Where Unix tools use stdin/stdout, MapReduce jobs read and write a distributed filesystem — in [[Hadoop]]'s case [[HDFS]], an open-source rebuild of the Google File System. HDFS follows the shared-nothing principle: a daemon on every commodity machine exposes its local disks, a central NameNode tracks which blocks live where, and blocks are replicated (or erasure-coded with Reed–Solomon for lower overhead) to survive machine and disk failures — RAID-like redundancy, but over an ordinary datacenter network instead of special hardware. Deployments reach tens of thousands of machines and hundreds of petabytes because commodity storage is dramatically cheaper than dedicated NAS/SAN appliances. On this foundation the topic builds up the mechanics of jobs, the join algorithms that bring related records together, the shapes that batch output takes, and a comparison with the parallel databases that got there first.

## Subtopics
- [[MapReduce Job Execution]] — mapper/reducer callbacks, the shuffle, putting computation near the data, and chaining jobs into workflows via HDFS directories.
- [[Reduce-Side Joins and Grouping]] — sort-merge joins, GROUP BY and sessionization as the same "bring related data together" pattern, and skew-handling for hot keys.
- [[Map-Side Joins]] — broadcast hash, partitioned hash, and map-side merge joins: faster, but only when you can make assumptions about input layout.
- [[The Output of Batch Workflows]] — search indexes and bulk-built key-value stores, plus the immutability philosophy that makes batch jobs maintainable.
- [[Comparing Hadoop to Distributed Databases]] — how Hadoop differs from MPP databases in storage freedom, processing-model diversity, and fault handling.

## Key Takeaways
- A MapReduce job = extract key/value (map) → partition by key hash → sort → merge → aggregate per key (reduce); the sort is implicit and always happens.
- Keys act like destination addresses: emitting a key-value pair "mails" the record to a reducer, separating network plumbing from application logic.
- Joins in batch mean resolving *all* occurrences of an association at once — never per-record lookups over the network, which are slow and nondeterministic.
- Output is all-or-nothing: partial output of failed jobs is discarded, so retries are safe and clean.
- The framework hides partial failure — code gets retried transparently, which only works because inputs are immutable.

## Related
- [[Ch 10 - Batch Processing]] — parent chapter MOC
- [[Batch Processing with Unix Tools]] — the single-machine philosophy this generalizes
- [[Beyond MapReduce]] — dataflow engines that fix its performance problems
- [[Partitioning by Hash of Key]] — the Chapter 6 mechanism reused in the shuffle

## Related in the other wiki
- [[hadoop-mapreduce]] — vutr's brief history of MapReduce's decline (Google dropped it internally by 2014) after enterprises struggled to tailor processing logic to its rigid paradigm.
