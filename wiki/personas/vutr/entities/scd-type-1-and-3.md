---
persona: vutr
kind: entity
sources:
- raw/dbt-and-dimensional-modeling/i-spent-6-hours-learning-about-slowly.md
last_updated: '2026-07-15'
qc: passed
slug: scd-type-1-and-3
topics:
- dbt
---

Vu also mentions **SCD Type 0** in passing: dimension records simply aren't allowed to change at all. He says there's not much to discuss about it and gives it no further treatment.

**Type 1 (overwriting)** detects the changed row and overwrites it with the new value, so consumers always see only the latest state — useful when history genuinely doesn't matter, but with an unavoidable downside: history is destroyed. His worked example: a user who lived in Vietnam in July and moved to Singapore in August will, under Type 1, have their country column overwritten to Singapore — the Vietnam purchase's context disappears, and a breakdown of total sales by country changes retroactively, because the user's July purchase no longer shows as a Vietnam sale.

**Type 3 (adding new columns)** exists because Type 2 has a real limitation: a fact row can only reference one version of a dimension record at a time. Type 3 instead adds one or more extra columns to the dimension row itself, each holding a prior value, so that a single row can represent both the current and a past state simultaneously without a schema-level version split — a property Vu calls, only half-jokingly, its "alternate realities" trick: when joining to the dimension, a fact row can pick which version to observe just by selecting a different column rather than needing a different foreign key. In practice one extra column is usually enough to hold the immediately-prior value.

Vu's own assessment of Type 3 is skeptical bordering on stuck: he confesses he struggles to think of a real use case, since its whole value proposition is letting a fact row see two different real-world moments simultaneously — and his intuition is that two events happening in different contexts at different times should usually be observed within their own respective contexts, not blended. He searched for examples online and found other people just as unsure. Kimball himself, per Vu's citation, states Type 3 is infrequently used, needed only when a fact row genuinely must be observed under two versions of a dimension at once. Vu also passes along a piece of internet folklore he finds plausible but can't verify: that Type 3 originated when SQL engines didn't yet support window functions, and that its whole effect can now be reproduced by running a `LAG` window function (partitioned by the dimension's key, ordered by `start_date`) over an ordinary Type 2 table — meaning modern SQL may have made Type 3 largely redundant. Storage cost, the other historical argument for Type 3 over Type 2, he considers negligible now that disk is cheap.

*See also: [[star-schema]] · [[grain-declaration]] · [[surrogate-keys]] · [[dbt]] · [[scd-type-2]] · [[dbt-origin-and-adoption]] · [[scd-type-4-mini-dimension]] · [[scd-hybrid-types-5-6-7]]*

## Open questions
- Vu could not find (and could not himself construct) a convincing real-world case for SCD Type 3 beyond the theoretical "observe two dimension versions simultaneously" scenario — whether one genuinely exists in production systems is left open.
