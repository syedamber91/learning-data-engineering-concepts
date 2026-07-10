---
persona: alex
kind: concept
sources:
- vutr/resource-allocation-and-scheduling-modes
last_updated: '2026-07-10'
qc: passed
slug: resource-allocation-and-scheduling-modes
topics:
- spark
learner: alex
source_note: resource-allocation-and-scheduling-modes
mastery: mastered
---

Wait, so I had this backwards in my head — I thought "Spark asks for more workers" and "Spark shares workers between jobs" were the same knob. They're not. It's like a company: resource allocation is HR deciding how many employees the whole company gets to hire, and scheduling mode is the office manager deciding which project those employees work on this week.

For hiring: static allocation is like signing a fixed headcount contract up front — you pay for say 20 people whether they're busy or twiddling their thumbs. Dynamic allocation is more like a staffing agency: if work piles up and stays piled up for a while (the backlog timeout), you call for more people, and you don't ask for 20 at once — you ask for 1, then 2, then 4, then 8, doubling each time you're still stuck, so you don't overhire for something that turns out to be a small job. And letting people go is dumber and faster — anyone sitting idle past a certain point just gets cut loose.

But cutting someone loose is risky if they were holding onto work nobody else has — like shuffle data. That's why there's this external shuffle service — it's like a shared filing cabinet all executors can pull from, so even after the person who filed something is gone, the file is still there. Cache doesn't get that filing cabinet automatically though — if you fire that executor, whatever it had cached is just gone, unless you specifically told Spark "don't touch this one."

Then scheduling mode is a totally separate question — once you HAVE your employees, does the first project hog everyone (FIFO), or does everyone get rotated across projects fairly (Fair), with pools acting like guaranteed minimum staff per department (minShare) plus weighted extra help on top.

*Source: [[resource-allocation-and-scheduling-modes]] (vutr)*
