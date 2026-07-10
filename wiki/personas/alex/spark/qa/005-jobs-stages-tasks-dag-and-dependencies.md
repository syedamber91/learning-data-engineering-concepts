---
persona: alex
kind: concept
sources:
- vutr/jobs-stages-tasks-dag-and-dependencies
last_updated: '2026-07-10'
qc: passed
slug: 005-jobs-stages-tasks-dag-and-dependencies
topics:
- spark
learner: alex
source_note: jobs-stages-tasks-dag-and-dependencies
mastery: mastered
---

*What Alex understood:* Wait, so it's not "Spark runs a job" like one blob — it's more like a recipe with checkpoints. Nothing even starts cooking until I actually ask for the dish, like calling count() — that's the action, and only then does the whole job kick off. Before that it's just a written-down plan.

Then inside the job, Spark has to figure out where it's allowed to keep working in one unbroken line versus where it has to stop and redistribute everything — that's the narrow vs wide dependency thing. If an operation like map only needs data from one known parent partition, Spark can just chain a bunch of those together, no need to stop, that's one stage. But the second you hit something like groupByKey or join, where one partition's data has to scatter out to a bunch of other partitions, Spark can't fake that — it has to physically shuffle the data across the cluster, and that's a hard stop. New stage. It's like a relay race where you can only hand off the baton at specific marked zones (the shuffle points), not wherever you feel like.

And stages aren't all the same job either — a ShuffleMapStage is basically the "prep and hand-off" stage, its whole purpose is writing out the shuffle data, while the ResultStage is the very last one that actually produces the answer.

Below that, tasks are just the same code copy-pasted across every partition, running in parallel on different executors — like giving the same instructions to a bunch of workers who each only handle their own slice of the data.

And the DAG is the map that ties it together — the DAGScheduler walks backward from the final RDD all the way to the source, finds every shuffle boundary, and builds stages in an order where nothing runs before its dependencies are done. It's not scheduling things randomly and hoping — it's topological, like you can't frost a cake before you've baked it.

The failure part surprised me — it's not "task failed, retry it" for everything. If shuffle files got lost, that's on the DAGScheduler, which may rerun the stages that produced that data. If a task fails for some other reason, the TaskScheduler retries that one task a limited number of times before giving up on the whole stage.

## Follow-up questions

**Alex:** You said the DAGScheduler computes preferred locations from cache status and things like HDFS block locations so tasks get scheduled close to their data — but what actually happens if that preferred executor is busy or the data isn't local at scheduling time? Does the task just wait, or does it run somewhere else and eat the network cost?

**vutr:** That one's answerable straight from the mechanics: pipelining only works when each task can produce its output partition using nothing but data that's already sitting with it — that's exactly what a narrow dependency guarantees, a limited, knowable set of parent partitions (often just one) feeding each child partition. A map task can run start to finish on the executor where its input partition already lives.

A wide dependency breaks that guarantee at the root: one parent partition's data has to contribute to *multiple* child partitions, which by definition means that data has to leave its current location and get redistributed across the cluster — the note is explicit that this "forces data to be repartitioned across the cluster." There's no way to keep that inside one task's local, sequential pipeline, because the task doing the reducing needs input that physically lives on other machines. That's why the note draws the stage boundary exactly at wide dependencies: the ShuffleMapStage's whole job is to do that shuffle write, so the data is materialized and available before the next stage's tasks read it. You can't pipeline across that because the data literally doesn't exist in its needed form and location until the shuffle write completes.

**Alex:** If narrow operations like map can all get pipelined into one stage because Spark knows exactly which parent partition feeds which output, why can't Spark just pipeline a wide operation like join the same way instead of stopping everything for a shuffle — like what physically breaks if you tried to keep a groupByKey in the same stage as the map before it?

**vutr:** (the wiki does not cover this — see open questions)
