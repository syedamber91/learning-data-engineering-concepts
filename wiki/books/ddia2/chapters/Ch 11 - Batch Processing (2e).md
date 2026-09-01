---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
type: chapter-moc
tags: [ddia2, batch-processing, mapreduce, spark, flink, etl, moc]
sources:
  - raw/ch11.md
---
# Ch 11 – Batch Processing
Most of the book so far has been about **requests and queries and the corresponding responses** — **online systems**, where **response time is usually the primary measure of performance** and fault tolerance is needed for high availability. **But sometimes you need a bigger computation or more data than fits in an interactive request**: training an AI model, transforming lots of data, computing analytics over a very large dataset. **These are batch processing jobs, and the systems handling them are sometimes called offline systems.**

**A batch job takes read-only input data and produces output generated from scratch every run.** It **typically does not mutate data the way a read/write transaction would**, so **the output is derived from the input** — **if you don't like the output, delete it, adjust the job's logic, and run again.**

**By treating inputs as immutable and avoiding side effects, batch jobs get good performance and other benefits:**
- **If you introduce a bug and the output is wrong, roll back the code and rerun — or simply keep the old output in a different directory and switch back to it.** **Most object stores and open table formats support this, known as time travel.** **Databases with read/write transactions mostly do not have this property: rolling back buggy code does nothing to fix the bad data it already wrote.** **The ability to recover from buggy code has been called human fault tolerance.**
- **Consequently, feature development can proceed more quickly than where mistakes mean irreversible damage** — **minimizing irreversibility is beneficial for Agile development.**
- **The same files can be input for various jobs**, including **monitoring jobs that calculate metrics and check whether output has the expected characteristics**, by comparing to the previous run and measuring discrepancies.
- **Batch frameworks make efficient use of computing resources.** Batch-processing via OLTP databases and application servers is possible but **much more expensive in resources.**

**The challenges:** with most frameworks, **output can be processed by other jobs only after the whole job finishes**; **any change to the input data — even a single byte — requires reprocessing the entire input**; and **a job may run for minutes, hours, or days.** **The primary measure of performance is throughput.** **Some batch systems handle faults by aborting and restarting the whole job; others are fault-tolerant enough for a job to complete despite node crashes.**

**Modern batch processing was heavily influenced by MapReduce**, published by Google in 2004 and implemented in Hadoop, CouchDB, and MongoDB. It is **a fairly low-level programming model, less sophisticated than the parallel query execution engines in data warehouses** — **a step forward at the time for the scale achievable on commodity hardware, but now largely obsolete and no longer used at Google.** **Batch processing today more often uses Spark, Flink, or data warehouse query engines**, which rely on the same sharding and parallel execution but with **far more sophisticated caching and execution strategies.** **As these systems matured, operational concerns were largely solved and focus shifted to usability**: dataflow APIs, query languages, and DataFrame APIs. **Orchestration matured too — Hadoop-centric schedulers like Oozie and Azkaban gave way to Airflow, Dagster, and Prefect.** And **batch storage is shifting from distributed filesystems like HDFS, GlusterFS, and CephFS to object storage like S3**, while **scalable cloud warehouses like BigQuery and Snowflake blur the line between warehouses and batch processing.**

## Map
- [[Batch Processing with Unix Tools (2e)]] — the whole model, on one machine, in six commands
  - [[Simple Log Analysis (2e)]] — the awk/sort/uniq pipeline that finds your five most popular pages
  - [[Chain of Commands Versus Custom Program (2e)]] — the same job in Python, and why the difference matters
  - [[Sorting Versus In-Memory Aggregation (2e)]] — working set, spilling to disk, and why sorting scales
- [[Batch Processing in Distributed Systems (2e)]] — the framework as a distributed operating system
  - [[Distributed Filesystems (2e)]] — blocks, data nodes, metadata services, and the VFS analogue
  - [[Object Stores (2e)]] — buckets, keys, immutability, and the directory illusion
  - [[Distributed Job Orchestration (2e)]] — executors, resource managers, schedulers, workflows, and faults
