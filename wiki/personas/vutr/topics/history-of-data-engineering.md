---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: history-of-data-engineering
---

Related: [[relational-model]] · [[data-warehouse]] · [[hadoop-mapreduce]] · [[open-table-formats]] · [[data-mesh]] · [[kimball-vs-inmon]] · [[elt-vs-etl]]

## Comparisons
The design debate that has shaped every [[data-warehouse]] is captured in [[kimball-vs-inmon]]: Kimball builds marts bottom-up, Inmon builds the enterprise warehouse top-down. On the storage side, [[hadoop-mapreduce]] and [[open-table-formats]] both tried to make the data lake usable, but where MapReduce forced developers to bend their logic to its paradigm (and Google itself abandoned it by 2014), the table formats brought a clean table abstraction to the lake — the same goal an earlier effort chased more than 15 years ago. Architecturally, [[data-mesh]] pushes toward decentralization while the classic [[data-warehouse]] centralizes, and the [[elt-vs-etl]] reflects how cheap cloud storage rewired the whole pipeline.

## Open questions
- If Google dropped MapReduce by 2014, why did so many enterprises still invest heavily in Hadoop clusters they could not fully benefit from?
- Given that [[open-table-formats]] revive an idea from more than 15 years earlier, what made the timing right for Delta Lake, Iceberg, and Hudi to succeed where the early effort did not?
- Will [[data-mesh]] prove to be a durable architectural shift, or one of the innovations that fails to add lasting value to the core goals of data engineering?
- Does the [[elt-vs-etl]] fully reverse once storage economics or governance pressures change again?

## Synthesis
The history runs from [[relational-model]] and the [[data-warehouse]] through the big-data detour of [[hadoop-mapreduce]] to today's [[open-table-formats]] and [[data-mesh]]. The recurring theme is that abstractions get reinvented — the table formats chase a goal from more than 15 years earlier — while economics quietly reshape practice, as in the [[elt-vs-etl]] driven by cheap cloud storage. One thing I'm certain of is that change will come quickly, and only the innovations that truly add value to the core goals of data engineering will stand the test of time.

## Related topics
- [[amazon-s3-gfs-hdfs-and-distributed-file-systems]] — Hadoop/HDFS was the big-data detour in the history of the field before object storage displaced it as the data-lake backbone.
- [[data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa]] — The warehouse, data mesh, and ELT-vs-ETL shift are the throughline of the field's history from relational model to open table formats.
- [[data-engineering-career-roadmap-and-learning-philosophy]] — The learning philosophy of anchoring on fundamentals that outlast tools is grounded in the field's history of reinvented abstractions.
- [[iceberg]] — Open table formats like Iceberg are the present-day chapter of the history, reviving a clean-table-abstraction goal from 15+ years earlier.
- [[sql-fundamentals-and-execution-model]] — The relational model is the historical root shared by both notes, the foundation everything since has built on.
- [[spark]] — Spark was built at AMPLab to spare iterative ML the disk-write penalty of MapReduce, the big-data era the history note traces.
