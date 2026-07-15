---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-15'
qc: passed
topic: olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
status: superseded
---

Related: [[bigquery-internals]] · [[snowflake-internals]] · [[clickhouse-internals]] · [[olap-cost-and-multi-engine-comparison]] · [[single-node-engines-duckdb-polars-vs-distributed-systems]]

## This topic has been split and superseded

This page originally covered BigQuery, Snowflake, ClickHouse, Redshift, DuckDB, and Databricks/Photon in one merged, snapshot-only topic (no real raw grounding — just a compressed persona document). Once vutr's own dedicated posts on these engines were ingested, the material was deep enough to warrant separate, focused topics rather than staying merged:

- **[[bigquery-internals]]** — Dremel, Vortex, Napa, Capacitor, disaggregated shuffle (9 dedicated posts)
- **[[snowflake-internals]]** — storage tiering, locality-aware scheduling, virtual-warehouse isolation, Cascades optimizer (3 dedicated posts)
- **[[clickhouse-internals]]** — MergeTree mechanics, Keeper/Raft replication, Tinybird case study (4 dedicated posts)
- **[[olap-cost-and-multi-engine-comparison]]** — cross-vendor pricing, Redshift's storage/compute internals (RMS, AutoWLM, AQUA), incremental view maintenance, real-time freshness (7 dedicated posts) — this is where Redshift finally got real depth; it previously had only a 4-sentence ungrounded stub
- **[[single-node-engines-duckdb-polars-vs-distributed-systems]]** — DuckDB's embedded/vectorized model (pre-existing topic, separately re-grounded)

**Known remaining gap:** Databricks/Photon was never re-grounded — no raw post covering it was found or ingested in this pass. The old snapshot referenced a "photon" entity that doesn't actually exist in this wiki (a dangling reference inherited from the original 2026-07-08 snapshot construction, not introduced here). If vutr's own writing on Databricks/Photon is ever captured, it needs its own ingest — there is currently zero grounded coverage of it in this wiki.

**Also flagged, not yet addressed:** the entity-level stubs `[[bigquery]]`, `[[snowflake]]`, `[[clickhouse]]`, `[[redshift]]`, `[[google-napa]]`, `[[bigquery-vortex]]`, and the concept `[[vectorized-vs-code-compilation]]` (vectorized execution vs. code-generation/JIT across these same engines) are still `sources: persona-snapshot` even though the topics above now cover the same engines in much greater grounded depth. They were deliberately left alone during the split (the per-engine agents didn't want to touch files outside their own scope), so several other notes still link to these shallow stubs rather than the deep topics. A follow-up pass could either retire these stubs the same way this page was retired, or fold them into the deep topics and repoint their inbound links.
