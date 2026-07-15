---
persona: vutr
kind: entity
sources:
- raw/uber-data-infrastructure-case-studies/ubers-big-data-revolution-from-mysql.md
last_updated: '2026-07-15'
qc: passed
slug: marmaray
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Marmaray is Uber's generalized data ingestion platform, built to solve the second-generation Hadoop lake's worst problem: 24-hour-old data. All upstream datastore events — including logs from various services — are sent to Kafka with a unified Avro encoding, and Marmaray runs in mini-batches, consuming those changelogs from Kafka and applying them to existing Hadoop data via Apache Hudi, so records can be updated or deleted instead of only appended. Behind the scenes, Spark jobs power Marmaray and run every 10-15 minutes, keeping data latency under 30 minutes. Because transformations are pushed downstream into Hadoop rather than performed during ingestion, Marmaray can ingest raw data quickly and reliably, and Uber reports improved data reliability precisely because error-prone transformations no longer happen at ingestion time.

Marmaray is the ingestion half of Uber's third-generation ("Hudi era") data platform; the transformation/modeling half is the separate incremental ETL pipeline built on Hudi, Spark, and Uber's Piper workflow tool ([[uber-hudi-etl-pipeline-and-impact]]).

*See also: [[uber-data-platform-evolution]] · [[uber-hudi-query-and-write-taxonomy]] · [[uber-data-platform]]*
