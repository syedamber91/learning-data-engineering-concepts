---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/data-engineering-system-design-11.md
last_updated: '2026-07-15'
qc: passed
slug: source-availability-and-sla
topics:
- change-data-capture-cdc-and-data-sourcing
---

Vu's closing sourcing question is deliberately anticlimactic: you've answered every question above, written a normal healthy call with the right parameters, hit no rate limit — and still get a "service unavailable" error. Availability of the source's infrastructure is a separate concern from the quality of its data, and it comes down to two questions: what is the source's uptime guarantee (a documented 99.9% SLA sounds reassuring, but what matters more is whether the source actually meets it, and what happens when it doesn't), and how long can your pipeline actually wait? A 2-hour outage is a non-event for a pipeline that runs daily, but a serious incident for one that runs every 30 minutes and feeds a real-time dashboard.

His standard response pattern: always retry with exponential backoff, alert when retries are exhausted, and — for critical sources — add a circuit breaker that stops retrying after N consecutive failures and waits for manual intervention rather than hammering a source that's already down. Where possible, work with the source team so availability commitments and outage announcements exist at all, rather than discovering an outage only when a call fails.

*See also: [[source-retention-and-replayability]] · [[source-performance-impact-by-type]]*
