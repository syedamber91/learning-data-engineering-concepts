---
persona: vutr
kind: concept
sources:
- raw/meta-data-stack-and-infrastructure/how-did-meta-modernize-their-lakehouse.md
last_updated: '2026-07-15'
qc: passed
slug: presto-on-spark-architecture
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

When Meta tried to migrate its batch pipelines off the Hive engine (and its later replacement, SparkSQL) onto the same Presto that was winning the interactive-query consolidation, it ran into a real conflict: at the time, Presto's architecture wasn't resilient enough to machine failures for Meta's long-running batch pipelines, while Spark was. Rather than pick one engine and lose the other's strength, Meta built Presto on Spark — refactoring Presto's front end (parser, analyzer, optimizer, planner) and back end (evaluation, I/O) into libraries embedded inside the Spark driver and worker processes. The result runs PrestoSQL queries with Spark's fault-tolerant execution model underneath.

The payoff the source calls out explicitly is query portability: because interactive queries already ran on Presto, and Presto on Spark offers "100% compatibility with PrestoSQL," users could move a query from the interactive tier straight into a production batch pipeline without rewriting it — one dialect ([[coresql]]-descended PrestoSQL) now serving two very different execution models. Presto on Spark was in production running thousands of pipelines daily at the time of the source article, making it Meta's concrete answer to a tension that any large consolidation effort eventually hits: sometimes the "one engine" goal is better served by embedding one engine's query brains inside another engine's execution runtime than by picking a single winner outright.

*See also: [[shared-foundations-consolidation]] · [[coresql]] · [[velox]]*
