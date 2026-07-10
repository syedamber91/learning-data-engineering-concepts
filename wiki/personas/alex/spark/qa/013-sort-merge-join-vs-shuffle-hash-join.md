---
persona: alex
kind: concept
sources:
- vutr/sort-merge-join-vs-shuffle-hash-join
last_updated: '2026-07-10'
qc: passed
slug: 013-sort-merge-join-vs-shuffle-hash-join
topics:
- spark
learner: alex
source_note: sort-merge-join-vs-shuffle-hash-join
mastery: mastered
---

*What Alex understood:* Okay wait, so — both of these start the exact same way? Before Spark can join anything, it has to physically move matching rows onto the same machine, otherwise a row on Computer A that should match a row on Computer B would just never meet. That's the shuffle, and every join type pays it. It clicked for me like sorting mail into P.O. boxes before anyone can read it — you can't hand out mail until it's in the right box.

Then they diverge. Sort-Merge Join is like alphabetizing two stacks of index cards and walking through both with one finger on each stack — whichever finger is "behind" alphabetically moves forward, and when both fingers land on the same value, that's a match. It only walks each stack once, which is why it's O(n+m), no backtracking.

Shuffle Hash Join instead picks whichever stack is smaller and builds a lookup index from it (a phone book — key in, row out), then walks the *other*, bigger stack, checking each card against the phone book. No alphabetizing needed, which sounds faster — except the phone book must fully fit in memory, and if a partition is unexpectedly huge (skew), it crashes with an OOM instead of degrading. Sort-Merge spills to disk instead. That's *why* SHJ got removed in 1.6 and only came back in 2.0 as opt-in — faster when the small side fits, but a gamble by default, so Spark makes you flip two settings to even try it.

## Follow-up questions

**Alex:** If Spark already figures out which side is smaller to build the hash table for SHJ, why doesn't it just always use SHJ with that smaller side instead of defaulting to SMJ? Sorting both sides in SMJ seems like strictly extra work compared to just hashing the small side once — so what's actually stopping Spark from doing that by default and just spilling to disk *only if* the hash table doesn't fit, instead of always paying the sort cost up front?

**vutr:** Good catch, and the note actually answers this directly: it's not that SMJ is "extra work for no reason" — it's a reliability trade-off, and the trade-off is exactly why SHJ got pulled from Spark in the first place. SHJ's build phase requires the *entire* build-side partition to fit in memory to construct the hash table. If a partition is unexpectedly large — skew is the named cause — the executor throws an OutOfMemoryError and the job just dies, full stop. SMJ has no such hard requirement: because the data is sorted, it can spill to disk if a partition is too big, so it degrades gracefully instead of crashing. That's literally "the actual reason SHJ was removed in Spark 1.6" — Spark chose the strategy that fails safely as the default, even though it costs more up front (the sort), over the strategy that's faster in the best case but crashes in the worst case. SHJ was only reintroduced in 2.0 as something you opt into, for when you specifically know the build-side partitions will fit — which is why forcing it takes two deliberate settings (`preferSortMergeJoin=False` and raising `maxShuffledHashJoinLocalMapThreshold` above its default of 0) rather than Spark just guessing dynamically per-partition.

**Alex:** The shuffle step already uses a hash function to decide which partition/worker a row goes to, and then Shuffle Hash Join hashes the join keys *again* to build the lookup table during the build phase. Isn't that hashing the same keys twice? Why doesn't Spark just reuse the routing done in the shuffle step as the hash table itself instead of doing a second hashing pass once the data lands on the worker?

**vutr:** This one the note can answer too, and the short version is: those two hashes are doing genuinely different jobs, at different scopes. The shuffle-level hash is a distribution/routing decision — it's used to decide which partition a row is sent to over the network so that matching keys from both tables *end up co-located in the first place*; the note describes this as data being "divided (usually by a hash function) and distributed to workers." Once that's done, a partition is just a local pile of rows sitting on one machine, still unsorted and unindexed. The build-phase hash in SHJ is a completely separate, local, in-memory structure built *after* the data has already arrived — it maps join keys to actual row data specifically so the probe phase can do fast lookups without scanning. So it's not redundant hashing of the same problem twice: the first hash gets the right rows onto the right machine, and the second hash organizes those rows, once they're already there, into something you can query row-by-row. Reusing the shuffle's routing as the lookup table wouldn't work because the shuffle hash only tells you *where* a row went, not a queryable key-to-row index you can probe against.
