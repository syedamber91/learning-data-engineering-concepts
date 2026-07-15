---
persona: vutr
kind: entity
sources:
- raw/druid-pinot-real-time-olap/a-glimpse-of-apache-pinot-the-real.md
last_updated: '2026-07-15'
qc: passed
slug: pinot-broker
topics:
- apache-pinot-druid-and-real-time-olap
---

Pinot's brokers route each user's HTTP query request to the servers hosting the necessary segments, using a scatter-gather-merge approach: the request fans out to those servers, sub-part responses come back, and the broker merges them into the final result before returning it to the client. A load balancer can sit in front of a group of broker instances for better performance.

**Query processing.** The broker receives the query, parses and optimizes it, then picks a routing table for the target table and communicates with all servers named in it. Each server generates logical and physical query plans over its subset of segments using index information and column metadata, then executes them; when all plan executions finish, results are gathered, merged, and returned to the broker, which returns the final result to the client. If some servers error or time out, Pinot marks the overall result partial, and the user can choose to view the incomplete result or resubmit the query.

**Routing table generation.** A routing table is a list of servers paired with their segment-subset mapping, pre-generated per table. Pinot supports two strategies: the default balanced strategy divides all of a table's segments equally across servers — fine for small and medium clusters, but not for large ones, since a larger cluster raises the odds that any given query depends on a struggling server and gets slowed down by it. The dedicated strategy for large clusters instead limits how many hosts any single query touches, minimizing the blast radius of a failed host and reducing tail latency; LinkedIn implements this with a random greedy algorithm that produces an approximately minimal number of assignments while balancing load, generating several candidate routing tables (by taking a random subset of servers and adding more until the segments are covered) and picking the final one by a specific metric.

**Multi-tenancy.** Multiple tenants can share the same hardware. Pinot prevents one tenant from starving others by giving each tenant a token bucket: every query draws tokens proportional to its execution time, and when a tenant's bucket is empty its queries are held until tokens are available again. The bucket refills slowly, which absorbs short workload spikes while stopping a misbehaving tenant from consuming all shared resources.

*See also: [[apache-pinot]] · [[pinot-cluster-components]] · [[druid-broker]] · [[real-time-olap]]*
