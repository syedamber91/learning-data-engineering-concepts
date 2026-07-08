---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: lakehouse
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

Databricks coined 'lakehouse' in a 2020 paper: a data management system built on low-cost storage that adds traditional analytical DBMS features like ACID transactions, versioning, caching, and query optimization. Technically BigQuery and Snowflake are lakehouse implementations, but they run against the spirit of the manifesto because you don't control your own storage layer.
