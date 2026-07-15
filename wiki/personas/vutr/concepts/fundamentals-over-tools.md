---
persona: vutr
kind: concept
sources:
- raw/data-engineering-career-roadmap-and-learning-philosophy-additional/4-things-to-keep-in-mind-as-i-begin.md
- raw/data-engineering-career-roadmap-and-learning-philosophy-additional/6-technical-skills-every-data-engineer.md
- raw/data-engineering-career-roadmap-and-learning-philosophy-additional/9-lessons-that-will-put-you-3-years.md
- raw/data-engineering-career-roadmap-and-learning-philosophy-additional/how-to-become-a-senior-data-engineer.md
- raw/data-engineering-career-roadmap-and-learning-philosophy-additional/the-data-engineer-roadmap.md
last_updated: '2026-07-15'
qc: passed
slug: fundamentals-over-tools
topics:
- data-engineering-career-roadmap-and-learning-philosophy
---

This is Vu's most-repeated argument across the whole batch, restated in nearly every article with the same self-critical origin story: in his first year, FOMO from job descriptions demanding tools A/B/C/D drove him to spin up "many Docker containers to get Kafka, Spark, Airflow, HDFS, Trino, MinIO... up and running." It was fun, but shallow — he knew Kafka "absorbs data streams," Spark "keeps data in memory," Airflow "lets you write DAGs," and nothing more. He still failed interviews. His conclusion, stated identically in "9 lessons" and "How to become a senior data engineer?": "learning tools is not wrong, but learning only tools is wrong, because tools can become obsolete and be replaced" — especially now, in the AI era, when everything moves faster than ever.

The counter-move is anchoring on fundamentals he states will not change, and the *same* worked list recurs, word for word, in "9 lessons" and "How to become a senior data engineer?": data will always be processed by splitting it across multiple machines; compute and storage decoupling in cloud warehouses is here to stay; columnar format always outperforms row format for analytical-heavy reads; and (added in the senior-focused piece) Spark's DataFrame/Dataset abstractions will always compile down to RDD. "4 Things To Keep In Mind" frames the same instinct as a three-part practice rather than a list of facts: (1) ask "what problems does this [tool] solve?" repeatedly until you hit the fundamental need — his worked example traces Spark back through MapReduce's clunky API, MapReduce's disk-bound slowness, and the need for fault tolerance via lineage; (2) don't just read theory, validate it incrementally with hands-on practice; (3) notice *shared* fundamentals across tools — once you know Snowflake separates compute and storage, you already understand a load-bearing fact about Databricks and BigQuery too.

The payoff, spelled out consistently: you can "scale" your learning across vendors instead of learning each tool from zero; you pick up a new tool faster because only the vendor-specific differences are new; you can spot marketing claims for what they are (every vendor claims to have invented the "fastest columnar OLAP database," but the columnar-format fundamental was never proprietary); and you build better abstractions in your own head — Snowflake/BigQuery/Databricks/Trino collapse into "OLAP systems," Airflow/Dagster into "orchestrators," Kafka/PubSub/Kinesis into "message systems" — becoming tool-agnostic rather than seeing fifty unrelated products. "6 technical skills every data engineer should have" opens on the same premise ("the most effective approach to learning in this era is to learn things that would not change") before walking through data modeling, Git, SQL, Python, OLAP, and orchestration as instances of exactly that kind of durable skill (see [[recommended-learning-order-2026]]). "The Data Engineer Roadmap" applies the same reasoning to justify deferring AI to the very end of its learning order: know the fundamentals well enough to audit AI's output before delegating to it (see [[ai-decision-vs-implementation-split]]).

*See also: [[recommended-learning-order-2026]] · [[senior-data-engineer-mindset-shifts]] · [[data-modeling-as-organizational-blueprint]] · [[feedback-loop-driven-learning]]*
