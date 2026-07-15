---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/data-engineering-system-design-11.md
last_updated: '2026-07-15'
qc: passed
slug: incremental-extraction-strategies
topics:
- change-data-capture-cdc-and-data-sourcing
---

How often you need to touch a source is tightly coupled to how stale the business is willing to let the data get. Vu's rule of thumb: don't over-engineer the freshness. If a user checks a dashboard once a day and is happy calling the daily refresh "real-time," there's no reason to build a streaming pipeline — a scheduled batch job (Cron, Airflow) is fine. Only when the real answer is near real-time do you need continuous extraction: CDC, streaming consumers like a Kafka consumer, or sensors that react to new data as it arrives (e.g., an Airflow sensor).

But underneath the cadence question sits a harder one: on each run, how do you know what's actually new? Reading an entire table every run is wasteful and, for large tables, often impractical. Vu lays out five common answers, in ascending order of what they guarantee: timestamp-based extraction (`WHERE updated_at > last_run_time`) is simple but silently breaks the moment someone updates a record without advancing the timestamp; the overlap date range approach deliberately re-fetches a wider window than the last run (e.g., always pulling "X days ago" through today) and relies on downstream deduplication, last-come-first-served, to discard the overlap; offset-based extraction, as in Kafka, has the consumer tell the broker which offset it last consumed and continuously poll from there; CDC has the source emit every change as an event — the most reliable option when it's available, and also the most complicated to build; and full refresh is sometimes simply the right answer for small, stable reference tables that don't justify any incremental machinery at all.

Read together, this is the toolbox that [[query-based-cdc]], [[trigger-based-cdc]], and [[log-based-cdc]] slot into: CDC is one strategy for answering "what's new," not the only one, and Vu's framing makes clear it earns its complexity only when the freshness requirement and the absence of a reliable timestamp column actually demand it.

*See also: [[query-based-cdc]] · [[log-based-cdc]] · [[pull-vs-push-source-types]] · [[source-retention-and-replayability]]*
