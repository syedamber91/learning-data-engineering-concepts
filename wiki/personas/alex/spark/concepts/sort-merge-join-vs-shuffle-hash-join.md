---
persona: alex
kind: concept
sources:
- vutr/sort-merge-join-vs-shuffle-hash-join
last_updated: '2026-07-10'
qc: passed
slug: sort-merge-join-vs-shuffle-hash-join
topics:
- spark
learner: alex
source_note: sort-merge-join-vs-shuffle-hash-join
mastery: mastered
---

Okay wait, so — both of these start the exact same way? Before Spark can join anything, it has to physically move matching rows onto the same machine, otherwise a row on Computer A that should match a row on Computer B would just never meet. That's the shuffle, and every join type pays it. It clicked for me like sorting mail into P.O. boxes before anyone can read it — you can't hand out mail until it's in the right box.

Then they diverge. Sort-Merge Join is like alphabetizing two stacks of index cards and walking through both with one finger on each stack — whichever finger is "behind" alphabetically moves forward, and when both fingers land on the same value, that's a match. It only walks each stack once, which is why it's O(n+m), no backtracking.

Shuffle Hash Join instead picks whichever stack is smaller and builds a lookup index from it (a phone book — key in, row out), then walks the *other*, bigger stack, checking each card against the phone book. No alphabetizing needed, which sounds faster — except the phone book must fully fit in memory, and if a partition is unexpectedly huge (skew), it crashes with an OOM instead of degrading. Sort-Merge spills to disk instead. That's *why* SHJ got removed in 1.6 and only came back in 2.0 as opt-in — faster when the small side fits, but a gamble by default, so Spark makes you flip two settings to even try it.

*Source: [[sort-merge-join-vs-shuffle-hash-join]] (vutr)*
