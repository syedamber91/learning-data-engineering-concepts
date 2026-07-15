---
persona: vutr
kind: concept
sources:
- raw/snowflake-internals/i-read-another-paper-to-understand.md
- raw/snowflake-internals/i-spent-8-hours-diving-deep-into.md
- raw/snowflake-internals/i-spent-another-6-hours-understanding.md
last_updated: '2026-07-15'
qc: passed
slug: ephemeral-storage-tiering-and-persistent-caching
topics:
- snowflake-internals
---

Snowflake's local disks inside a Virtual Warehouse hold two different things that are easy to conflate: intermediate data thrown off by running operators (joins, sorts, spills) and a cache of persistent data files pulled down from S3. Both live in the same "ephemeral storage system," and the two-part 2020 paper Vu read spends most of its attention here precisely because — unlike the remote persistent store, which just reuses S3 — this custom-built layer is where Snowflake's own design decisions actually show up.

The tiering logic for intermediate data is a straightforward cascade: write to local memory first; when memory fills, spill to local SSD; when SSD fills too, spill onward to remote storage (S3). In-memory would be fastest, but fitting hundreds of GBs or TBs of a single query's intermediate results entirely in memory is simply not feasible. Spilling to S3 rather than to another compute node's disk is a deliberate choice — it avoids one node's spill turning into another node's out-of-memory problem, and it keeps the ephemeral storage system "thin" instead of having to track where intermediate data physically landed across the cluster. Snowflake also prioritizes this space for intermediate data over the persistent-data cache: if a query needs the room, cached files get evicted first.

The persistent-data cache side works differently. A worker node's cache holds file headers plus whichever columns queries have actually needed — not whole files — for as long as that worker node lives, and it is shared across every query that node subsequently runs. Eviction is a plain LRU policy. Assignment of which file goes to which node is done by consistent hashing on the file name, so that repeated queries against the same table tend to land on the same node and reuse what's already cached — this is also the basis for [[locality-aware-scheduling-and-work-stealing]]. Because a copy of every cached file also sits durably in S3, the cache has to behave as a *write-through* cache for consistency: nothing in ephemeral storage is allowed to be the only copy of persisted data.

Consistent hashing has an obvious cost when the node count changes — the naive version reshuffles which node owns which file, meaning data has to move. Snowflake sidesteps this with lazy consistent hashing, and the worked example makes the mechanism concrete: at t0, four nodes hold files 1–4 one-to-one, with node 1 additionally holding file 5 (and task 5, which reads it). When a fifth node joins, Snowflake does *not* immediately move file 5 to node 5. Instead it waits until task 5 is scheduled again — at that point, consistent hashing now says file 5 belongs on node 5, so the scheduler places task 5 there, node 5 reads file 5 directly from the remote persistent store and caches it locally, and node 1's now-stale copy simply falls out of use and gets evicted by LRU. Reassignment happens lazily, driven by task scheduling, not by an eager rebalance.

The paper is explicit that this isn't a finished design. It names the cache-hit-rate dependency on VW size versus the volume of intermediate data (since both share the same ephemeral storage pool) as something needing "more fine-grained analysis," flags the scenario where cache demand exceeds intermediate-data demand as unresolved given intermediate data's priority, and anticipates that as non-volatile memory and deeper remote-ephemeral tiers mature, the caching mechanism will need to coordinate across more storage layers than just memory/SSD/S3.

*See also: [[locality-aware-scheduling-and-work-stealing]] · [[virtual-warehouse-isolation-and-shared-tenancy-economics]] · [[snowflake]] · [[amazon-s3]]*
