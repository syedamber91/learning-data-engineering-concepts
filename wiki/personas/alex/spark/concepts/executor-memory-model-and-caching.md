---
persona: alex
kind: concept
sources:
- vutr/executor-memory-model-and-caching
last_updated: '2026-07-10'
qc: passed
slug: executor-memory-model-and-caching
topics:
- spark
learner: alex
source_note: executor-memory-model-and-caching
mastery: mastered
---

Wait, so — okay, I think I finally get why my job crashed even though I set executor memory to "plenty." It's like getting a paycheck and thinking you get to spend all of it, but taxes and rent come off the top first, and only what's left over is your actual spending money. Spark takes a flat 300MB "tax" off every executor no matter what, then a chunk of what's left becomes my "user" money (my own stuff), and only 60% of the remainder — the unified pool — is what I actually get to spend on shuffling, joins, and caching. So a 2GB executor is really only giving me about 1GB to work with. That's wild.

And then inside that leftover pool, there's this tug-of-war between execution (the active shuffle/join/sort work) and storage (my cached data). It's not split in stone anymore like it used to be pre-1.6 — it's more like roommates sharing a closet. If execution needs more space, it can shove into storage's side and force storage to throw out its oldest cached stuff (LRU) until storage shrinks down small enough. But it only goes one way — storage can never shove execution's stuff out to get space back. It can only clean out its own junk. Execution basically always has the right of way because Spark cares more about finishing the current computation than keeping old cache around.

Off-heap is a totally separate fix — it's not about this closet fight at all, it's about Java objects being bloated (a tiny 4-byte string turning into 48+ bytes of overhead) and garbage collection pausing everything. Tungsten just works on raw binary instead of Java objects to dodge that.

And caching isn't free just because it's "in memory" — a compressed 2.6GB file on disk becomes 3.7GB once Spark decompresses it into memory, so caching can actually make your memory problem worse, not better.

*Source: [[executor-memory-model-and-caching]] (vutr)*
