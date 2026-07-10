---
persona: alex
kind: concept
sources:
- vutr/resource-allocation-and-scheduling-modes
last_updated: '2026-07-10'
qc: passed
slug: 015-resource-allocation-and-scheduling-modes
topics:
- spark
learner: alex
source_note: resource-allocation-and-scheduling-modes
mastery: mastered
---

*What Alex understood:* Wait, so I had this backwards in my head — I thought "Spark asks for more workers" and "Spark shares workers between jobs" were the same knob. They're not. It's like a company: resource allocation is HR deciding how many employees the whole company gets to hire, and scheduling mode is the office manager deciding which project those employees work on this week.

For hiring: static allocation is like signing a fixed headcount contract up front — you pay for say 20 people whether they're busy or twiddling their thumbs. Dynamic allocation is more like a staffing agency: if work piles up and stays piled up for a while (the backlog timeout), you call for more people, and you don't ask for 20 at once — you ask for 1, then 2, then 4, then 8, doubling each time you're still stuck, so you don't overhire for something that turns out to be a small job. And letting people go is dumber and faster — anyone sitting idle past a certain point just gets cut loose.

But cutting someone loose is risky if they were holding onto work nobody else has — like shuffle data. That's why there's this external shuffle service — it's like a shared filing cabinet all executors can pull from, so even after the person who filed something is gone, the file is still there. Cache doesn't get that filing cabinet automatically though — if you fire that executor, whatever it had cached is just gone, unless you specifically told Spark "don't touch this one."

Then scheduling mode is a totally separate question — once you HAVE your employees, does the first project hog everyone (FIFO), or does everyone get rotated across projects fairly (Fair), with pools acting like guaranteed minimum staff per department (minShare) plus weighted extra help on top.

## Follow-up questions

**Alex:** If a Fair-scheduling pool has a minShare that's supposed to guarantee it a floor of resources, but dynamic allocation's remove policy just cuts any executor that's been idle past the timeout — does removal check whether killing that executor would break some pool's minShare guarantee, or could a quiet pool's guaranteed floor get scaled away just because nothing's running on it that exact moment?

**vutr:** By default, nothing built into the remove policy protects cached data — the note is explicit that cache "doesn't get the same protection by default" and disappears when its executor is removed. The only fix the note gives is manual: you configure cache-holding executors to never be removed, opting them out of the idle-timeout removal entirely. So your instinct is right — without that explicit configuration, dynamic allocation's plain idle-based removal would eventually cut a cache-holding executor just like any other idle one.

**Alex:** You said cache doesn't get the external-shuffle-service protection, so removing a cache-holding executor loses the cache — but doesn't dynamic allocation's own remove policy (kill anything idle) basically guarantee that'll happen eventually unless you do something about it? What's actually stopping it by default?

**vutr:** (the wiki does not cover this — see open questions)
