---
persona: vutr
kind: concept
sources:
- raw/meta-data-stack-and-infrastructure/how-did-meta-move-terabytes-of-data.md
last_updated: '2026-07-15'
qc: passed
slug: scribe-write-path-and-batching
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Scribe's write path is a chain of batching stages, each trading a little latency for a lot of efficiency. An application's Producer instances accept writes and batch messages from multiple Categories together in memory purely to save memory footprint; they flush that batch to ScribeD, a local daemon running once per host that collects from every Producer instance on the machine and buffers on disk specifically so a crash before the data reaches durable storage doesn't lose it. ScribeD forwards to the Write Proxy, which runs admission-control checks and then re-splits the mixed-category batch so that messages from the same Category end up together again, before routing those per-category batches to the Batch Service.

The Batch Service is where the write path's core design decision shows up: it deliberately separates metadata from payload. It compresses and flushes the actual message bytes to two places — an ephemeral store for caching and Tectonic (the Durable Data Store) for long-term retention — while writing only the batch's metadata, including a pointer to where the payload landed, to [[logdevice]], the log-based metadata store. To keep the number of physical data blocks manageable, Scribe packs data from multiple categories into the same underlying block (accumulated in tens-of-megabytes chunks before a flush), while still grouping same-category data together within a block, up to 2MB, so reads stay efficient. This metadata/payload split is what lets Scribe give consumers a clean sequential-stream abstraction — via LogDevice's monotonically increasing sequence numbers — without every read having to touch the much larger payload store directly.

*See also: [[scribe]] · [[logdevice]] · [[tectonic]] · [[scribe-read-path-and-ephemeral-cache]] · [[scribe-delivery-guarantees]]*
