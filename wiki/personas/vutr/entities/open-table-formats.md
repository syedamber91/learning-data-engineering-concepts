---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: open-table-formats
topics:
- history-of-data-engineering
- iceberg
---

The modern table-format wave brought the table abstraction to the data lake: Apache Hive arrived from Meta in 2009, Databricks open-sourced Delta Lake in 2016, Uber ran Hudi on HDFS in production from 2016, and Netflix began developing Iceberg in 2017 — echoing, as I like to remind people, an early effort more than 15 years ago to achieve the same thing these three formats are now chasing. What makes these formats 'open' is that the metadata layer is separate and has no database dependence — that is why 'open' comes before 'table formats.' The metadata lives with the data on object storage rather than inside a proprietary database.
