---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9.md
last_updated: '2026-07-15'
qc: passed
slug: stale-or-incorrect-data-handling
topics:
- data-pipeline-design-framework
---

Vu Trinh's framing for this problem is deliberately blunt: "bad things will happen. The question isn't whether your serving layer will ever serve bad data. The question is whether it's honest about it, or whether your users find out before you do." The design questions that follow from that: can consumers tolerate stale data during a failure, or is stale data actually worse than no data at all; if an upstream correction changes a number from a week ago, does the serving layer need to reflect that correction; and how will consumers even know whether what they're looking at right now is fresh or stale, correct or corrupted?

His trust-building responses split into two moves. The first is confirming explicitly at the serving layer — alerting on what consumers actually experience, and optionally formalizing it as a data contract that states what producers guarantee (schema, freshness, completeness), which functions as a visible "this data is good to go" signal. Where an issue can't be caught before a user notices it, his fallback is to communicate the problem explicitly and broadly rather than fix it silently, and to feed the root cause back into prevention (typically new [[data-quality-rules-and-anomaly-detection|data quality rules]]).

The second move is specific to [[backfilling-data-pipelines|backfills]]: because a backfill can touch a wide range of historical data, the before-and-after can look dramatically different, and end users can be genuinely alarmed if a dashboard looks unrecognizable compared to two hours earlier. His pattern for avoiding that shock: write the backfilled result to a separate table, run validation checks against it, notify users that a backfill is coming, and only then rename the backfill table into the position of the main table — so the switch is deliberate and communicated rather than a silent swap.

*See also: [[data-quality-rules-and-anomaly-detection]] · [[backfilling-data-pipelines]] · [[safe-writes-and-schema-evolution-in-serving]]*
