---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/my-framework-to-build-a-data-pipeline.md
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9-4c5.md
- raw/data-pipeline-design-framework-additional/how-to-build-a-data-pipeline-thats.md
last_updated: '2026-07-15'
qc: passed
slug: pipeline-failure-recovery-and-checkpointing
topics:
- data-pipeline-design-framework
---

Vu Trinh's baseline stance is blunt: "when the pipeline fails, you can't let it just fail" — there must be a mechanism to bring it back, and ideally that recovery is automatic rather than manual. He splits the recovery question into two layers: does the orchestration layer (Airflow, Dagster, Prefect) or the processing layer itself (Spark, Snowflake, BigQuery) handle the retry, and — the more consequential question — when the pipeline comes back, does it restart from the beginning or resume from where it failed?

Checkpointing is his answer to that second question when the processing framework supports it: mechanisms like Flink's or Spark's checkpoints track which pieces of data have already been processed, so on recovery the system resumes only the unprocessed remainder instead of redoing completed work. For frameworks without built-in checkpointing, he describes an equivalent pattern built by hand: persist each step's output to a separate store (object storage) rather than passing data directly between tasks, so that if step 3 of a 3-step pipeline fails, the pipeline can rerun just step 3 and pick up step 2's result from where it was written — turning a monolithic failure into a resumable one.

His satirical inverse makes the stakes explicit: a pipeline built to fail on purpose is one that skips exactly these questions — no self-healing, no backoff on retries, no thought for whether retrying stresses the source or corrupts the sink with duplicate inserts, no plan for where steps A and B's intermediate output goes if step C fails. Treating "does it restart from the beginning" as an afterthought is, in his framing, one of the more reliable ways to guarantee a pipeline that never recovers cleanly.

*See also: [[idempotency]] · [[backfilling-data-pipelines]] · [[dead-letter-queue-and-bad-data-isolation]]*
