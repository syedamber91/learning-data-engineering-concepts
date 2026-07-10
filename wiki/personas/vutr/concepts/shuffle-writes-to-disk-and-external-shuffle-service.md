---
persona: vutr
kind: concept
sources:
- raw/spark/i-spent-4-hours-learning-apache-spark.md
last_updated: '2026-07-11'
qc: passed
slug: shuffle-writes-to-disk-and-external-shuffle-service
topics:
- spark
---

The tempting assumption is that removing an executor is always a cheap, safe operation — after all, that's exactly what happens under static allocation, where an executor only exits once its application has fully completed, so discarding it costs nothing. Dynamic allocation breaks that assumption. Under [[resource-allocation-and-scheduling-modes|dynamic allocation]], Spark can remove an executor *while the application is still running*, and if that application later tries to access data the removed executor stored or produced, Spark has to recompute it from scratch. Removing an executor mid-run is not free — it can force recomputation.

The mechanism that exists to blunt this cost is graceful decommissioning: before an idle executor is actually removed, Spark tries to preserve whatever it was holding, effectively making the executor "a bit stateless" first rather than just killing it outright.

The concrete case the source walks through is shuffle output. During a shuffle, an executor writes its map outputs to local disk, and then — critically — that same executor also acts as the serving endpoint other executors fetch those files from. That coupling is the actual problem: if the executor that wrote the shuffle files is removed, the files it was serving become unreachable, and downstream tasks that need them trigger a recompute of the upstream stage.

The fix is to decouple *storage* of shuffle files from the *lifetime* of the executor that produced them. That's what the external shuffle service does: it's a long-running process on each cluster node that runs independently of any particular Spark application or executor. Once this service is in place, executors fetch shuffle files from the service rather than from each other directly. That one change is what makes the earlier problem go away — shuffle data written by an executor keeps being served by the node-level service even after that executor has been terminated, so dynamic allocation can reclaim the executor without forcing a recompute of its shuffle output.

It's worth being precise about what this solves and what it doesn't. The external shuffle service only addresses shuffle map output. Executors also cache data, on disk or in memory, and that caching path is not covered by the same node-level service — when an executor holding cached data is removed, the cached data is simply gone. The workaround the source gives is configuration, not a systemic fix: users can mark executors that hold cached data so they are never removed by default. The asymmetry is the point — shuffle output gets a proper decoupled service, [[executor-memory-model-and-caching|cached data]] gets a manual opt-out instead.

The source flags where this is headed rather than where it already is: cached data may eventually be stored off-heap and managed independently of the executor's lifetime, the same pattern the external shuffle service already applies to shuffle data. That's a stated direction, not a shipped mechanism — don't treat it as current behavior.

Mechanically, the removal trigger that puts this whole system into play is `spark.dynamicAllocation.executorIdleTime`: an executor is removed once it has sat idle for that configured interval. It's at that removal moment — not at request time — that the shuffle-service decoupling actually matters, because that's when an executor without the service would otherwise take its shuffle files with it. The external shuffle service is, in effect, the piece of infrastructure that makes the remove policy safe to execute aggressively instead of leaving shuffle data hostage to executor idle timeouts.
