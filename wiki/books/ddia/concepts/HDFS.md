---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, storage, batch-processing]
sources:
  - raw/ch10.md
---
# HDFS

Hadoop's distributed filesystem: files split into large blocks, replicated across
datanodes' local disks, with a namenode tracking placement. Shared-nothing —
commodity machines and no special hardware — making storage cheap enough to keep raw
data and derive many views from it. Fault tolerance via block replication or erasure
coding.

In the book: the substrate of [[MapReduce and Distributed Filesystems]] (Ch 10);
its write-once immutable files are what make MapReduce's retry-based fault
tolerance and [[Hadoop]]'s tool diversity possible.

## Referenced In
- [[Batch Processing with Unix Tools]]
- [[Batch and Stream Processing]]
- [[Beyond MapReduce]]
- [[Ch 10 - Batch Processing]]
- [[Comparing Hadoop to Distributed Databases]]
- [[Fault Tolerance]]
- [[MapReduce Job Execution]]
- [[MapReduce and Distributed Filesystems]]
- [[Materialization of Intermediate State]]
- [[Reduce-Side Joins and Grouping]]
- [[Strategies for Rebalancing]]
- [[The Output of Batch Workflows]]

## Related in the other wiki
- [[amazon-s3-gfs-hdfs-and-distributed-file-systems]] — vutr's detail on the NameNode RAM-bound metadata design that caps HDFS's scale, and how S3's disaggregated microservices sidestepped that ceiling.
