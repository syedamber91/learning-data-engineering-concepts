---
persona: vutr
kind: entity
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/amazon-s3-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: amazon-s3
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

Amazon Simple Storage Service (S3), introduced in 2006, is AWS's pioneering object storage service and — per Vu's framing — the one AWS service that has been there "from the very beginning" and never became obsolete. Object storage manages data as **objects** inside flat containers called **buckets**, not as a file hierarchy. Every object carries a unique **key** as its identifier, an optional **prefix** (a leading substring of the key that only *looks* like a folder path — see [[prefix-as-folders]]), an optional **version ID** when versioning is enabled, a **value** (an arbitrary byte sequence — S3 doesn't care what format it holds), and **metadata** split into system-assigned and user-defined fields. Clients never touch a local disk directly; even the AWS console is calling the same object APIs on the user's behalf underneath.

Under the hood, S3 is not one program but 350+ microservices per AWS region, organized into four layers: a **frontend fleet** serving the REST API, **namespace services**, a **storage fleet** of millions of hard disks, and a **storage management fleet** running background operations like object expiration and replication. This disaggregation is the architectural opposite of GFS and HDFS's single-coordinator design ([[gfs]], [[hdfs]]) — there is no one server holding all the metadata in RAM, which is exactly what lets S3 avoid the scaling ceiling those systems hit (see [[hdfs-namenode-scaling-limit]]).

S3's popularity in data engineering, in Vu's view, comes down to a simple economic fact: it is nearly impossible for an individual organization to operate storage infrastructure with the same durability and availability guarantees AWS (or GCP) provides, at the same cost. That case is developed further in [[object-storage-durability-erasure-coding]], [[s3-strong-consistency]], [[s3-atomicity-and-conditional-writes]], and [[object-storage-as-backbone]].

*See also: [[gfs]] · [[hdfs]] · [[prefix-as-folders]] · [[object-storage-durability-erasure-coding]] · [[s3-strong-consistency]]*
