---
persona: vutr
kind: entity
sources:
- raw/meta-data-stack-and-infrastructure/how-did-meta-move-terabytes-of-data.md
last_updated: '2026-07-15'
qc: passed
slug: scribe
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Scribe is Meta's internal message queue, built over 18 years to move data at a scale where it ingests over 15TB/s and serves over 110TB/s to consumers. Producers and consumers are client libraries built around a logical stream called a Category, which Scribe splits into physical shards — log files holding metadata pointers to the actual message payloads rather than the payloads themselves. The write path (producer → ScribeD → Write Proxy → Batch Service) and the storage split (LogDevice for metadata, Tectonic for durable payloads, plus a regional ephemeral cache) are what let Scribe offer three different delivery guarantees — best effort, at least once, and repeatable reads — depending on what the consuming application actually needs.

*See also: [[scribe-write-path-and-batching]] · [[scribe-read-path-and-ephemeral-cache]] · [[scribe-delivery-guarantees]] · [[logdevice]] · [[tectonic]]*
