---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: pull-over-push
topics:
- kafka
---

LinkedIn chose a pull model over push so consumers can retrieve messages at the maximum rate they can afford, rather than being flooded by messages pushed faster than they can handle. It moves flow control to the consumer's own capacity.
