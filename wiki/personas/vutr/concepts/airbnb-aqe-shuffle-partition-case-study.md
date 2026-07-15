---
persona: vutr
kind: concept
sources:
- raw/spark/i-spent-6-hours-to-learn-how-apache.md
last_updated: '2026-07-15'
qc: passed
slug: airbnb-aqe-shuffle-partition-case-study
topics:
- spark
---

[[adaptive-query-execution|AQE's]] dynamically-coalescing-shuffle-partitions feature is usually explained in the abstract — start with a large partition count, let AQE combine small adjacent ones once real post-shuffle sizes are known. Airbnb's 2022 ingestion migration is the concrete production case where that abstraction was the actual fix for an actual outage-adjacent problem, not just a performance tweak.

The setup: Airbnb's Hive-based data ingestion framework processes over 35 billion Kafka messages and 1,000+ tables daily, with per-table datasets ranging from kilobytes to terabytes across hourly and daily partitions. When Airbnb moved this framework's Hive queries onto Spark, they hit a mismatch Hive itself didn't have: Spark requires a single, fixed shuffle-partition count set ahead of time (`spark.sql.shuffle.partitions`), and no single fixed number could be right for both a kilobyte-scale table and a terabyte-scale table in the same ingestion framework — too large for the small event streams, too small for the large ones, with no per-job override that scaled with the framework's own volume variance.

AQE's dynamically-coalescing-shuffle-partitions feature is what Airbnb used to close that gap in production, and specifically that feature alone — the case study doesn't invoke AQE's other two features (skew-join splitting or join-strategy switching) as part of the fix. The mechanic, as applied here: start with a shuffle partition count sized for the largest tables the framework will ever see, and let AQE combine small adjacent partitions at runtime once it has observed each job's actual post-shuffle data volume — so the same fixed upstream partition count that would otherwise be wildly oversized for a small hourly event stream gets coalesced down automatically, rather than needing a bespoke per-table partition count tuned by hand. Airbnb reports this produced a significant performance boost precisely because the coalescing continuously adapts to shuffle data size as it grows or shrinks between stages, rather than committing to one partition count for the framework's entire, highly heterogeneous table population.

The broader point the case study makes concrete: AQE's value isn't confined to query plans written by a single analyst tuning a single job. It solves a *framework*-level problem — one ingestion pipeline serving thousands of tables at wildly different scales — precisely because it removes the need for a human to pick the right static partition count per table in advance.

*See also: [[adaptive-query-execution]] · [[jobs-stages-tasks-dag-and-dependencies]] · [[airbnb-infrastructure-philosophy]]*
