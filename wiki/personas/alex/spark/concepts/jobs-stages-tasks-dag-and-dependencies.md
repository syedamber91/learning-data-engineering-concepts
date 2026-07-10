---
persona: alex
kind: concept
sources:
- vutr/jobs-stages-tasks-dag-and-dependencies
last_updated: '2026-07-10'
qc: passed
slug: jobs-stages-tasks-dag-and-dependencies
topics:
- spark
learner: alex
source_note: jobs-stages-tasks-dag-and-dependencies
mastery: mastered
---

Wait, so it's not "Spark runs a job" like one blob — it's more like a recipe with checkpoints. Nothing even starts cooking until I actually ask for the dish, like calling count() — that's the action, and only then does the whole job kick off. Before that it's just a written-down plan.

Then inside the job, Spark has to figure out where it's allowed to keep working in one unbroken line versus where it has to stop and redistribute everything — that's the narrow vs wide dependency thing. If an operation like map only needs data from one known parent partition, Spark can just chain a bunch of those together, no need to stop, that's one stage. But the second you hit something like groupByKey or join, where one partition's data has to scatter out to a bunch of other partitions, Spark can't fake that — it has to physically shuffle the data across the cluster, and that's a hard stop. New stage. It's like a relay race where you can only hand off the baton at specific marked zones (the shuffle points), not wherever you feel like.

And stages aren't all the same job either — a ShuffleMapStage is basically the "prep and hand-off" stage, its whole purpose is writing out the shuffle data, while the ResultStage is the very last one that actually produces the answer.

Below that, tasks are just the same code copy-pasted across every partition, running in parallel on different executors — like giving the same instructions to a bunch of workers who each only handle their own slice of the data.

And the DAG is the map that ties it together — the DAGScheduler walks backward from the final RDD all the way to the source, finds every shuffle boundary, and builds stages in an order where nothing runs before its dependencies are done. It's not scheduling things randomly and hoping — it's topological, like you can't frost a cake before you've baked it.

The failure part surprised me — it's not "task failed, retry it" for everything. If shuffle files got lost, that's on the DAGScheduler, which may rerun the stages that produced that data. If a task fails for some other reason, the TaskScheduler retries that one task a limited number of times before giving up on the whole stage.

*Source: [[jobs-stages-tasks-dag-and-dependencies]] (vutr)*
