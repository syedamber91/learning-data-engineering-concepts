---
persona: vutr
kind: concept
sources:
- raw/spark/i-spent-8-hours-learning-apache-spark.md
last_updated: '2026-07-11'
qc: passed
slug: data-locality-and-speculative-execution
topics:
- spark
---

Data locality and speculative execution aren't two separate subsystems bolted onto Spark's scheduler — both live inside the **TaskSetManager**, the component that schedules the tasks of a single TaskSet. It's worth naming that up front, because it's easy to think of "where a task runs" and "what happens if a task is slow" as unrelated concerns. They're not: both are the TaskSetManager reacting to the same underlying problem — an executor isn't behaving the way you'd want, either because the data isn't there yet or because the task on it is dragging.

## Where locality preference comes from

Locality isn't decided by the TaskSetManager itself. The **DAGScheduler** computes the preferred locations for each task in a stage — based on the preferred locations of the underlying RDDs, or the location of cached or shuffle data — and passes that along with the TaskSet to the TaskScheduler. This is part of the same DAGScheduler responsibility as cache tracking: it already knows which RDDs are cached (to avoid recomputing them) and which shuffle map stages produced which output files, so it's positioned to say "task X should ideally run near data Y."

The TaskSetManager then tries to honor that preference, using five locality levels, ordered nearest to farthest:

- **PROCESS_LOCAL** — task runs on the same executor where the data resides
- **NODE_LOCAL** — same node, different executor
- **NO_PREF** — data is accessed equally quickly from anywhere; no local preference
- **RACK_LOCAL** — same rack, different node
- **ANY** — no locality preference is satisfied; runs wherever there's a free slot

## The mechanism: delay scheduling

The actual trick that makes locality-aware scheduling work is **delay scheduling**, and the idea is simple: when a task is ready to be scheduled, the TaskSetManager first checks whether an available executor currently holds the desired locality level. If one does, great, the task runs there. If none does, the TaskSetManager does *not* immediately fall back to a worse locality — it waits a short, configurable period, betting that a local executor will free up during that window. Only if the delay expires with no satisfied executor available does it relax to a "farther" locality level and launch the task there.

That's the whole mechanism — it's a bet, traded off against wait time. Hold out too long for PROCESS_LOCAL and you waste cluster time; give up too fast and you pay for cross-network reads. The source doesn't give the actual delay duration, just that it's short and configurable.

## Speculative execution

Speculative execution is a separate health-check the TaskSetManager runs on top of this: it watches for tasks that are taking abnormally long — the source's example is hardware problems on a given executor — and, when `spark.speculation = true`, re-submits ("speculates") a copy of that slow task onto a different executor, running both copies **in parallel**. Critically, the TaskSetManager does not kill the original slow task first — it lets both run, and whichever copy finishes successfully first is kept; the other copy is killed once a winner exists.

So the connective thread between the two mechanisms: data locality decides *where* a task should ideally start, using a wait-and-see delay before compromising; speculative execution is the *escape hatch* for when a task is already running but is going too slowly, dealing with the problem by resubmission and a race rather than diagnosis. Locality is about placement before execution; speculation is a runtime backstop once placement didn't guarantee good performance. Both sit downstream of the same [[jobs-stages-tasks-dag-and-dependencies|TaskSet]] handed off by the DAGScheduler, and both are handled entirely inside the TaskSetManager rather than by the TaskScheduler or SchedulerBackend, which are only responsible for resource offers and launching serialized task descriptions — see [[spark-application-architecture-and-execution-modes]] for how those pieces fit together.
