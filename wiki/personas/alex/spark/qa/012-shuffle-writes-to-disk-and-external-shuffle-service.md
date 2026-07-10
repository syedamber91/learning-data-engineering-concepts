---
persona: alex
kind: concept
sources:
- vutr/shuffle-writes-to-disk-and-external-shuffle-service
last_updated: '2026-07-10'
qc: passed
slug: 012-shuffle-writes-to-disk-and-external-shuffle-service
topics:
- spark
learner: alex
source_note: shuffle-writes-to-disk-and-external-shuffle-service
mastery: mastered
---

*What Alex understood:* Wait, so — okay, let me see if I've got this. Normally, if an executor is just a worker that dies when the whole job is done, killing it is like closing a store after all the customers already left. Nothing lost. But with dynamic allocation, Spark can fire a worker in the *middle* of the shift, while other people are still trying to buy stuff from that worker's counter. That's the dangerous part.

And the specific thing that breaks is shuffle files. An executor writes its shuffle output to its own local disk, but it's ALSO the guy standing at the counter handing those files to other executors when they ask for them. So it's not just storage getting removed, it's the delivery guy getting removed too — same person doing both jobs. If Spark fires that executor, the files might physically still be safe somewhere, but nobody knows how to get them anymore, so Spark just gives up and recomputes the whole upstream stage instead. That's wasteful.

So the external shuffle service is like hiring a separate warehouse on each machine that's always open, no matter which workers come and go. Executors drop their shuffle output there instead of guarding it themselves, and other executors pick it up from the warehouse, not from the original worker. So now you can fire the original worker (once idle for `executorIdleTime`) and the warehouse just keeps handing out the files like nothing happened.

But — and this is the part that seems inconsistent — cached data doesn't get a warehouse. If an executor is holding cached data in memory or on disk and gets removed, that data is just gone, no recompute-avoidance trick, nothing. The only protection is telling Spark "don't ever auto-remove this specific executor" if it's holding cache. That feels like a patch, not a real fix, compared to the shuffle service's actual architecture change.

## Follow-up questions

**Alex:** If the external shuffle service is what makes removing an executor safe for shuffle data, why wasn't the same warehouse-style service just built for cached data too instead of relying on a 'never remove this executor' flag as a workaround?

**vutr:** The note explicitly frames this as a stated asymmetry rather than an oversight it can fully explain: shuffle output gets a proper decoupled node-level service, while cached data gets a manual opt-out (marking executors holding cached data so they're never removed by default) instead of a systemic fix. The note does say the direction of travel is toward closing that gap — cached data may eventually be stored off-heap and managed independently of executor lifetime, the same pattern the external shuffle service already applies to shuffle data — but it's explicit that this is a stated future direction, not a shipped mechanism. So the honest answer from the note is: the external shuffle service exists today for shuffle output, an equivalent for caching doesn't exist yet, and the note doesn't give the underlying engineering reason why caching wasn't solved the same way from the start.

**Alex:** The removal trigger is executorIdleTime — an executor only gets killed once it's sat idle for that interval. But during an active shuffle, is the executor serving files 'idle' the whole time, or could Spark try to remove an executor that's mid-write on its shuffle output, and if so does graceful decommissioning cover that in-progress case or only the already-idle case?

**vutr:** (the wiki does not cover this — see open questions)
