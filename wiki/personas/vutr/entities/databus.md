---
persona: vutr
kind: entity
sources:
- raw/linkedin-data-infrastructure/diving-deep-into-linkedins-data-infrastructure.md
last_updated: '2026-07-15'
qc: passed
slug: databus
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Databus is LinkedIn's change data capture system — the "stream system" tier in [[linkedin-three-tier-service-architecture]] — built to deliver CDC events from LinkedIn's primary databases (Oracle and MySQL, via built-in adapters, with support for extending to other sources) to applications like the Social Graph Index, the People Search Index, and processors such as Company Name and Position Standardization. On the sink side, it exposes a subscription API that lets applications subscribe to changes from a given source.

The pipeline has three parts. The **relay** captures changes from the source database — either via triggers or by consuming the database's own replication log — and serializes each change into Avro before buffering it in memory. Each captured change becomes a Databus CDC event carrying a sequence number, metadata, and the serialized payload. LinkedIn runs multiple shared-nothing relays connected directly to databases or to other relays, so the change stream itself has replicated availability. The **bootstrap server** exists because a relay's in-memory buffer can't hold unlimited history: it provides long-term storage for the event stream and serves the requests a relay can't. It answers two kinds of query — a consolidated delta since a given position (returning only the latest update per row/key, so a lagging client can catch up quickly) and a consistent snapshot at a position (plus the sequence number of the last transaction applied in that snapshot, so the client knows where to resume consuming from the relay). Underneath, the bootstrap server keeps two separate storages to answer both without disturbing the relay's own event stream: an append-only log that a log writer fills from the relay, and a snapshot storage — holding only the latest event per row/key — that a log applier updates by watching for new log entries. Recent requests are served straight from the log; everything else comes from the snapshot. The **client library** is the piece that actually connects relays, bootstrap servers, and a consumer's business logic, and it bundles progress tracking, a choice of push or pull interfaces, local buffering and flow control, multi-threaded processing, and retry logic for failures.

Databus began narrowly, as the mechanism keeping LinkedIn's social graph and search index consistent with the primary databases, and grew into a general-purpose replication system underpinning read replicas, cache consistency, and near-line processing more broadly. At LinkedIn's operating scale it captures changes from close to a hundred data sources using tens of relays, at very low latency — and it's also the replication mechanism [[espresso]] itself relies on internally to keep its storage-node replicas timeline-consistent.

*See also: [[voldemort]] · [[espresso]] · [[linkedin-three-tier-service-architecture]] · [[linkedin-data-infrastructure]]*

## Related in the other wiki
- [[Change Data Capture]] — DDIA's chapter-11 concept names Databus directly as one of its real-world CDC examples; this entity is the grounded, mechanism-level account (relay, bootstrap server, log/snapshot split) behind that one-line mention.
