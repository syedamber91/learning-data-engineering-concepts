---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, batch-processing, systems]
sources:
  - raw/ch10.md
---
# Hadoop

The open-source ecosystem around [[HDFS]] (storage) and [[MapReduce]] (compute),
grown into a platform where many processing models (Hive, Pig, Spark, Tez, HBase)
share one filesystem. The book frames it as "Unix philosophy at datacenter scale":
files (immutable inputs, write-once outputs) as the uniform interface, letting
diverse tools compose — and contrasts that openness with monolithic MPP databases.

Book home ground: [[MapReduce and Distributed Filesystems]] and
[[Comparing Hadoop to Distributed Databases]] (Ch 10).

## Referenced In
- [[Avro]]
- [[Batch Processing with Unix Tools]]
- [[Batch and Stream Processing]]
- [[Ch 10 - Batch Processing]]
- [[Comparing Hadoop to Distributed Databases]]
- [[Data Warehousing]]
- [[Describing Performance]]
- [[Map-Side Joins]]
- [[MapReduce Job Execution]]
- [[MapReduce and Distributed Filesystems]]
- [[Membership and Coordination Services]]
- [[Parallel Query Execution]]
- [[Partitioning and Replication]]
- [[Simple Log Analysis]]
- [[The Foundation - Datalog]]
- [[The Unix Philosophy]]
- [[Transaction Processing or Analytics]]
- [[Unbundling Databases]]

## Related in the other wiki
- [[amazon-s3-gfs-hdfs-and-distributed-file-systems]] — vutr's account of what came after Hadoop's HDFS: object storage (S3) displacing it as the data-lake backbone once its single-coordinator design hit scaling limits.
