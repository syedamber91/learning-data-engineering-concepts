---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/my-framework-to-build-a-data-pipeline.md
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9-4c5.md
last_updated: '2026-07-15'
qc: passed
slug: backfilling-data-pipelines
topics:
- data-pipeline-design-framework
---

Backfilling, in Vu Trinh's definition, is "loading or recomputing historical data that was missed, incorrect, or not previously processed" — triggered either by a business-logic change that must be re-applied to old data, or by a failure that left data incomplete. Most orchestration frameworks make the mechanics straightforward: Airflow and Dagster let you run a pipeline over any date range, and because they track dependencies between steps, backfilling one step correctly triggers the backfill of everything downstream too — you rarely backfill only the source-pulling task and leave dependent tables stale.

Two constraints decide whether a backfill is actually possible or safe, though. First, [[source-constraints-and-schema-risk|source retention]]: if the source no longer holds the data you need to recompute, there is no way to build the backfill regardless of how good your orchestration is. Second — and this is where his deeper processing-layer treatment goes further than the framework version — whether the pipeline can be backfilled *partially*. That requires the processing logic to operate in partitions (daily, hourly, weekly) so each partition can be fixed in isolation: fixing March 5th means rerunning only March 5th. Treat the dataset as one indivisible whole, and every rerun has to be a full rerun, because there's no safe unit smaller than "everything."

The other risk he names is resource contention: a 90-day backfill can mean up to 90 Airflow DAG runs queued simultaneously, and if each run needs a quarter of total processing capacity, letting even four run at once starves every other workload on the cluster. His two controls are capping the maximum concurrent runs at the orchestration layer, and assigning backfill work to a dedicated resource pool at the processing layer so it can't crowd out regular jobs. He also ties backfill trustworthiness directly to [[testing-data-pipeline-correctness|regression testing]]: comparing the backfilled output against the prior version isn't optional here, since backfills are exactly where "meaningfully different where it should be" needs confirming.

*See also: [[source-constraints-and-schema-risk]] · [[testing-data-pipeline-correctness]] · [[pipeline-failure-recovery-and-checkpointing]] · [[stale-or-incorrect-data-handling]]*
