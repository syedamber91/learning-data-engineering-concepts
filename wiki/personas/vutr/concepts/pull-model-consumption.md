---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: pull-model-consumption
topics:
- change-data-capture-cdc-and-data-sourcing
---

Even a Kafka consumer is a pull model — consumers continuously poll the broker for new messages rather than having messages pushed to them. It's worth internalizing that polling shows up everywhere in these pipelines, not just in query-based CDC.

*See also: [[log-based-cdc]] · [[read-replica]] · [[query-based-cdc]] · [[write-ahead-log]] · [[secrets-manager]] · [[trigger-based-cdc]]*
