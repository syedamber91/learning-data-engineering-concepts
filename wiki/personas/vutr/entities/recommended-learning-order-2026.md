---
persona: vutr
kind: entity
sources:
- raw/data-engineering-career-roadmap-and-learning-philosophy-additional/the-data-engineer-roadmap.md
- raw/data-engineering-career-roadmap-and-learning-philosophy-additional/6-technical-skills-every-data-engineer.md
- raw/data-engineering-career-roadmap-and-learning-philosophy-additional/the-best-way-to-do-a-data-engineering.md
last_updated: '2026-07-15'
qc: passed
slug: recommended-learning-order-2026
topics:
- data-engineering-career-roadmap-and-learning-philosophy
---

"The Data Engineer Roadmap" gives Vu's fullest ordered curriculum, explicitly stated as sequence, not a bag of equally-weighted skills: **Data Modeling → SQL → Python → OLAP systems (cloud data warehouses, DuckDB, open table formats) → dbt → data formats (CSV/JSON/Avro/Parquet on disk, Arrow in-memory) → processing engines (Spark, then Polars for medium data) → data orchestration (Airflow) → software engineering (Git, CI/CD, testing, Docker, Kubernetes optional) → message systems (Kafka) → stream processing (Flink) → AI-related (LLMs, agents, vector databases, and how to direct AI rather than be replaced by it)**. His companion piece, "6 technical skills every data engineer should have," narrows to a tighter six — data modeling, Git, SQL, Python, OLAP systems, orchestration — as the load-bearing subset if time is scarce.

Two placement decisions are deliberate rather than incidental. First, data modeling leads every list: "If I read a data engineering roadmap online and it doesn't include learning data modeling as one of the first steps, I will skip it right away." Second, AI is placed explicitly last, with a stated rationale that inverts a common current: "someone might say I'm conservative when putting AI last, but I always believe in the 'know what you're doing before letting AI do it.'" This is a direct, sourced correction of an earlier vault snapshot's claim that "Cloud should be one of the last things you learn" — the roadmap actually places cloud data warehouses (Snowflake, Databricks, BigQuery trials) as an early sub-step *within* the OLAP-systems stage (the third item in the order), not deferred to the end; only AI is explicitly deferred. See the topic note's Open questions for what remains unresolved about this correction.

Notably, Kafka and Flink sit near the *end* of the order, after software engineering — Vu's reasoning is that a data engineer will "deal with batch processing 90% of the time," with Spark Structured Streaming covering 60–70% of the streaming remainder, so message systems and true stream processing are treated as a widening of scope rather than a foundational step. He also explicitly separates the roadmap from non-technical growth factors ("problem-solving, communication, and a user-oriented mindset are other key factors, but I won't mention them here to keep the article concise") — see [[senior-data-engineer-mindset-shifts]] for that side of his advice.

*See also: [[data-modeling-as-organizational-blueprint]] · [[fundamentals-over-tools]] · [[nine-software-engineering-skills-for-des]] · [[git-mental-model-for-data-engineers]] · [[ai-decision-vs-implementation-split]]*
