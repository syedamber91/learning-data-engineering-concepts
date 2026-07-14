---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: amazon-s3-gfs-hdfs-and-distributed-file-systems
---

Related: [[amazon-s3]] · [[s3-strong-consistency]] · [[gfs]] · [[gfs-record-append]] · [[hdfs]] · [[hdfs-namenode-scaling-limit]] · [[prefix-as-folders]] · [[component-failure-as-normal]] · [[object-storage-as-backbone]]

## Comparisons
The three systems share a lineage but diverge sharply on where metadata lives and how they scale. Both [[gfs]] and [[hdfs]] centralize metadata in a single memory-resident coordinator (GFS master, HDFS NameNode) and default to 3 replicas — GFS with 64MB chunks, HDFS with 128MB blocks. But they differ on chunk location: GFS deliberately does NOT persist chunk locations on the master, polling chunkservers at startup instead. The RAM-bound design is exactly what caps [[hdfs]] — see [[hdfs-namenode-scaling-limit]] — where GFS separates control and data flow and uses [[gfs-record-append]] for concurrent atomic writes.

By contrast, [[amazon-s3]] abandons the single-coordinator model entirely: it's 350+ microservices partitioning a flat keyspace by prefix (see [[prefix-as-folders]]), which sidesteps the petabyte ceiling that hobbles HDFS. The trade S3 historically made was consistency — eventual, not strong — until [[s3-strong-consistency]] closed that gap in December 2020. All three, though, are built on the same premise of [[component-failure-as-normal]].

## Open questions
- How does S3's per-prefix throughput ceiling (3,500 PUT / 5,500 GET) interact with its lexicographic partitioning in practice — does key design still matter for hot prefixes?
- What exactly is the new [[s3-strong-consistency]] staleness-check component doing internally, and what does it cost in latency?
- Given [[hdfs-namenode-scaling-limit]], what architectural moves (federation, alternative metadata stores) actually push HDFS past the 50-100PB wall?
- If [[gfs-record-append]] only guarantees at-least-once, how do downstream consumers deduplicate, and is that pushed to the application layer?
- With [[object-storage-as-backbone]] displacing HDFS, what workloads (if any) still justify running HDFS today?

## Synthesis
The through-line across [[gfs]], [[hdfs]], and [[amazon-s3]] is that they all start from [[component-failure-as-normal]] — failure is assumed, so recovery is designed in. Where GFS and HDFS bind their scalability to a single RAM-resident metadata coordinator (the reason for [[hdfs-namenode-scaling-limit]]), [[amazon-s3]] disaggregates into hundreds of microservices over a flat prefix keyspace, which is how [[object-storage-as-backbone]] became true and HDFS handed over the data-lake crown. The remaining maturity gap — consistency — was closed by [[s3-strong-consistency]] in December 2020, cementing object storage as the default substrate for modern data architecture.

## Related topics
- [[airflow]] — Airflow's KubernetesExecutor runs tasks as isolated pods on the same distributed-file-system/object-storage substrate, and its scaling trade-offs mirror the coordinator-bound designs of GFS/HDFS.
- [[iceberg]] — Iceberg's open table formats sit directly on object storage, deriving free Durability from S3 while needing conditional writes because S3 gives no multi-object atomicity.
- [[history-of-data-engineering]] — Hadoop/HDFS was the big-data detour in the history of the field before object storage displaced it as the data-lake backbone.
- [[kafka]] — Diskless Kafka designs (AutoMQ, WarpStream) push the write-ahead log onto S3/EBS, reacting to the same cross-AZ economics of distributed storage.
- [[data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa]] — Cheap object storage is the substrate that makes the data lake and lakehouse possible in the architecture debate.
- [[Hadoop]] — DDIA's account of the Hadoop ecosystem (HDFS + MapReduce, "Unix philosophy at datacenter scale") that this note's HDFS thread traces forward into object storage displacing it.
- [[HDFS]] — DDIA's mechanics of HDFS's blocks, replication, and NameNode placement — the design whose RAM-bound metadata coordinator this note identifies as the source of the NameNode scaling limit.
