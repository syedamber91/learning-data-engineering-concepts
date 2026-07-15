---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/my-framework-to-build-a-data-pipeline.md
- raw/data-pipeline-design-framework-additional/how-to-build-a-data-pipeline-thats.md
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9-4c5.md
last_updated: '2026-07-15'
qc: passed
slug: idempotency
topics:
- airflow
- data-pipeline-design-framework
---

Idempotency means performing the same operation multiple times produces the same result as performing it once — the property that keeps a pipeline's data in a good state no matter how many times a step runs. It matters because reruns are not an edge case; they are routine. A step gets retried automatically after a failure, backfilled deliberately after a logic change, or rerun manually while debugging, and every one of those reruns carries the same risk: if the pipeline isn't carefully designed, rerunning it can silently produce duplicate, corrupted, or inconsistent data.

Vu Trinh's fix is to make idempotency a property you design in proactively rather than hope for. The concrete techniques he names: overwrite whole tables or partitions instead of doing naive appends/inserts, so a rerun replaces rather than adds; use MERGE/upsert semantics, matching on a unique key and replacing, so duplicate runs converge on the same final state; and avoid non-deterministic functions — `NOW()`, `CURRENT_TIMESTAMP`, `RAND()` — since any function whose output changes between runs breaks the guarantee by construction. Idempotency and reproducibility travel together for him: if a job isn't idempotent, rerunning it for debugging won't even reproduce the same bug, because the output itself keeps shifting.

The property has one hard requirement he calls out explicitly: it has to be end-to-end, not partial. If a pipeline's first two steps correctly overwrite their output but the final step naively appends, the whole pipeline is not idempotent — one non-idempotent step downstream undoes the guarantee every upstream step worked to establish. He treats it as an all-or-nothing chain rather than a per-step checklist.

This is also a design decision that recurs by name across every layer he writes about, not just orchestration: the same overwrite/MERGE/no-non-deterministic-functions logic he applies to a processing step, he applies again to serving-layer writes, where the added twist is that the *sink itself* — not just the job re-running — has to detect and absorb a duplicate logical write (see the serving-side treatment in [[safe-writes-and-schema-evolution-in-serving]]).

*See also: [[kubernetes-executor]] · [[assets]] · [[celery-executor]] · [[trigger-rules]] · [[local-executor]] · [[xcom]] · [[pipeline-failure-recovery-and-checkpointing]] · [[backfilling-data-pipelines]]*
