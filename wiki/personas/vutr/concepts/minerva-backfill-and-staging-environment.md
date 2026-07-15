---
persona: vutr
kind: concept
sources:
- raw/airbnb-data-infrastructure/how-did-airbnb-build-their-semantic.md
last_updated: '2026-07-15'
qc: passed
slug: minerva-backfill-and-staging-environment
topics:
- airbnb-data-infrastructure
---

Minerva's "Scalable" and "Highly Available" principles both come down to how it moves and refreshes data without breaking production, and the two solve different halves of the same problem.

On the ingest side, Minerva's computational flow runs through four stages: an **ingestion stage** where sensors trigger on new partitions and pull the latest data in; a **data check stage** that verifies upstream data is "right" (no empty required fields, unique primary keys); a **join stage** that executes joins based on join keys to generate dimension sets, computing the same logic (e.g. the same city dimension) once and reusing it across every dimension set that needs it, rather than recomputing it per consumer; and a **post-processing and serving stage** that aggregates outputs for downstream consumption and can optionally optimize query performance further. That reuse-over-recompute discipline is Minerva's application of the DRY principle at data-pipeline scale, and it's what let Minerva keep serving 5,000+ datasets across 80+ teams without a proportional blowup in compute. Minerva is also "data-aware": it checks for missing data on every job run, and if it finds a gap, it folds that gap into the current run automatically — so a run's data range can change dynamically (e.g. 3 days of data becomes 4) without anyone manually resetting the task.

Backfilling — recomputing history when logic changes — has a scale problem of its own: a long backfill window (say, several months) as one query gets expensive, but splitting it into many small windows makes a large initial backfill too slow. Minerva's answer is batch backfill: split the window into smaller pieces sized to that dataset's scalability characteristics (e.g. a one-year window becomes twelve one-month windows) and run those pieces in parallel.

But backfilling constantly changing datasets creates a second problem: if backfills can't keep pace with how often users change definitions, a frequently-edited dataset could be stuck backfilling forever, causing data downtime for anyone depending on it. Minerva's fix is environment isolation, not faster compute: a parallel **Staging environment** that replicates Production. Users develop and test changes locally, merge them into Staging, Staging loads the Staging configuration (retrieving Production configuration where needed) and backfills the modified datasets there, and only once that backfill finishes do the Staging changes merge into Production. Production consumers never see a dataset mid-backfill — they see the old version until the new one is fully ready.

*See also: [[minerva]] · [[minerva-data-versioning]]*
