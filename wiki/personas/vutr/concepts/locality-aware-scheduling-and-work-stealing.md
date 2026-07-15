---
persona: vutr
kind: concept
sources:
- raw/snowflake-internals/i-read-another-paper-to-understand.md
- raw/snowflake-internals/i-spent-8-hours-diving-deep-into.md
- raw/snowflake-internals/i-spent-another-6-hours-understanding.md
last_updated: '2026-07-15'
qc: passed
slug: locality-aware-scheduling-and-work-stealing
topics:
- snowflake-internals
---

Because Snowflake assigns cached persistent-data files to worker nodes by consistent hashing (see [[ephemeral-storage-tiering-and-persistent-caching]]), it can schedule a task on the node its file already hashes to, avoiding a network fetch. This is what the paper calls locality-aware task scheduling, and it has a side effect worth internalizing: query parallelism ends up tightly coupled to how files are hashed across nodes, not to the query itself. The paper's own example makes this concrete — a customer with 1 million files running a ten-node Virtual Warehouse will, with high likelihood, spread *both* a 100-file query and a 100,000-file query across all ten nodes, simply because consistent hashing has already scattered files that widely.

Locality-first scheduling creates hotspots: if the files a query touches happen to consistently-hash onto a lopsided set of nodes, some nodes get overloaded while others sit idle. Snowflake's answer is work stealing — a node that finishes its own work early can pull a task from a slower, overloaded node instead of waiting. Later coverage of the same idea (surfacing again as "file stealing" for scan-heavy straggler scenarios) makes the mechanics explicit: when work stealing occurs, the persistent files needed for the stolen task are read directly from the remote store (S3) by the node doing the stealing, *not* from the overloaded node — which is exactly what prevents the rescue from becoming a second burden on the node it's supposed to be helping.

The paper frames locality-aware scheduling and work stealing as two ends of a spectrum the scheduler has to navigate, and names the actual extremes explicitly. One extreme — Snowflake's current implementation — places tasks with their cached data, spreading queries across all nodes per consistent hashing; this minimizes network traffic for reading persistent data but can increase the overhead of exchanging intermediate results between nodes, since more nodes means more inter-node traffic for join/shuffle-style operators. The other extreme is placing every task for a query on a single node: this removes intermediate-data exchange entirely (everything is local) but maximizes the network traffic needed to pull persistent data in, since one node now has to fetch everything itself. Snowflake's stated future direction is redesigning the scheduler to pick the right subset of nodes between these two extremes rather than defaulting to either one.

*See also: [[ephemeral-storage-tiering-and-persistent-caching]] · [[virtual-warehouse-isolation-and-shared-tenancy-economics]] · [[snowflake]]*
