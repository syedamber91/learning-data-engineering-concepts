---
persona: vutr
kind: entity
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/how-does-notion-handle-200-billion.md
last_updated: '2026-07-15'
qc: passed
slug: notion-block-model
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

A block is Notion's single universal unit of content — text, images, lists, database rows, and even entire pages are all blocks, and the notes describe them as Notion's "LEGOs": dynamic units that can be transformed into other block types or moved freely within the product. This uniform representation is also what made Notion's underlying data-scale problem so distinctive: every kind of content the product supports funnels into the same storage model, so the same scaling story (Postgres sharding, then a CDC-fed data lake) applies uniformly across notes, databases, and pages alike.

The block count itself is the notes' scale marker for Notion's growth: more than 20 billion blocks in 2021, growing to more than 200 billion by the time of writing. Before 2021, all blocks lived in a single Postgres instance; Notion then sharded that instance into 480 logical shards spread across 96 Postgres instances (5 shards per instance) to keep the operational database itself scalable, a step that came before — and was distinct from — the separate analytics-infrastructure rebuild described in [[notion-postgres-to-datalake-migration]].

*See also: [[notion-postgres-to-datalake-migration]]*
