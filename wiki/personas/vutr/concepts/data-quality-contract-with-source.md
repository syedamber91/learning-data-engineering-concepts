---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/data-engineering-system-design-11.md
last_updated: '2026-07-15'
qc: passed
slug: data-quality-contract-with-source
topics:
- change-data-capture-cdc-and-data-sourcing
---

Vu's warning here is that a pipeline can run technically correctly — every task succeeds — and still produce the wrong output, because if the source sends bad data, the pipeline just delivers bad data downstream faster. The diagnostic questions he asks: are there known bad records the source team already knows about but hasn't fixed? Are fields that are supposed to be non-null actually nullable in practice? Are there late records — ones that belong to last week's update but only arrive today?

His responses map one-to-one onto those questions: add validation at ingestion that checks null rates, value distributions, and record counts against expectations; build alerts for when incoming data looks meaningfully different from historical runs; and, where possible, turn the informal understanding into an actual contract between you and the source team. This is deliberately softer and less structural than [[schema-change-severity-and-detection]] — a schema change is a structural break a query can fail on, while a data quality problem is a silent semantic one that technically valid rows can still carry.

*See also: [[schema-change-severity-and-detection]] · [[exactly-once-and-missing-data-detection]] · [[source-access-trust-boundary]]*
