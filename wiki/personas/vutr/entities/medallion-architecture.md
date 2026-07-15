---
persona: vutr
kind: entity
sources:
- raw/lakehouse-architecture-and-practical-builds/data-architecture-101.md
last_updated: '2026-07-15'
qc: passed
slug: medallion-architecture
topics:
- dbt
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

Medallion is Databricks' term for organizing a lakehouse's data into three layers — bronze (raw data), silver (cleaned and standardized data), and gold (business-support data) — to control data quality, apply governance, and provide reproducibility. Vu is careful to note the idea itself is not exclusive to Databricks or new: it has long existed under other names, most commonly Landing/Curated/Serving (which is exactly the three-schema layout — landing, staging, curated — he uses in his own laptop lakehouse build; see [[trino]]).

He classifies Medallion as a pattern rather than an architecture — see [[architecture-vs-pattern]] — using his own working distinction: an architecture is the high-level blueprint of how data is ingested, stored, processed, and served, while a pattern is a reusable solution to one specific problem inside that architecture. Medallion, in this framing, is a pattern for organizing storage, not the blueprint itself. He adds a second, sharper distinction: Medallion is not data modeling either — arranging tables into bronze/silver/gold tiers says nothing about how the data within those tiers is structured or related; that question is answered separately by a modeling approach such as Kimball, Inmon, or Data Vault, chosen based on business needs regardless of which architecture or pattern is in play.

*See also: [[star-schema]] · [[grain-declaration]] · [[surrogate-keys]] · [[dbt]] · [[scd-type-2]] · [[scd-type-1-and-3]] · [[architecture-vs-pattern]]*
