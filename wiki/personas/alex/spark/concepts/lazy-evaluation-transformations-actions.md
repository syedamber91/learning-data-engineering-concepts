---
persona: alex
kind: concept
sources:
- vutr/lazy-evaluation-transformations-actions
last_updated: '2026-07-10'
qc: passed
slug: lazy-evaluation-transformations-actions
topics:
- spark
learner: alex
source_note: lazy-evaluation-transformations-actions
mastery: mastered
---

Wait, so it's not like a recipe where you cook step 1 the second you write it down — it's more like I'm handing someone a stack of index cards, each one just saying 'take whatever the card before me produces and do THIS to it,' but nobody's actually cooking anything yet. Nobody lights the stove until I say 'action' — like, actually serve the dish. Until then the cards are just linked to each other, each one pointing back at the previous card, and none of them have run.

And the reason that's even possible is because Spark isn't allowed to change the card that's already there — every transformation has to make a NEW card instead of scribbling on the old one, since RDDs are immutable. So the chain grows by adding new pointer-cards, not by mutating anything.

The narrow vs. wide thing is basically: some steps only need the ingredient sitting right in front of them (map, coalesce — one parent partition feeding one output), but others — like groupByKey or join — need to reach across the whole kitchen and grab stuff from other stations, which means ingredients have to get physically carried across the room (the shuffle). And BECAUSE Spark has the whole stack of cards laid out before cooking starts, it can look ahead and say 'okay, right here is where someone has to walk across the kitchen, so that's where I cut a new stage.' It couldn't know that in advance if it were cooking each card the instant it was written.

And the fault-tolerance thing actually clicked for me: Spark doesn't need to keep a backup copy of every finished dish sitting around — it just keeps the RECIPE (the lineage). So if a dish falls on the floor (a partition is lost), it just re-cooks that one dish from the recipe instead of needing a spare copy already made somewhere else. That's cheaper than what MapReduce did, writing everything to disk between steps just in case.

Two things are bugging me though:

*Source: [[lazy-evaluation-transformations-actions]] (vutr)*
