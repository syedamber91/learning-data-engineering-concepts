---
persona: alex
kind: concept
sources:
- vutr/photon
last_updated: '2026-07-09'
qc: passed
slug: photon
topics:
- spark
learner: alex
source_note: photon
mastery: learning
---

So Photon is a fast C++ engine bolted onto Databricks that reads data column-by-column and chews through it in batches instead of one row at a time — same batch idea as BigQuery and Snowflake. And the team chose the simpler 'interpreted/vectorized' way over auto-generating code because it was quicker to build and easier to debug, and the cost of jumping between Java and C++ turned out to be almost zero (0.06%).

*Source: [[photon]] (vutr)*
