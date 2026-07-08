---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: data-locality
topics:
- spark
---

Spark's scheduler prefers to run a task where its data already lives, ranking locality from nearest to farthest: PROCESS_LOCAL (data in the same JVM) > NODE_LOCAL (same node, different process) > NO_PREF (no locality preference) > RACK_LOCAL (same rack) > ANY (anywhere). It waits briefly for a better level before falling back to a worse one. Speculative execution is the companion mechanism: when a task runs unusually slow, Spark re-submits a duplicate copy to another executor and takes whichever finishes first — a hedge against a straggler node dragging down the whole stage. This preferred-location signal ties back to the [[rdd]]'s fifth property, optional preferred locations.
