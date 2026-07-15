---
persona: vutr
kind: entity
sources:
- raw/airbnb-data-infrastructure/groupby-40-data-infrastructure-at.md
last_updated: '2026-07-15'
qc: passed
slug: airbnb-gold-silver-hadoop-clusters
topics:
- airbnb-data-infrastructure
---

By the time Airbnb wrote up its data infrastructure (2016), it ran two separate HDFS clusters, Gold and Silver, holding 11 petabytes of data between them plus multiple additional petabytes in S3. Critical jobs ran in Gold, "relaxed" jobs ran in Silver, Gold was treated as the single source of truth, and data could only ever be copied from Gold to Silver — never the other direction. That isolation bought safety at the cost of data replication and the ongoing work of keeping the two clusters in sync. Data reached these clusters from two sources: events from Kafka and MySQL database dumps, carrying user activity events and dimensional snapshots. Hive-managed tables were the central source and sink for data, Presto handled almost all ad hoc queries against them, and Airbnb built its own web-based query tool, Airpal, backed by Presto as the primary user-facing SQL interface. Airflow handled job scheduling, and engineers and data scientists used Spark for both machine learning and stream processing.

Two years before that 2016 writeup, Airbnb's Hadoop footprint was two poorly architected clusters, Pinky and Brain, running HDFS on EC2 instances at 300 terabytes. The migration to Gold/Silver had to solve four distinct problems, each with a named fix:

- **Running Hadoop on Mesos** — poor visibility into logs and cluster health, Mesos capping Hadoop at MapReduce v1, cluster underutilization, and high operational load. Fixed by moving away from Mesos.
- **Remote reads and writes** — storing HDFS data on mounted EBS volumes forced large data transfers over the public EC2 network, against Hadoop's local-read/write design; splitting storage across three availability zones (each treated as its own "rack") caused every replica read/write to cross zones, compounding the slowdown. Fixed by using dedicated instances with local storage running in a single availability zone.
- **Heterogeneous workload on homogeneous machines** — Hive/Hadoop/HDFS needed storage but not much RAM or CPU, while Presto and Spark needed RAM and CPU but not much storage, yet all ran on the same machine shape. Fixed by picking EC2 instance types per component to match its actual resource profile.
- **System monitoring** — Hadoop, Hive, and HDFS have many potential failure points, and building custom monitoring/alerting from scratch felt like reinventing the wheel. Fixed by signing a support contract with Cloudera and adopting Cloudera Manager.

The measured result: disk read/write throughput improved from 70–150MB/sec to 400+ MB/sec, read throughput roughly tripled, write throughput roughly doubled, and cost dropped 70%.

*See also: [[airbnb-infrastructure-philosophy]] · [[minerva]]*
