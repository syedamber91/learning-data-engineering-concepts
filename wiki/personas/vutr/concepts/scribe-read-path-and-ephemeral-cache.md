---
persona: vutr
kind: concept
sources:
- raw/meta-data-stack-and-infrastructure/how-did-meta-move-terabytes-of-data.md
last_updated: '2026-07-15'
qc: passed
slug: scribe-read-path-and-ephemeral-cache
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Reading from Scribe means talking to metadata and payload through two separate services, mirroring the write path's split (see [[scribe-write-path-and-batching]]). A Consumer instance opens a stateful connection to the Read Stream Service, which Meta deliberately colocates in the same region as the consumer; that service identifies the relevant LogDevice clusters and physical shards, hands the actual record-pulling to a "reader" instance, and merges the results back into one metadata stream for the consumer. The consumer then takes the data pointer from that metadata and issues an RPC to the Read Proxy, whose job is everything related to fetching the actual payload.

The interesting design choice is how the Read Proxy avoids hitting Tectonic (the Durable Data Store) directly on every read. It first checks the regional Ephemeral Data Store (EDS) — a two-tier cache with a remote tier (Memcached, holding payloads for 1-2 hours, which Meta judged sufficient for consumers reading merely "warm" data) and a local tier (Cachelib, using Read Proxy hosts' spare memory for the hottest data). Because a Category's producers run globally, a consumer's read very often needs payload data that physically lives in a different region than the Durable Data Store; when a Read Proxy in region A needs data whose DDS copy is in region B, it routes the request to a Read Proxy instance in region B, which populates the data into region B's EDS — so a later request from a *third* region, C, gets served from region B's cache instead of crossing all the way to the original DDS, at the cost of still being a cross-region hop.

The Read Proxy does more than fetch bytes: Meta explicitly designed it as "a data staging area," transforming payloads from their original row format into columnar format as it populates the EDS, so downstream analytics consumers never pay that conversion cost themselves, and it can push down a consuming application's filter — evaluating a subset of SQL directly inside the proxy — before data ever leaves it.

*See also: [[scribe]] · [[scribe-write-path-and-batching]] · [[tectonic]] · [[scribe-delivery-guarantees]]*
