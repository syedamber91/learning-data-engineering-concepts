---
persona: alex
kind: concept
sources:
- vutr/adaptive-query-execution
last_updated: '2026-07-09'
qc: passed
slug: 005-adaptive-query-execution
topics:
- spark
learner: alex
source_note: adaptive-query-execution
mastery: learning
---

*What Alex understood:* So basically AQE (new in Spark 3.0) lets Spark rewrite its own plan mid-query. It can merge shuffle partitions, swap which join method it uses, and deal with lopsided skew joins. And it can only do this because a shuffle or broadcast creates a pause point (a query stage boundary), and that pause is where Spark checks the real data stats and fixes its plan.

## Follow-up questions

**Alex:** Why does Spark need that pause at the shuffle or broadcast to re-optimize, instead of just fixing the plan whenever it wants?

**vutr:** On my first question: the note says the shuffle or broadcast exchange creates a query stage boundary, and 'that pause is exactly what gives Spark the chance to re-optimize with real statistics.' So the pause is required because it's the point where real statistics become available, and only with real numbers (not up-front guesses) can Spark safely change the plan. The note doesn't explain any deeper mechanism than that.

**Alex:** When you say it 'switches join strategies on the fly,' does the note tell us what it switches from and to?

**vutr:** On my second question: honestly, the note only says AQE 'switches join strategies on the fly' but it does NOT name which strategies it switches between. So I can't answer that from this note alone.
