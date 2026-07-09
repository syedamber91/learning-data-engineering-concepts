---
persona: alex
kind: concept
sources:
- vutr/data-locality
last_updated: '2026-07-09'
qc: passed
slug: 011-data-locality
topics:
- spark
learner: alex
source_note: data-locality
mastery: mastered
---

*What Alex understood:* Data sits in partitions across the cluster and tasks need to run near their data because moving code is cheap but moving data is expensive. The scheduler places each task at the closest locality it can get: PROCESS_LOCAL (data in the same executor process, no transfer), then NODE_LOCAL (same machine, different process, no network hop), then NO_PREF (no preference, place anywhere), then RACK_LOCAL (different machine but same rack, faster local network), then ANY (anywhere else, farthest and slowest). Nearer wins because each step out means shipping data over slower links. And if one task lags (a straggler), speculative execution launches a duplicate on another executor and takes whichever finishes first.

## Follow-up questions

**Alex:** If the scheduler wants PROCESS_LOCAL but no slot is free inside the executor that holds the data, does it wait for a slot to open or immediately fall back to a farther locality level like NODE_LOCAL?

**vutr:** vutr: Good instinct — this is exactly the real tension. Spark does not instantly give up on the best locality. There is a small waiting window (a locality-wait timeout) where the scheduler holds the task briefly hoping a slot frees up at the preferred level; if nothing opens in time, it relaxes one step down the hierarchy — PROCESS_LOCAL to NODE_LOCAL, and so on outward to ANY. It is a trade-off between paying a little idle-wait cost versus paying the data-movement cost of running farther away. The source itself only gives you the ordering nearest-to-farthest, so treat the timeout-and-fallback detail as the mechanism behind that ordering rather than something stated verbatim in this text.

**Alex:** With speculative execution, when the original straggler and its re-submitted duplicate are both running, what happens to the losing copy's work once the faster one finishes?

**vutr:** vutr: When the faster copy finishes its task, that task's result is accepted and the stage moves on, so the slower copy is now redundant — its output is no longer needed and it gets killed/abandoned. The point of speculative execution is purely to stop one straggler from holding up the whole stage; you deliberately 'waste' some duplicate compute to buy back wall-clock time. The source states the mechanism (slow tasks re-submitted to another executor) but does not spell out the cancellation of the loser, so that part is my explanation of how it necessarily resolves, not a direct quote.
