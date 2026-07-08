---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: netflix-iceberg-maestro
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Netflix processes trillions of daily events and once ran 600,000 Hive tables with 250 million partitions, migrating roughly 1.5 million of them to Apache Iceberg. Its Maestro orchestrator drives 70,000 workflows and 500,000 job steps daily, with Flink as the standard for real-time pipelines and the WAP (write-audit-publish) pattern guarding data quality.
