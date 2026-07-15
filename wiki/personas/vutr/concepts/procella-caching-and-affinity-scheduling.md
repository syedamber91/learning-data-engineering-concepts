---
persona: vutr
kind: concept
sources:
- raw/google-infrastructure/procella-the-query-engine-at-youtube.md
last_updated: '2026-07-15'
qc: passed
slug: procella-caching-and-affinity-scheduling
topics:
- google-infrastructure
---

Because [[procella|Procella]] separates compute and storage, every read that isn't served from memory pays a network round trip to [[colossus-and-borg-as-shared-substrate|Colossus]] — so Procella layers several distinct caches to keep that round trip rare rather than trying to eliminate the separation itself. Data Servers cache Colossus file handles (the mapping from data blocks to the Colossus servers that hold them) so they don't repeatedly pay the cost of opening files; they separately cache header information such as column sizes and min/max values in a dedicated LRU cache; and they cache the actual columnar data itself in its own cache, which the [[artus-columnar-format|Artus]] format makes cheap to populate because Artus's in-memory and on-disk representations are identical — no transform step stands between a cached byte range and the query executor. Metadata Servers run a parallel version of the same idea, caching metadata locally to avoid remote calls back to the underlying metadata store for every query.

None of that caching helps if requests for the same data keep landing on different servers, so Procella adds affinity scheduling on top: the system tries to route the same data or metadata operation to the same server each time, so its caches actually accumulate hits instead of getting invalidated by scatter. The affinity is explicitly not rigid, though — if the preferred server is down, the request is rerouted to a different one, accepting a lower cache-hit rate in exchange for guaranteed completion. That fallback is presented as a deliberate trade for high availability, not a failure mode to be tuned away: correctness and progress win over cache efficiency when the two conflict. Taken together, the source's own framing is that when there's enough memory for the caches to hold what's needed, Procella effectively becomes an in-memory database — the disk-backed path exists for capacity and durability, but the hot path for a well-cached workload never has to touch Colossus at all.

*See also: [[procella]] · [[artus-columnar-format]] · [[colossus-and-borg-as-shared-substrate]] · [[procella-tail-latency-mitigation]]*
