---
persona: alex
kind: concept
sources:
- vutr/executor-memory-model-and-caching
last_updated: '2026-07-10'
qc: passed
slug: 009-executor-memory-model-and-caching
topics:
- spark
learner: alex
source_note: executor-memory-model-and-caching
mastery: mastered
---

*What Alex understood:* Wait, so — okay, I think I finally get why my job crashed even though I set executor memory to "plenty." It's like getting a paycheck and thinking you get to spend all of it, but taxes and rent come off the top first, and only what's left over is your actual spending money. Spark takes a flat 300MB "tax" off every executor no matter what, then a chunk of what's left becomes my "user" money (my own stuff), and only 60% of the remainder — the unified pool — is what I actually get to spend on shuffling, joins, and caching. So a 2GB executor is really only giving me about 1GB to work with. That's wild.

And then inside that leftover pool, there's this tug-of-war between execution (the active shuffle/join/sort work) and storage (my cached data). It's not split in stone anymore like it used to be pre-1.6 — it's more like roommates sharing a closet. If execution needs more space, it can shove into storage's side and force storage to throw out its oldest cached stuff (LRU) until storage shrinks down small enough. But it only goes one way — storage can never shove execution's stuff out to get space back. It can only clean out its own junk. Execution basically always has the right of way because Spark cares more about finishing the current computation than keeping old cache around.

Off-heap is a totally separate fix — it's not about this closet fight at all, it's about Java objects being bloated (a tiny 4-byte string turning into 48+ bytes of overhead) and garbage collection pausing everything. Tungsten just works on raw binary instead of Java objects to dodge that.

And caching isn't free just because it's "in memory" — a compressed 2.6GB file on disk becomes 3.7GB once Spark decompresses it into memory, so caching can actually make your memory problem worse, not better.

## Follow-up questions

**Alex:** If execution can always force storage to evict its cache but storage can never force execution to give space back, what actually stops execution from just grabbing basically all of the unified memory over and over and wiping out my cache completely every single time there's a big shuffle?

**vutr:** Good catch on the asymmetry — execution can evict storage but not vice versa, which sounds like it could go to zero. It can't, though: the note is explicit that when execution reclaims space, "storage is forced to evict using LRU until it falls under the R threshold" — not down to nothing. That phrasing means there's a protected floor (the R threshold) that eviction stops at, so execution can squeeze storage down hard, but not wipe it out completely on every shuffle. I'll be straight with you though: the note names this R threshold as the stopping point but doesn't give the exact formula or value for R, so I can't tell you precisely how big that floor is — just that it exists and caps how far execution can push.

**Alex:** You said doubling executor memory from 2GB to 4GB with the same 2 cores didn't shrink the spill at all, but shrinking the partition size did — that seems backwards, since more memory should mean more room before you spill. Why doesn't more raw memory actually fix it?

**vutr:** This is actually a case where I don't have a clean mechanistic answer, and I said so honestly in the hands-on project: doubling executor memory to 4GB with the same core count left the spill totally unchanged, and that's flagged as unresolved — my working guess is it's tied to SortAggregate's sort overhead rather than raw memory pressure, but it's a guess, not a proven mechanism. What I do have solid evidence for is the more general lesson: it's memory available *per task*, not total executor memory, that controls spill. Shrinking partition size from 256MB to 128MB doubled the number of tasks (84 to 168) and halved the spill while cutting per-task time from 35s to 12s — because each task now handles a smaller slice. And going the other direction, raising cores from 2 to 4 at the same memory *increased* spill from 832MB to 1GB, because more concurrent tasks were now sharing that same memory pool, shrinking each task's effective slice again. So memory-per-task is the lever that actually moves spill; raw executor memory, in this case, wasn't.
