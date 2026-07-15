---
persona: vutr
kind: concept
sources:
- raw/data-engineering-career-roadmap-and-learning-philosophy-additional/9-lessons-that-will-put-you-3-years.md
- raw/data-engineering-career-roadmap-and-learning-philosophy-additional/how-to-become-a-senior-data-engineer.md
last_updated: '2026-07-15'
qc: passed
slug: simplicity-over-complexity-in-pipeline-design
topics:
- data-engineering-career-roadmap-and-learning-philosophy
---

Vu tells the identical cautionary anecdote in both "9 lessons that will put you 3 years ahead" and "How to become a senior data engineer?", down to the same numbers, which signals it's a deliberately reused teaching example rather than incidental repetition. He was asked to build a pipeline delivering daily dashboard insights and instead built a full CDC-based real-time system — a pipeline continuously monitoring PostgreSQL changes, routing them through Kafka brokers (or, in the senior-focused retelling, Debezium into Pub/Sub) into BigQuery, with Dataflow handling processing. His own diagnosis of why: "That was just because I had just read a book about real-time processing and dreamt of building such a system" — not because the requirement demanded it.

The result, stated the same way in both pieces: the team now had to operate and understand Debezium/Kafka or Pub/Sub, plus Dataflow, plus BigQuery, plus a pile of Python glue code — and the Dataflow bill was high precisely because the team lacked experience tuning it. Since the actual requirement was only a daily refresh, "we could have used a simple batch pipeline orchestrated by Airflow to dump data from the PostgreSQL database and load it into BigQuery," with the CDC pipeline's performance concern addressed just as well by running the export against a read replica. The lesson he draws is not "never use real-time architecture," but that architectural sophistication must be earned by an actual requirement, not by what's exciting to build or what a book made him want to try.

He's careful to note that simplicity is a skill, not a shortcut: "that's harder than it sounds. Choosing the right tools, along with providing well-designed abstractions to make the code cleaner, requires a lot of time to get right," and in the senior-focused version he adds that it sometimes comes down to "gut feeling" built from experience rather than a formula. The payoff he claims is durable: simplicity "gives you a better chance of creating scalable, understandable, and maintainable solutions" — the same three qualities [[nine-software-engineering-skills-for-des]] ties to writing understandable code and environment separation. In the senior-focused piece, simplifying sits alongside trade-off thinking and reversible decisions as one lens on the same underlying discipline: choose a solution because it solves the actual problem, not because it's the most technically interesting option available (see [[senior-data-engineer-mindset-shifts]]).

*See also: [[senior-data-engineer-mindset-shifts]] · [[nine-software-engineering-skills-for-des]] · [[data-modeling-as-organizational-blueprint]]*
