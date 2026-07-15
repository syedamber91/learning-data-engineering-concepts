---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/everything-you-need-to-know-about-741.md
last_updated: '2026-07-15'
qc: passed
slug: query-based-cdc
topics:
- change-data-capture-cdc-and-data-sourcing
---

Query-based CDC (also called polling-based CDC) is the simplest of the three CDC types to implement, and also the most limited. It periodically runs a SQL query against a dedicated column on the source table — typically `updated_timestamp` — checking for rows changed since the last run. The process keeps a checkpoint (the timestamp of the last run), queries for everything newer than that checkpoint, then advances the checkpoint for the next run.

Its appeal is pure simplicity: standard SQL, no special database features required. But every one of its weaknesses traces back to the same root cause — it can only see what a `SELECT` can see. Once a row is physically deleted, there's nothing left for a subsequent query to select, so DELETE operations are silently skipped and the target drifts out of sync with the source. Frequent polling of large tables also puts real pressure on the source, which is why polling queries are often routed to a read-only replica instead of the primary. Freshness is capped by the polling interval — a five-minute poll means data can be up to five minutes stale. And the whole approach depends on the table actually having a usable timestamp column in the first place; if a colleague forgot to add one, query-based CDC simply isn't available for that table.

*See also: [[trigger-based-cdc]] · [[log-based-cdc]] · [[incremental-extraction-strategies]] · [[source-delete-handling]]*
