---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/data-engineering-system-design-11.md
last_updated: '2026-07-15'
qc: passed
slug: source-performance-impact-by-type
topics:
- change-data-capture-cdc-and-data-sourcing
---

Vu frames "how will the source's performance be impacted?" as a question about being a good consumer — not crashing the thing you depend on — and the impact he describes is specific to each source type. For databases, the risk is query pressure: full-table scans can spike CPU or lock rows on a production system, so the fix is a read replica the pipeline hits instead of the master. He explicitly ranks CDC via logical replication as gentler than periodic bulk exports here, because it rides the replication log rather than querying live data, though it requires more setup. For APIs, the concern is rate limiting: implement exponential backoff and retry logic, prefer bulk endpoints over one-record-at-a-time calls, and watch for concurrency — his example is an Airflow backfill running hundreds of DAGs at once, which can blow through an API's rate limit far faster than a single steady stream of calls would. For files in object storage, the source itself is rarely the bottleneck, but frequent bucket listing or unnecessary GET requests can quietly inflate your bill. For streams like Kafka, the danger is a slow consumer falling behind the producer — consumer lag — to the point where the broker either has to retain more data than its retention policy allows, or the consumer falls behind so far it misses data outright; the fix is monitoring lag and sizing consumers to keep up.

The unifying principle across all four: the source team should never see your pipeline show up as an anomaly on their own monitoring dashboard.

*See also: [[pull-vs-push-source-types]] · [[log-based-cdc]] · [[source-retention-and-replayability]]*
