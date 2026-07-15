---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/data-engineering-system-design-11.md
last_updated: '2026-07-15'
qc: passed
slug: source-retention-and-replayability
topics:
- change-data-capture-cdc-and-data-sourcing
---

If the business needs 30 days of history but the source only retains 48 hours, Vu is blunt that no pipeline design can fix that — it's a negotiation with the source team or the business, not an engineering problem. Retention matters in two distinct ways: first, whether the source can even give you the data range you need; second, that it shapes your recovery options, which is why landing raw data in object storage and leaving it there is a common pattern — it lets you retain history longer without depending on the source's own retention window.

A related and separate question is replayability. A Kafka topic with 7-day retention lets you replay any event in that window simply by resetting the consumer's offset. A REST API that only returns the current state of a report offers no such thing — once you've missed a change, it's gone for good, because there was never a log to rewind. Vu's answer for non-replayable sources is the same pattern as before: store the data in object storage as you receive it, so you build your own replay capability rather than depending on the source having one.

*See also: [[incremental-extraction-strategies]] · [[log-based-cdc]] · [[source-availability-and-sla]]*
