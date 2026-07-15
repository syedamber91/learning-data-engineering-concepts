---
persona: vutr
kind: entity
sources:
- raw/uber-data-infrastructure-case-studies/how-did-uber-build-their-data-infrastructure.md
last_updated: '2026-07-15'
qc: passed
slug: sparkle-etl-framework
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Sparkle is the framework Uber built on top of Apache Spark to standardize how its 20,000+ critical batch pipelines and datasets get written, after Uber migrated all batch workloads onto Spark in 2023. Sparkle's core idea is to let users express business logic as modules, where each module is a single unit of transformation — this improves reusability and lets teams write test suites per module or for whole end-to-end pipelines, rather than testing monolithic jobs. It offers source and sink integrations so users can focus on writing business logic in SQL or in Java, Scala, or Python, rather than plumbing.

Sparkle is integrated with Apache Hudi's DeltaStreamer tool (which Uber originally contributed to) to simplify the common Kafka-to-Hudi pipeline: with this integration, users only need to supply three inputs — a table definition (DDL + Hudi format), DeltaStreamer YAML configs (including the Hudi primary key used for deduplication), and the SQL or Scala/Java transformation logic itself ([[uber-hudi-etl-pipeline-and-impact]]).

*See also: [[uber-data-platform]] · [[uber-hudi-etl-pipeline-and-impact]] · [[uber-hudi-query-and-write-taxonomy]]*
