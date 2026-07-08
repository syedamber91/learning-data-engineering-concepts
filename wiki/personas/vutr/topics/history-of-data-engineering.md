---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: history-of-data-engineering
---

Related: [[relational-model-and-sql]] · [[data-warehouse]] · [[hadoop-mapreduce]] · [[open-table-formats]] · [[data-mesh]] · [[kimball-vs-inmon]] · [[etl-to-elt-shift]]

## Comparisons
The design debate that has shaped every [[data-warehouse]] is captured in [[kimball-vs-inmon]]: Kimball builds marts bottom-up, Inmon builds the enterprise warehouse top-down. On the storage side, [[hadoop-mapreduce]] and [[open-table-formats]] both tried to make the data lake usable, but where MapReduce forced developers to bend their logic to its paradigm (and Google itself abandoned it by 2014), the table formats brought a clean table abstraction to the lake — the same goal an earlier effort chased more than 15 years ago. Architecturally, [[data-mesh]] pushes toward decentralization while the classic [[data-warehouse]] centralizes, and the [[etl-to-elt-shift]] reflects how cheap cloud storage rewired the whole pipeline.

## Open questions
- If Google dropped MapReduce by 2014, why did so many enterprises still invest heavily in Hadoop clusters they could not fully benefit from?
- Given that [[open-table-formats]] revive an idea from more than 15 years earlier, what made the timing right for Delta Lake, Iceberg, and Hudi to succeed where the early effort did not?
- Will [[data-mesh]] prove to be a durable architectural shift, or one of the innovations that fails to add lasting value to the core goals of data engineering?
- Does the [[etl-to-elt-shift]] fully reverse once storage economics or governance pressures change again?

## Synthesis
The history runs from [[relational-model-and-sql]] and the [[data-warehouse]] through the big-data detour of [[hadoop-mapreduce]] to today's [[open-table-formats]] and [[data-mesh]]. The recurring theme is that abstractions get reinvented — the table formats chase a goal from more than 15 years earlier — while economics quietly reshape practice, as in the [[etl-to-elt-shift]] driven by cheap cloud storage. One thing I'm certain of is that change will come quickly, and only the innovations that truly add value to the core goals of data engineering will stand the test of time.
