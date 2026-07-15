---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9.md
last_updated: '2026-07-15'
qc: passed
slug: data-grain-and-serving-storage-shape
topics:
- data-pipeline-design-framework
---

Vu Trinh opens his serving-layer piece with a personal failure story: tasked with backing a dashboard and letting users run ad hoc SQL, he built one beautifully modeled, pre-joined "wide table" and let everyone query it — dashboards, the data science team, an internal app, a downstream pipeline. "It felt clean at first. Then it wasn't." The dashboard needed pre-aggregation because scanning the full table per filter was slow; data scientists needed a lower grain; the app needed sub-second user_id lookups that the columnar layout without indexing couldn't give; refresh needs ranged from daily (data science) to hourly (dashboard). His lesson: there is never a single serving approach that satisfies every use case, which is why identifying how the data will actually be used has to come first.

The first concrete question is how data will be stored and served — table, dashboard, CSV, API, web-app, or ML training set — because each implies different prep: a warehouse table means columnar format plus partitioning/clustering if needed; a dashboard means the real engineering is in pre-aggregation and caching; a file means deciding storage location, format, access control, and versioning; an API means you're now running a service with uptime SLAs, auth, rate limiting, and versioning.

The second is staleness tolerance, mirrored from the sink-first framework but now paired with a specific new lever: a materialized view, which refreshes on a schedule tied to source changes and suits many real-time use cases without needing a dedicated low-latency store.

The third, and the one he spends the most care on, is grain — the "raw" level of data — because "raw" means something different to each audience: event-level (every click, every transaction) to a data scientist, denormalized fact-table level to a BI analyst, latest-entity-state (one row per user) to an application backend. The asymmetry he names is the core rule: lower grain can always be aggregated up later (date+event → date), but a higher-grain table can never be broken back down to the lower grain it never captured. So lower grain is more flexible, but higher grain is more convenient and performant when users only ever need the aggregate — dashboard users tend to prefer higher grain, ad hoc and exploratory users need lower grain.

*See also: [[sink-first-requirements-gathering]] · [[physical-layout-partitioning-clustering-and-compaction]] · [[batch-vs-stream-throughput-and-latency]]*
