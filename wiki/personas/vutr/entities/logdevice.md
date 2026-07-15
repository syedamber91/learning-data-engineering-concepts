---
persona: vutr
kind: entity
sources:
- raw/meta-data-stack-and-infrastructure/how-did-meta-move-terabytes-of-data.md
last_updated: '2026-07-15'
qc: passed
slug: logdevice
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

LogDevice is the log-based storage system that holds Scribe's message metadata, not the payloads. For each Category, LogDevice appends batch metadata to a per-physical-shard file called a log, where every record carries a monotonically increasing sequence number; Meta runs millions of these logs across LogDevice clusters, replicating each record across a subset of the cluster's storage nodes. Because millions of clients querying LogDevice directly would overwhelm it despite being "a transactional, highly available database," Meta built a caching and distribution layer plus periodic background jobs on top of it that fan the metadata out to clients instead of serving every request from LogDevice itself.

*See also: [[scribe]] · [[scribe-write-path-and-batching]] · [[scribe-read-path-and-ephemeral-cache]]*
