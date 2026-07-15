---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/data-engineering-system-design-11.md
last_updated: '2026-07-15'
qc: passed
slug: pull-vs-push-source-types
topics:
- change-data-capture-cdc-and-data-sourcing
---

Vu's first data-sourcing question is "what is the type of the source?" — and he treats it as the question that changes everything else: the infrastructure you need, the kind of connection you build, and the failure modes you have to prepare for. He splits sources into two categories. Pull-based is "knock, knock, give me some data": databases you query directly or export from, APIs (REST or GraphQL) you call while handling pagination and rate limits, files someone drops in S3 that you wake up and pick up, and — perhaps counterintuitively — Kafka, because even consuming a topic is a pulling model: the consumer continuously polls the broker for new messages. Push-based is "shut up and receive the data," with the webhook as the canonical example: the source calls your endpoint when something happens.

The reason this distinction matters in practice is that each type demands a different setup. A database source might need a read replica so your pipeline doesn't compete with production queries. An API source needs pagination logic and rate-limit handling. A push-based source requires you to run a receiver that's always available and can absorb peak load — you can't just "poll again later" if the sender is the one initiating contact.

*See also: [[source-performance-impact-by-type]] · [[incremental-extraction-strategies]] · [[source-access-trust-boundary]]*
