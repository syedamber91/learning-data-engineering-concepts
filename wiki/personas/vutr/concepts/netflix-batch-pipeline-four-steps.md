---
persona: vutr
kind: concept
sources:
- raw/netflix-data-infrastructure/netflix-data-engineer-stack.md
last_updated: '2026-07-15'
qc: passed
slug: netflix-batch-pipeline-four-steps
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Netflix frames a typical batch pipeline implementation as four steps: the transform, ensuring quality, scheduling jobs, and managing the data — a structure vutr took from a 2023 Netflix tech-talk overview of their data engineering stack.

The transform step runs on thousands of Apache Iceberg tables covering the business, with every batch pipeline built on Apache Spark, which gives first-class support for SQL, Python, and Scala so users pick whichever language suits their use case. For SQL users specifically, a tool called the Netflix big data query UI documents which tables a query touches, auto-completes, and acts as one entry point across multiple backend engines — Spark, Trino, Druid, or Snowflake — rather than forcing users to know each engine's own client. For heavy jobs like backfills, a UI tool called go/boost lets users register the compute resources those jobs need.

The quality step is the [[write-audit-publish-pattern]], backed by native unit test libraries, a Spark-specific test library, and Dataflow Mock Generation for realistic test data. The scheduling step is [[maestro-workflow-orchestrator]], handling 70,000 workflows and 500,000 job steps a day. The data management step covers cost and lifecycle: a Cost Insights Dashboard monitors compute and storage costs broken down by team, organization, and platform, while a tool called the Aggressive Janitor handles cleaning up unused data and enforcing data retention policies.

Netflix's real-time counterpart to this batch framework is [[keystone-real-time-platform]] (with Flink as the standard real-time engine, Keystone abstracting stream destinations, and [[mantis-observability-agent]] for live debugging) — the two together are presented as the full picture of Netflix's data engineering stack.

*See also: [[write-audit-publish-pattern]] · [[maestro-workflow-orchestrator]] · [[keystone-real-time-platform]]*
