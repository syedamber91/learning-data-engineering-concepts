---
persona: vutr
kind: entity
sources:
- raw/cloud-kubernetes-docker-infrastructure-tooling/i-spent-6-hours-learning-aws-glue.md
last_updated: '2026-07-15'
qc: passed
slug: aws-glue
topics:
- cloud-kubernetes-docker-infrastructure-tooling
---

Before Glue existed, AWS had no first-party tool for data integration. Operational data from RDS or DynamoDB had to be loaded into Redshift for analytics, and the rise of the data-lake pattern meant semi-structured data landing in object storage first, then getting processed via EMR or Athena. The ETL tools of that era were built for structured data, weren't elastic on the cloud, and left customers self-managing the infrastructure behind their own scripts. AWS Glue was built to relieve that heavy lifting: a cloud-native, serverless ETL service designed around three explicit principles — let customers write custom code when the system can't satisfy their needs, support diverse analytics environments without forcing one data model or query language, and reduce infrastructure-management time so developers stay productive. Vu's notes on Glue are themselves a distillation of Amazon's own VLDB paper, "The Story of AWS Glue."

Glue is really two services wearing one name. The **ETL stack** is the processing side: Glue Studio is a visual, DAG-based interface that auto-generates human-readable Spark scripts (each node is a source/sink/transform step a user can edit directly); the Glue ETL runtime bundles core Spark packages with Glue-specific libraries — most notably [[glue-dynamicframe-and-schema-inference|DynamicFrame]], introduced to handle semi-structured data that lacks a schema upfront; an orchestration layer called **workflows** stitches Crawlers and Spark/Python jobs into pipelines with parameter passing, fallback jobs, and schedule- or event-based triggers; and the serverless execution layer lets a user submit a job and hand everything else — provisioning, scaling — to AWS, an area that went through three real architectural generations (see [[glue-serverless-execution-evolution]]).

The **Glue Data Catalog** is the metadata side: a scalable, managed replacement for the Hive Metastore that lets customers model S3 data, relational databases, NoSQL stores, and streaming sources as databases and tables queryable by Athena, EMR, and Redshift alike (see [[glue-data-catalog-and-crawlers]] for how it's built and kept up to date). Both halves integrate tightly with the rest of Amazon's ecosystem — S3, Redshift, Athena — which is what makes Glue, in Vu's framing, "a powerful choice for building and maintaining data lakes and pipelines" rather than just another Spark-as-a-service offering.

Glue's own use cases, per the source, cluster around three patterns: loading semi-structured S3 data into Redshift by discovering schema and transforming nested/inconsistent formats; migrating on-prem DBMS data into S3 by inferring schemas with Crawlers and organizing output into Parquet; and ingesting streaming data from Kinesis or Kafka for cleaning and pre-aggregation before it lands in S3 or Redshift. The challenges Glue was built to address — inconsistent/missing metadata, multi-source integration across VPCs and auth protocols, Spark's horizontal scaling putting pressure on source databases, unpredictable batch-vs-backfill workload sizes, and small-file/large-file partition-layout trade-offs in object storage — are the throughline that explains why the Data Catalog, the Parquet writer, and the crawler design all look the way they do.

*See also: [[glue-dynamicframe-and-schema-inference]] · [[glue-serverless-execution-evolution]] · [[glue-data-catalog-and-crawlers]] · [[object-storage-as-data-lake-backbone]]*
