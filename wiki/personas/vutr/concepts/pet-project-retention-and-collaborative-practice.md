---
persona: vutr
kind: concept
sources:
- raw/weekly-newsletter-roundups-misc/groupby-36-agoda-how-we-solve-load.md
last_updated: '2026-07-15'
qc: passed
slug: pet-project-retention-and-collaborative-practice
topics:
- weekly-newsletter-roundups-misc
---

In issue #36's opening note, Vu describes a personal cycle he says repeated often enough to notice: he'd search something like "data engineering side project," pick whichever one excited him most, spend a whole weekend following the tutorial to get it running, and feel proud of the accomplishment — only to find that "two weeks later, I remember nothing. Empty head." His diagnosis is blunt: doing pet projects for the sake of getting things up and running teaches almost nothing on its own, and the natural response — abandoning that project for a new one — just restarts the same loop without building retained knowledge.

His corrective is a short list of his own practices, not a citation to anyone else's framework. Before starting, set explicit expectations for what the project is meant to teach. While building, "do things right" rather than just get them working — learn the fundamentals of Docker and Git rather than copy-pasting commands, organize and test code properly, and understand mechanics like SQL's order of execution. He also recommends doing the project with friends specifically to learn what building alongside more than one person is like, since a solo project can't teach that. For every tool touched — Spark, Airflow, Git, Docker — his suggested habit is to ask two questions: "what problem do these tools try to solve?" and "how are they gonna solve that problem?" rather than only learning the tool's surface commands. After the project runs, he suggests role-playing as the eventual consumer of the data warehouse or dashboard and honestly asking "Am I satisfied? Do I get things I need?" — grounded in his claim that a data engineer's job is, most of the time, serving that internal data-consuming user. Finally, he names applying data modeling to the project specifically, rather than skipping straight to picking tools.

This is a shorter, more personal reflection than his more fully worked-out side-project framework captured elsewhere in this wiki ([[side-project-strategy-for-job-seeking]]), which lays out a step-by-step process (start from a real problem, model before tooling, break things on purpose, document and share). The two overlap on modeling-before-tools and on treating the project as more than "getting it to run," but this issue-#36 note is the only place in Vu's captured writing where he specifically names building with collaborators as its own distinct lesson a solo project cannot teach.

*See also: [[groupby-newsletter]] · [[side-project-strategy-for-job-seeking]]*
