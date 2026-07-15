---
persona: vutr
kind: concept
sources:
- raw/olap-cost-and-multi-engine-comparison/i-spent-another-8-hours-understanding.md
- raw/olap-cost-and-multi-engine-comparison/the-internal-of-bigquery-snowflake.md
- raw/olap-cost-and-multi-engine-comparison/12-i-analyzed-the-pricing-models.md
last_updated: '2026-07-15'
qc: passed
slug: redshift-managed-storage-and-elastic-compute
topics:
- olap-cost-and-multi-engine-comparison
---

Redshift is the one warehouse in vutr's survey that started shared-nothing (data on the compute node's own disks, the legacy dc2 generation) and only later separated storage from compute — Redshift Managed Storage (RMS), available on the RA3 cluster generation and on serverless. RMS sits on Amazon S3 and inherits its durability/availability figures (99.999999999% durability, 99.99% availability across zones), with local SSD demoted to a tier-1 cache in front of it, kept warm by automatic fine-grained eviction and prefetching rather than manual tuning.

Physically, a table's data is split into data slices stored as a logical chain of 1MB blocks, each carrying header metadata (identity, table ownership, slice info). Blocks are indexed by an in-memory structure vutr calls a superblock — "an indexing structure with characteristics similar to many filesystems" per the source paper — which also tracks which running queries have touched which blocks. Zone maps (min/max per block) let a query scan the superblock to identify only the needed blocks before touching disk at all. A two-level reference-count cache handles hot/cold promotion: every access to a cold ("low level") block increments its reference count, repeated access promotes it to "high level," and eviction decrements the count until it hits zero, at which point the block drops to low level or is evicted outright — deliberately reminiscent, vutr notes, of Python's own object reference counting.

Because RMS commits synchronously to S3 across availability zones, multiple clusters can read consistent data, and deleting data from the main cluster only marks it for the object-store garbage collector rather than removing it immediately — so an SSD failure never loses anything already committed to S3. Update cost is kept down by incremental commits: RMS captures only the delta since the last commit rather than rewriting the whole state, and a log-based commit protocol (each superblock is itself a log of changes, separated from the in-memory structure it describes) reportedly improved commit performance by 40% by turning a series of random I/Os into a handful of sequential log appends. Concurrency control layers Multi-Version Concurrency Control with snapshot isolation on top, plus a Serial Safety Net (SSN) certifier that adds strict serializability guarantees while only needing summary information from prior committed transactions — a memory-efficient way to get stronger guarantees than snapshot isolation alone provides.

Decoupling storage from compute is precisely what makes Elastic Resize cheap: instead of physically shuffling data when nodes are added or removed, Redshift only redistributes the partition-to-node *assignment metadata*, generating a plan that minimizes data movement and keeps the cluster balanced, then refills each node's local cache from S3 in order of which data is hottest. That still leaves a real problem — after a resize, nodes don't necessarily hold equal amounts of data — which Redshift solves by decoupling compute parallelism (the number of worker processes/threads) from the number of data partitions entirely: when parallelism is lower than the partition count, one process just handles multiple partitions; when it's higher, multiple processes share a single partition's work. This is only possible because Redshift's work units are explicitly designed to be shareable. Concurrency Scaling applies the same underlying idea across time rather than node count: rather than resizing the base cluster, Redshift spins up whole additional clusters behind a single customer-facing endpoint when queries start queuing on the primary cluster, and those extra clusters fill their own local disks from S3 the same way a resized node would.

Elastic Resize and Cross-Instance Restore (moving a snapshot's data or a cluster's configuration between differently-sized clusters) are, per the source paper, heavily used features — customers reconfigure over 15,000 times a month — with a failure rate below 0.0001%, achieved by recording block/row/table counts and checksums before a reconfiguration and validating them again after it completes.

*See also: [[redshift-code-generation-and-self-tuning-operations]] · [[cloud-warehouse-compute-pricing-abstractions]] · [[cloud-warehouse-storage-pricing-dimensions]] · [[leader-follower-replication]]*
