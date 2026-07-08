---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: page-cache-storage
topics:
- kafka
---

Rather than building a proprietary cache, Kafka leans on the OS filesystem and the kernel page cache to hold data before it is flushed to disk. This sidesteps JVM object overhead and GC pain, and takes advantage of the fact that sequential disk access can outperform random RAM access.

*See also: [[kafka-origin]] · [[paypal-kafka-scale]] · [[tiered-storage-kip-405]] · [[linkedin-kafka-scale]] · [[logical-offset]] · [[acks-setting]]*
