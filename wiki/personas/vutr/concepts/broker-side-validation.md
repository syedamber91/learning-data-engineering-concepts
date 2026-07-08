---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: broker-side-validation
topics:
- kafka
---

Client-side validation isn't really validation — clients opt into it and can simply skip it. A trusted, centralized validation point is needed, and since all clients connect to the broker, enforcement belongs there.

*See also: [[kafka-origin]] · [[paypal-kafka-scale]] · [[tiered-storage-kip-405]] · [[linkedin-kafka-scale]] · [[logical-offset]] · [[acks-setting]]*
