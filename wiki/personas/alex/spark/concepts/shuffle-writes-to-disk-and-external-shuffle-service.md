---
persona: alex
kind: concept
sources:
- vutr/shuffle-writes-to-disk-and-external-shuffle-service
last_updated: '2026-07-10'
qc: passed
slug: shuffle-writes-to-disk-and-external-shuffle-service
topics:
- spark
learner: alex
source_note: shuffle-writes-to-disk-and-external-shuffle-service
mastery: mastered
---

Wait, so — okay, let me see if I've got this. Normally, if an executor is just a worker that dies when the whole job is done, killing it is like closing a store after all the customers already left. Nothing lost. But with dynamic allocation, Spark can fire a worker in the *middle* of the shift, while other people are still trying to buy stuff from that worker's counter. That's the dangerous part.

And the specific thing that breaks is shuffle files. An executor writes its shuffle output to its own local disk, but it's ALSO the guy standing at the counter handing those files to other executors when they ask for them. So it's not just storage getting removed, it's the delivery guy getting removed too — same person doing both jobs. If Spark fires that executor, the files might physically still be safe somewhere, but nobody knows how to get them anymore, so Spark just gives up and recomputes the whole upstream stage instead. That's wasteful.

So the external shuffle service is like hiring a separate warehouse on each machine that's always open, no matter which workers come and go. Executors drop their shuffle output there instead of guarding it themselves, and other executors pick it up from the warehouse, not from the original worker. So now you can fire the original worker (once idle for `executorIdleTime`) and the warehouse just keeps handing out the files like nothing happened.

But — and this is the part that seems inconsistent — cached data doesn't get a warehouse. If an executor is holding cached data in memory or on disk and gets removed, that data is just gone, no recompute-avoidance trick, nothing. The only protection is telling Spark "don't ever auto-remove this specific executor" if it's holding cache. That feels like a patch, not a real fix, compared to the shuffle service's actual architecture change.

*Source: [[shuffle-writes-to-disk-and-external-shuffle-service]] (vutr)*
