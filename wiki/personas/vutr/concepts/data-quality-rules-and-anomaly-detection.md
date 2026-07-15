---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9-4c5.md
- raw/data-pipeline-design-framework-additional/my-framework-to-build-a-data-pipeline.md
last_updated: '2026-07-15'
qc: passed
slug: data-quality-rules-and-anomaly-detection
topics:
- data-pipeline-design-framework
---

Vu Trinh starts data quality from data modeling and input profiling, which together surface "binary constraints" — checks with a clean pass/fail answer: a column shouldn't be null, values should be unique, a count shouldn't exceed a threshold, a column should be a given type, data should arrive by a given time. These are captured with a rule system — dbt test, Great Expectations, or custom SQL — and his useful-checks list is concrete: record counts in vs. out, null rates on fields that should be populated, duplicate checks on keys that should be unique, distribution checks on critical fields (a sudden shift is worth investigating), and referential integrity (a high non-match rate on a join key often signals a logic error or a source problem, not just messy data).

The limitation he calls out explicitly is that fixed-threshold rules miss slow drift: a 5% null-rate threshold doesn't catch a field quietly drifting from 0.1% to 4.9% over three months, and a simple row-count check can't see a weird trend forming in the data. That gap is what anomaly detection is for — instead of checking against a fixed rule, you analyze historical patterns with time-series techniques (a moving average, for instance) to detect the shape of a drift or drop, and for harder detection patterns he notes this sometimes needs a machine-learning model built in collaboration with the data science team.

He draws one more explicit boundary: data quality checks are runtime concerns that catch bad data as it occurs, which is a different job from [[testing-data-pipeline-correctness|testing]] — catching logic or syntax errors in the transformation code itself before it ever touches production data.

*See also: [[business-rules-and-data-modeling-drift]] · [[dead-letter-queue-and-bad-data-isolation]] · [[processing-layer-observability]] · [[testing-data-pipeline-correctness]]*
