---
title: "Idempotency"
area: "Data Pipelines"
topic: "Processing Paradigms"
tags: [idempotency, retries, exactly-once, reliability]
---

# Idempotency

*Part of [[processing-paradigms-moc|Processing Paradigms]] · [[data-pipelines-moc|Data Pipelines]]*

**In one line:** An idempotent step gives the same result whether it runs once or five times — so retrying after a failure is always safe.

**Picture this:** Pressing a lift's "call" button. Press it once or jab it ten times — the lift comes exactly once. Compare that to a "charge my card" button that bills you every press. The lift button is idempotent; the naive charge button is not.

**How it actually works:** Pipelines fail and get retried constantly (network drops, crashes). If a retry re-adds rows you already added, you get duplicates and wrong totals. To be idempotent you design steps so re-running changes nothing extra: use a unique key per record and *upsert* (insert-or-update) instead of blind insert, or check "did I already process this batch?" before acting.

**In the real world:** Payment systems like Stripe attach an *idempotency key* to each charge request. If your app retries because the reply got lost, Stripe sees the same key and refuses to charge the customer twice — turning a scary network glitch into a non-event.

**Why you'd use it (and when not to):** Build idempotency into anything that can be retried or replayed — which in data engineering is almost everything. It takes extra design thought, so for a truly one-shot manual task it may be unnecessary.

**Connects to:** [[batch-vs-streaming]] · [[transactions-acid]] · [[automated-testing]]
