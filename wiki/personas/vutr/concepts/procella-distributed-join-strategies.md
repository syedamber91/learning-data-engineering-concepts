---
persona: vutr
kind: concept
sources:
- raw/google-infrastructure/procella-the-query-engine-at-youtube.md
last_updated: '2026-07-15'
qc: passed
slug: procella-distributed-join-strategies
topics:
- google-infrastructure
---

[[procella|Procella]] doesn't commit to one join algorithm; it picks from five strategies per query, chosen either by an explicit hint or implicitly by the optimizer based on the layout and size of the data involved. Broadcast join is for when one side of the join is small enough to fit entirely in the memory of every data server running the query — the small table is replicated everywhere rather than shuffled. Co-partitioned join applies when both the fact and dimension tables are already partitioned on the same join key, so a data server only ever needs to load the small subset of the other table's data that shares its partition, avoiding any data movement across the network for the join itself. Shuffle join is the fallback when both sides are large: data from both tables is redistributed ("shuffled") across a set of intermediate servers keyed on the join column, the classic strategy for joins where neither the broadcast nor the co-partition shortcut applies.

The remaining two strategies are more specialized. Pipelined join targets the case where the right-hand side of the join is a complex subquery that's likely to produce a small result set — that subquery runs first, and its (small) result is then sent to the servers handling the left-hand-side query, which ends up behaving like a broadcast join even though it started from a query the optimizer couldn't statically size in advance. Remote lookup join covers the common case where the dimension table is partitioned on the join key but the fact table isn't: rather than shuffling the fact table, the data server processing it sends remote RPCs to the server responsible for the relevant dimension-table partitions to fetch just the keys and values it needs for the join. Across all five, the throughline is that Procella tries to avoid moving data across the network whenever partitioning, size, or an intermediate result already makes it unnecessary — partitioning and clustering choices made at table-registration time (date-partitioned fact tables, dimension-key-partitioned dimension tables) exist in part to make co-partitioned and remote-lookup joins possible in the first place.

*See also: [[procella]] · [[colossus-and-borg-as-shared-substrate]]*
