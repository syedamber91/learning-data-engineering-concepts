---
persona: vutr
kind: concept
sources:
- raw/snowflake-internals/i-read-another-paper-to-understand.md
- raw/snowflake-internals/i-spent-8-hours-diving-deep-into.md
- raw/snowflake-internals/i-spent-another-6-hours-understanding.md
last_updated: '2026-07-15'
qc: passed
slug: virtual-warehouse-isolation-and-shared-tenancy-economics
topics:
- snowflake-internals
---

A Virtual Warehouse (VW) is Snowflake's unit of elastic compute: a cluster of cloud VM "worker nodes," sized only by an abstract T-shirt label (X-Small to XX-Large) so customers never touch the underlying instance configuration — a design explicitly compared, across the posts, to BigQuery's "slot" abstraction. Because table data lives in S3 rather than on the VW's own disks, VWs are stateless: they scale up or down on demand without any risk of losing data, and Snowflake keeps a pool of pre-warmed EC2 instances on standby so that scaling happens in tens of seconds rather than waiting on cold VM boot time. Each VW operates on an isolated set of nodes with its own ephemeral storage, so one customer's query load never contends with another's on the same node; each query runs on exactly one VW, workers are never shared across VWs, and — notably — a failed query cannot be partially retried, it must restart from the beginning.

That per-VW isolation is clean for the customer but costly for Snowflake. The paper's own measurement is blunt: for up to 30% of VWs, the standard deviation of CPU usage over time is as large as the mean itself, and customers provision VW size for peak demand, not average — so a VW sized for its worst moment sits underutilized the rest of the time. Worse, high-utilization periods across different customers' VWs are not synchronized, so there's no natural pooling effect; the resources one idle VW isn't using can't spill over to a busy VW next to it, because isolation is enforced at the node level.

This tension between performance isolation and utilization was tolerable under hourly billing — if a node from the pre-warmed pool was used by *any* customer for even part of an hour, Snowflake could bill the whole hour to that customer, effectively pricing over the idle time. Per-second billing (the industry-wide shift among major cloud vendors) removes that accounting trick: idle cycles on a pre-warmed node can no longer be charged to any one customer, so every unused second is now a cost Snowflake itself absorbs rather than passes on. That's the specific economic pressure driving Snowflake toward a shared-resource model underneath the VW abstraction — sharing compute and ephemeral storage across customers while keeping the VW abstraction customers see unchanged.

Moving to shared resources without breaking isolation raises two separate hard problems for ephemeral storage specifically (compute is comparatively easy, since a centralized task scheduler already exists). First, because ephemeral storage holds *both* cached persistent data and intermediate data jointly, evicting one tenant's idle cache to make room for another requires predicting when the first tenant will need that data again — which isn't really predictable. Second, elasticity itself threatens isolation: all cached data is consistently hashed onto one global address space, so scaling up ephemeral storage would trigger a rehash affecting *every* tenant's cache, not just the tenant whose resources changed, causing cache misses for everyone else. The fix the paper points toward is giving each tenant a private address space and only reorganizing data for the tenants that actually received new resources — but as of the paper, this is future work, not a shipped design.

*See also: [[ephemeral-storage-tiering-and-persistent-caching]] · [[locality-aware-scheduling-and-work-stealing]] · [[snowflake]] · [[shared-nothing-vs-shared-disk]]*
