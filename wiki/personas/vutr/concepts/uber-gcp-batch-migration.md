---
persona: vutr
kind: concept
sources:
- raw/uber-data-infrastructure-case-studies/groupby-38-modernizing-ubers-batch.md
- raw/uber-data-infrastructure-case-studies/groupby-41-ubers-batch-data-infrastructure.md
- raw/uber-data-infrastructure-case-studies/ubers-big-data-revolution-from-mysql.md
last_updated: '2026-07-15'
qc: passed
slug: uber-gcp-batch-migration
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Uber runs one of the largest Hadoop installations in the world — more than 1 exabyte of data across tens of thousands of servers in each of two regions — and announced it is moving its batch data analytics and ML training stack to Google Cloud Platform to keep up with growing needs.

The **strategy** is staged: first move to cloud object storage for the data lake plus cloud IaaS (Infrastructure as a Service) for compute, prioritizing a quick and minimally disruptive migration; only later lean into applicable PaaS offerings like GCP Dataproc or BigQuery. Four **migration principles** guide execution. To **avoid painful migrations for data users**, Uber minimizes what changes for people like dashboard owners by using a cloud storage connector that gives HDFS-compatible access to Google Cloud Storage, built on open standards (Parquet, Hudi, Spark, Hadoop YARN, Kubernetes) so on-prem HDFS services integrate with GCP storage without a rewrite. To **enhance data access proxies**, Uber extends the proxies it already built in front of Presto, Spark, and Hive (which hide the underlying compute clusters from callers) so that, once migration completes, all queries and jobs submitted through them get routed to the new cloud-based stack transparently. To **leverage Uber's container and deployment infrastructure**, the batch stack sits on infrastructure building blocks already designed to be agnostic between cloud and on-prem, letting the batch ecosystem expand onto GCP without a separate deployment model. And to **forecast data governance issues early**, Uber plans to restrict its data management services to only approved cloud-vendor data services, heading off governance complexity before it appears rather than retrofitting controls later.

The **major workload** breaks into four concrete pieces of engineering: formulating the bucket-mapping algorithm that migrates HDFS files/directories to cloud objects; extending Kerberos-based authentication so all users, groups, and service accounts keep the same authorized-access levels against the object-store data lake and other cloud PaaS as they had on-prem; extending **HiveSync** — Uber's existing permissions-aware, bi-directional data replication service — to replicate the on-prem data lake into the cloud-based lake and its corresponding Hive Metastore; and provisioning new YARN and Presto clusters on GCP that the existing data access proxies route traffic to.

Four **challenges** are named up front. **Performance**: Object Store and HDFS have different feature and performance characteristics, so Uber plans to lean on (and help evolve) open-source Hadoop connectors to close that gap. **Usage governance**: cloud costs can spiral without active management, so Uber pairs cloud elasticity with its internal capacity engineering team to build more advanced cost tracking. **Non-analytics/ML use of HDFS**: some Uber teams use HDFS as a generic file store outside analytics/ML, and those use cases get migrated to other internal blob stores via a transparent path designed to avoid disruption. **Unknown unknowns**: Uber expects unanticipated issues and hopes to catch them early through end-to-end integration testing rather than in production.

This migration is the successor to [[uber-data-platform-evolution|Generation 3's]] Hadoop/Hudi-on-HDFS platform, and it inherits the same scaling pressure — HDFS's NameNode ceiling — that Hudi's incremental design ([[uber-hudi-query-and-write-taxonomy]]) had already been built to work around, but this time the fix is architectural (leave HDFS) rather than incremental (process HDFS more efficiently).

*See also: [[uber-data-platform-evolution]] · [[uber-data-platform]]*
