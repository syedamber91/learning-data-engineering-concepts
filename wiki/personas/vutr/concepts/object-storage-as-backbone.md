---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/amazon-s3-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: object-storage-as-backbone
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

Object storage has stopped being a dumping ground for archival data or disaster recovery and become the backbone of many organizations' data architecture — Vu traces this shift through three waves. First, the historical handoff: HDFS was the primary data-lake choice before cloud object storage matured, but once S3/GCS arrived, HDFS "handed over the crown" — no management overhead, the ability to store any data at all (the exact goal of a data lake), and durability/scalability no single organization could match on its own (see [[gfs]], [[hdfs]], and their scaling constraints in [[hdfs-namenode-scaling-limit]]).

Second, the 2020s lakehouse wave: because object storage provides Durability "for free" but no multi-object atomic transactions, table formats like Apache Iceberg and Delta Lake had to build a table abstraction *on top* of raw objects — turning object storage from an inert bucket of files into something that behaves like transactional table storage, via the conditional-write mechanism described in [[s3-atomicity-and-conditional-writes]].

Third, and most recent per Vu: systems that used to depend on local disk have started rebuilding themselves on object storage instead. On the streaming side, Kafka-compatible systems — WarpStream, AutoMQ, Bufstream — build their message-log storage on object storage rather than broker-local disks (see [[kafka]]'s diskless architecture material for the deep dive). On the database side, Neon reimagines Postgres around object storage, and turbopuffer is a vector/full-text search database built the same way. S3 has also added native support for storing and querying vector embeddings directly, letting AI workloads skip a separate vector store entirely. Vu's overall verdict: none of this happens without cloud vendors doing the unglamorous work of making object storage simple and robust enough to trust as a foundation, not just a place to archive old files.

*See also: [[amazon-s3]] · [[s3-atomicity-and-conditional-writes]] · [[object-storage-operational-practices]]*
