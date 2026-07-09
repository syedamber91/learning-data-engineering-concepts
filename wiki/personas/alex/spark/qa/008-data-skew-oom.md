---
persona: alex
kind: concept
sources:
- vutr/data-skew-oom
last_updated: '2026-07-09'
qc: passed
slug: 008-data-skew-oom
topics:
- spark
learner: alex
source_note: data-skew-oom
mastery: learning
---

*What Alex understood:* So skew is when one partition is way bigger than the others, and because that big partition goes to just one task, adding more memory doesn't help — you have to split that partition up. And that's also why the same job can randomly pass one day and fail another: it's the scheduling order, not the data size, that changed.

## Follow-up questions

**Alex:** You said adding more memory doesn't fix it because the big partition still lands on one task — so is the trick basically to make sure no single task ever gets the whole giant chunk?

**vutr:** Yes — grounded in the note: the note says the real fix is to break the skewed partition apart, precisely because the skewed partition otherwise still lands on a single task that needs more memory than you can give. So the goal is to stop one task from holding the whole giant partition.

**Alex:** When you say a different scheduling order causes pass-vs-fail, does that mean the exact same data can just get unlucky depending on the order the tasks run?

**vutr:** Yes — the note says the same job passes on Monday and fails on Thursday because of a different scheduling order, not a change in data volume. So the same data can produce a different outcome depending on the order things get scheduled.
