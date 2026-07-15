---
persona: vutr
kind: concept
sources:
- raw/linkedin-data-infrastructure/4-trillion-events-daily-at-linkedin.md
last_updated: '2026-07-15'
qc: passed
slug: unified-batch-stream-pipelines-via-beam
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

LinkedIn's real-time infrastructure processes about 4 trillion events daily across roughly 3,000 pipelines for over 950 million users. Before 2016, that traffic ran through a custom-built ecosystem: Kafka (built in 2010 as the ingestion backbone), an in-house streaming framework called Samza, Spark for batch, plus Brooklin (streaming data across stores and messaging systems) and Venice (a storage system for batch and stream results). Spark and Samza together formed a Lambda architecture — and Lambda's signature disadvantage is that it demands two codebases and two separate engines for what is conceptually the same logic.

The concrete pain this caused shows up in LinkedIn's standardization pipelines — a series of jobs that use AI models to map free-text user input (job titles, skills) into predefined internal IDs for job recommendations. This process needed both real-time processing, to react to user updates immediately, and periodic backfill, to re-run history whenever a new AI model shipped. Under Lambda, the backfill job alone required over 5,000 GB-hours of memory and nearly 4,000 CPU-hours — the two-codebase tax made concrete in compute cost.

Apache Beam, an open-source programming model released in 2016, is what let LinkedIn ask a different question: "is it possible to maintain one codebase but with the ability to run it as either a batch job or streaming job?" LinkedIn built a Samza runner for Beam in 2018, and by 2019 Beam pipelines were powering several critical use cases (see [[apache-beam]] for the framework itself, [[managed-beam-platform]] for how LinkedIn productized it internally). Migrating the standardized pipeline to a unified Beam pipeline cut resource use by half — from roughly 5,000 GB RAM-hours and 4,000 CPU-hours down to roughly 2,000 GB RAM-hours and 1,700 CPU-hours — and cut processing time from 7.5 hours to 25 minutes.

The same unified-pipeline pattern repeats in other LinkedIn systems. The Anti-Abuse AI Team runs two chained streaming Beam pipelines: a filter pipeline that consumes user-activity events from Kafka, extracts fields, aggregates, and filters them; and a model pipeline that consumes the filtered stream, aggregates member activity over defined time windows, triggers AI scoring models, and writes abuse scores downstream. That two-stage design, running on the same Beam abstraction, reduced the time to label abusive actions from 1 day to 5 minutes at a throughput of over 3 million queries per second. LinkedIn's Notifications Platform runs on Beam and Samza the same way — consuming, aggregating, and processing activity events across all LinkedIn members and feeding the results into ML models that drive personalized notifications.

What unifies all three cases is the same trade Beam is built to make: write the business logic once, and let Beam's pluggable runner architecture (plus its I/O connectors, e.g. to Kafka and key-value stores) decide whether it executes as a real-time or backfill job — abstracting away the underlying infrastructure so LinkedIn can switch data-processing engines without rewriting the pipeline.

*See also: [[apache-beam]] · [[managed-beam-platform]] · [[linkedin-data-infrastructure]]*
