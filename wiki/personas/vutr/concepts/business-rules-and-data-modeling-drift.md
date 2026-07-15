---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9-4c5.md
- raw/data-pipeline-design-framework-additional/my-framework-to-build-a-data-pipeline.md
last_updated: '2026-07-15'
qc: passed
slug: business-rules-and-data-modeling-drift
topics:
- data-pipeline-design-framework
---

Business rules are the filters, joins, aggregations, and enrichments that turn raw data into meaning — a user counted as "active" if they logged in within 30 days, revenue defined to exclude refunds. Vu Trinh's case for why a data model matters here is a specific drift scenario he lays out step by step: a team needs a pipeline, there's no data model upfront, so an engineer works with stakeholders, forms his own interpretation of "active user," and ships it. Two weeks later a different team builds a similar pipeline against the same source, a different engineer forms a slightly different interpretation, and now two definitions of the same concept live in two pipelines. Six months after that, nobody knows which one is right.

A data model is what prevents this: it defines a concept like "active user," "completed order," or "revenue" once, and every pipeline that follows implements that definition as a spec rather than re-deriving its own. When a well-defined model exists, the business rules are just the model's logic transplanted into processing code — a clear guideline, not a judgment call. When it doesn't exist, he doesn't treat that as a blocker: his move (stated identically in his sink-first framework) is to model only what this pipeline's output needs first, working directly with end users, and expand the model to cover other business processes incrementally later.

Data modeling earns a second, distinct payoff here beyond consistency: because business rules define what "valid" data looks like (a user can't log in twice with the same email; a signup requires a name), they are also what tells you what to check for — which is the direct handoff into [[data-quality-rules-and-anomaly-detection|data quality rule design]].

*See also: [[sink-first-requirements-gathering]] · [[data-quality-rules-and-anomaly-detection]] · [[testing-data-pipeline-correctness]]*
