---
persona: vutr
kind: concept
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/how-did-discord-evolve-to-handle.md
last_updated: '2026-07-15'
qc: passed
slug: dbt-incremental-race-condition
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Discord's notes call out a specific dbt bug that only surfaces once you try to parallelize incremental models: a race condition over dbt's own temporary table naming.

The mechanism, per the notes: dbt's incremental model creates a temporary table named `destination_table__dbt_tmp`, uses it to update the destination table incrementally, and deletes it once the update finishes. That naming scheme assumes one run per destination table at a time. When Discord tried to run multiple incremental updates against the same table in parallel — each covering a different data range, needed to backfill or process partitions concurrently at their scale — every concurrent run created a temp table with the *same* `__dbt_tmp` name, so one run's in-flight temp table could be deleted or overwritten by another run still using it, causing conflicts.

Discord's fix was to modify dbt's own logic for storing temporary data so that parallel executions of different partitions of the same asset no longer collide — the notes describe the effect (parallel execution of different partitions became safe) without spelling out dbt's original temp-table-naming internals or exactly how Discord's patch scopes the temp table name per run. This is presented as a real, load-bearing customization made to stock dbt behavior rather than a workaround at the orchestration layer, and it sits alongside Discord's other dbt investments — customized dbt CLI commands, a CI/CD process to guard against disruptive changes to table logic, macros, and tests — as part of making dbt usable at Discord's scale rather than accepting it as-is.

*See also: [[discord-declarative-vs-imperative-orchestration]]*

## Open questions
- **source gap**: the notes describe the effect of Discord's fix (parallel partitions of the same asset no longer conflict) but not the mechanism — how the temp table name is actually scoped per run/partition to avoid collision.
