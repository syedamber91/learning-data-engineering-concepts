---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9-4c5.md
last_updated: '2026-07-15'
qc: passed
slug: testing-data-pipeline-correctness
topics:
- data-pipeline-design-framework
---

Transformation logic is code, and Vu Trinh's position is that it should be tested like code — catching logic and syntax errors before they ever run against real data, which he distinguishes sharply from [[data-quality-rules-and-anomaly-detection|data quality checks]] (a runtime concern that flags bad data as it occurs). Testing is what gives confidence the logic is "safe" to apply in the first place.

He names three levels. Unit tests exercise critical transformation functions in isolation, against test datasets built to mimic production, and should test business-rule logic explicitly — if "active user" means logged in within 30 days, the test should verify that a user who logged in 31 days ago is excluded. Integration tests run the full transformation chain end-to-end against a representative sample of real data, because unit tests only verify individual pieces of logic, not how they compose. Regression tests run a changed version of the logic against a fixed historical dataset and compare its output to the previous version — any unexpected difference is a warning sign. He flags this last one as especially important during backfills specifically: the goal there isn't zero difference, it's confirming the new logic produces *meaningfully different* results exactly where it's supposed to, which ties testing directly into whether a [[backfilling-data-pipelines|backfill]] can be trusted.

*See also: [[data-quality-rules-and-anomaly-detection]] · [[backfilling-data-pipelines]] · [[business-rules-and-data-modeling-drift]]*
