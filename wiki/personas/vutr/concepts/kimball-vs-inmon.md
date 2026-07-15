---
persona: vutr
kind: concept
sources:
- raw/history-of-data-engineering-and-hadoop-ecosystem/the-history-of-data-engineering.md
last_updated: '2026-07-15'
qc: passed
slug: kimball-vs-inmon
topics:
- history-of-data-engineering
---

Bill Inmon worked as a data professional from the late 1970s into the 1980s and, in the late 1980s, developed the notion of the data warehouse, describing it as "a subject-oriented, integrated, nonvolatile, and time-variant collection of data in support of management's decisions." He was also involved in the origin of ETL: in the early days, data was manually moved into the warehouse by writing programs to access a source, find the required data, transform it, and load it — work Inmon found so time-consuming and repetitive that he and his colleagues concluded automated tooling was needed, which is what the automated ETL tools of the late 1980s and 1990s (Informatica, IBM DataStage, later Cognos and Microsoft SSIS) went on to provide.

The 1990s then produced the two named, competing philosophies for building the warehouse itself. In 1991, Inmon founded Prism Solutions and introduced Prism Warehouse Manager, software for developing a data warehouse; in 1992 he codified his approach in the book *Building the Data Warehouse*, popularizing best practices for building enterprise data warehouses. Inmon's design is top-down: build a centralized enterprise data warehouse first, and let it serve as the single source of truth. In 1996, Ralph Kimball published *The Data Warehouse Toolkit*, setting the foundations of dimensional modeling. Kimball's design is bottom-up: build data marts for specific business processes first, and integrate them into a more comprehensive warehouse later.

This same decade, as attention turned to the analytics workload running on databases still designed primarily for transactions (row-stored, inefficient when a query only needs a subset of columns), people began building Data Cubes: pre-computed aggregations specified and refreshed on a schedule, so an analytics query could hit the cube instead of scanning raw data. The cube approach and the Kimball/Inmon design debate both belong to the same 1990s push to make the warehouse serve analytics workloads it wasn't originally built for.

*See also: [[hadoop-mapreduce]] · [[apache-hive]]*

## Related in the other wiki
- [[Stars and Snowflakes - Schemas for Analytics]] — DDIA's account of the fact-table-plus-dimension-tables shape nearly all warehouses converge on is the schema-level mechanics behind Kimball's bottom-up, dimensional-modeling side of this debate.
- [[Data Warehousing]] — DDIA's chapter frames the warehouse as a separate system for OLAP workloads distinct from OLTP databases, the same separation-of-concerns motivation this note traces back to Inmon's original definition.
