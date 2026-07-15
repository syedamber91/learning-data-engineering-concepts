---
persona: vutr
kind: concept
sources:
- raw/snowflake-internals/i-spent-8-hours-diving-deep-into.md
- raw/snowflake-internals/i-spent-another-6-hours-understanding.md
last_updated: '2026-07-15'
qc: passed
slug: cascades-optimizer-and-runtime-adaptivity
topics:
- snowflake-internals
---

Every user query in Snowflake passes through the Cloud Services layer first, where it's parsed, resolved against catalog objects, checked against access control, and optimized before any compute is touched. The optimizer itself follows a Cascades-style approach — top-down, cost-based — and the statistics that cost-based optimization needs are maintained automatically as data loads and updates happen, not computed on demand. Snowflake keeps these at two granularities: table-level (row count, size in bytes) and column-level (min/max, null count, distinct count) — the same min/max values that also drive pruning (see [[min-max-pruning-and-dynamic-data-skipping]]).

What the posts single out as distinctive is that this optimization doesn't stop once a plan is chosen: Snowflake supports runtime adaptivity, meaning the system can revise its execution decisions *during* a running query based on conditions observed as data is actually processed — changing a join strategy or adjusting resource allocation mid-flight rather than committing irrevocably to whatever the pre-execution, static Catalyst-style plan predicted. The posts frame this as a deliberate departure from traditional static optimization, which locks in its choices before execution starts and has no way to react if its cost estimates turn out to be wrong once real data volumes and skew show up. The dynamic min-max pruning described in [[min-max-pruning-and-dynamic-data-skipping]] — pushing build-side join-key statistics to the probe side mid-query — is itself one concrete manifestation of runtime adaptivity, not a separate mechanism.

Throughout query execution, the Cloud Services layer keeps monitoring: it collects performance metrics, detects failed nodes, and persists query state and statistics for later audit and analysis, which is also what lets users inspect the history and progress of past and ongoing queries through Snowflake's UI. The posts note, without elaborating further, that other systems — Google BigQuery and Databricks among them — also employ this kind of runtime adaptivity; the mechanism's value is framed as mattering most under unpredictable data volumes or query patterns, where a plan chosen once, in advance, is most likely to be wrong by the time it actually runs.

*See also: [[min-max-pruning-and-dynamic-data-skipping]] · [[snapshot-isolation-and-immutable-file-versioning]] · [[snowflake]] · [[adaptive-query-execution]]*