- [[Batch Processing Models (2e)]] — how the data actually gets processed
  - [[MapReduce (2e)]] — mapper, sort, reducer, and its functional-programming roots
  - [[Dataflow Engines (2e)]] — Spark and Flink, and six advantages over MapReduce
  - [[Shuffling Data (2e)]] — the distributed sort that underlies joins and aggregations
  - [[Joins and Grouping (2e)]] — sort-merge joins and secondary sort
  - [[Query Languages (2e)]] — SQL as the lingua franca, and where it doesn't fit
  - [[DataFrames (2e)]] — the data scientist's API, distributed
- [[Batch Use Cases (2e)]] — where all this is actually used
  - [[Extract-Transform-Load (2e)]] — the archetypal batch workload
  - [[Analytics (2e)]] — the lakehouse, pre-aggregation, and ad hoc queries
  - [[Machine Learning (2e)]] — feature engineering, training, batch inference, and LLM data preparation
  - [[Serving Derived Data (2e)]] — why you must not write to production databases from a batch job

## Chapter Summary
**Batch frameworks process immutable, bounded input datasets to produce output data, allowing reruns and debugging without side effects.** Three main components: **an orchestration layer determining where and when jobs run, a storage layer to persist data, and a computation layer that processes it.**

**Distributed filesystems and object stores manage large files through block-based replication, caching, and metadata services**, and **modern frameworks interact with them via pluggable APIs.** **Job orchestrators schedule tasks, allocate resources, and handle faults**, and are distinct from **workflow orchestrators managing the lifecycle of a dependency graph of jobs.**

**MapReduce** established the canonical map/sort/reduce model; **dataflow engines like Spark and Flink offer simpler dataflow APIs and better performance.** **The shuffle** — a distributed sort — **is the foundational operation enabling grouping, joining, and aggregation.** As batch systems matured, **focus shifted to usability**: SQL and DataFrame APIs make jobs **more accessible and easier to optimize**, with the framework determining how to execute them efficiently.

The **use cases**: **ETL pipelines**; **analytics**, both pre-aggregated and ad hoc; **machine learning**, for preparing and processing training data; and **populating production-facing systems from batch outputs**, via streams or bulk-loading tools.

## Since the 1st Edition
This is the 1st edition's Chapter 10, **rewritten around the fact that MapReduce lost.** The 1st edition treated MapReduce as the organising model with dataflow engines as "beyond MapReduce"; **the 2nd edition states plainly that MapReduce is largely obsolete and no longer used at Google**, and reorganises around **orchestration / storage / computation as the three layers.**

**Retained:** the Unix-tools opening with the NGINX log example, the sorting-versus-in-memory-aggregation argument, MapReduce's mechanics and functional-programming roots, the shuffle, sort-merge joins, and the "don't write to a production database from a batch job" warning.

**Genuinely new:** [[Object Stores (2e)]] as a first-class storage layer alongside distributed filesystems, with a careful account of how they differ; [[Distributed Job Orchestration (2e)]] with its resource-allocation and gang-scheduling trade-offs, spot instances, and preemption; [[Query Languages (2e)]] and [[DataFrames (2e)]] as full subtopics; and **the entire [[Batch Use Cases (2e)]] topic** — ETL, analytics/lakehouse, ML including **LLM data preparation with Ray, Kubeflow, and Flyte**, and serving derived data **via Kafka rather than direct writes.**

**Dropped or compressed:** the 1st edition's long treatment of MapReduce join algorithms (broadcast hash joins, partitioned hash joins, map-side merge joins), its Pig/Hive/Cascading discussion, and its "materialization of intermediate state" essay are heavily condensed. **The 1st edition's [[The Output of Batch Workflows]] topic becomes [[Serving Derived Data (2e)]].**

## Related
- home: [[Home (2e)]] · previous: [[Ch 10 - Consistency and Consensus (2e)]] · next: [[Ch 12 - Stream Processing (2e)]]
- [[Ch 12 - Stream Processing (2e)]] — the same problems with unbounded input
- [[Data Warehousing (2e)]] — ETL and the data lake
- 1st edition: [[Ch 10 - Batch Processing]] — the chapter this one rewrites
