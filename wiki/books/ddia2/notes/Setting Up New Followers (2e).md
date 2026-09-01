---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Single-Leader Replication
type: subtopic
tags: [ddia2, snapshot, catch-up, object-storage, zero-disk-architecture, wal-g]
sources:
  - raw/ch06.md
---
# Setting Up New Followers
> Snapshot, copy, replay the log from the snapshot's exact position, catch up. Four steps, no downtime — and increasingly the snapshot lives in an object store.

## The Idea
From time to time you need new followers — to increase the number of replicas or to replace failed nodes. **Simply copying data files from one node to another is typically not sufficient**: clients are constantly writing, the data is always in flux, and a standard file copy would see different parts of the database at different points in time, so the result might not make any sense. You could make the on-disk files consistent by **locking the database**, making it unavailable for writes — but that defeats high availability.

## How It Works
Fortunately it can usually be done without downtime:
1. **Take a consistent snapshot** of the leader's database at some point in time, if possible without locking the entire database. Most databases have this feature, since it is also required for backups; in some cases third-party tools are needed, such as **Percona XtraBackup for MySQL**.
2. **Copy the snapshot** to the new follower node.
3. **The follower connects to the leader and requests all data changes since the snapshot was taken.** This requires the snapshot to be associated with **an exact position in the leader's replication log** — PostgreSQL calls it the **log sequence number**; MySQL has two mechanisms, **binlog coordinates** and **global transaction identifiers (GTIDs)**.
4. When the follower has processed the backlog, it has **caught up** and can continue processing changes as they happen.

The practical steps vary significantly by database: **in some systems this is fully automated; in others it is a somewhat arcane multistep workflow that must be performed manually by an administrator.**

You can also **archive the replication log to an object store** along with periodic whole-database snapshots — a good way of implementing backups and disaster recovery, and steps 1 and 2 can then be performed by downloading those files. **WAL-G** does this for PostgreSQL, MySQL, and SQL Server; **Litestream** does the equivalent for SQLite.

## Trade-offs & Pitfalls
**Databases backed by object storage.** Object storage is increasingly used not just for archiving but to serve **live queries**. The benefits are substantial:
- **Inexpensive** compared to other cloud storage, letting databases keep less-frequently-queried data on cheaper, higher-latency storage while serving the working set from memory, SSDs, and NVMe.
- **Multi-zone, dual-region, or multi-region replication with very high durability guarantees**, which also lets databases bypass inter-zone network fees.
- **Conditional write** support — essentially a compare-and-set operation — can implement **transactions and leadership election**.
- Storing data from multiple databases in one object store **simplifies data integration**, particularly with open formats such as Parquet and Iceberg.

Together these **dramatically simplify database architecture by shifting transactions, leadership election, and replication onto object storage**. But the trade-offs are real: object stores have **much higher read and write latencies** than local disks or virtual block devices; many providers charge a **per-API-call fee**, forcing systems to batch reads and writes, which further increases latency; objects are often **immutable**, making random writes into a large object extremely resource-intensive; and many object stores **lack standard filesystem interfaces**. FUSE lets operators mount buckets as filesystems, but many FUSE interfaces lack POSIX features such as nonsequential writes or symlinks that systems may depend on.

Systems handle this differently. Some use **tiered storage**, keeping less-accessed data on object storage and new or hot data on SSDs, NVMe, or memory. Others use object storage as the primary tier but keep the **WAL on a separate low-latency system** such as Amazon EBS or Neon's Safekeepers. Some go further with a **zero-disk architecture (ZDA)**: all data persisted to object storage, disks and memory used strictly for caching, so **nodes have no persistent state** — which dramatically simplifies operations. **WarpStream, Confluent Freight, Buf's Bufstream, and Redpanda Serverless** are Kafka-compatible systems built this way; nearly every modern cloud data warehouse also adopts such an architecture, as do **Turbopuffer** (vector search) and **SlateDB** (a cloud native LSM engine).

## Examples & Systems
Percona XtraBackup; PostgreSQL log sequence numbers; MySQL binlog coordinates and GTIDs; WAL-G and Litestream; WarpStream, Confluent Freight, Bufstream, Redpanda Serverless, Turbopuffer, SlateDB for zero-disk architectures.

## Since the 1st Edition
The four-step follower setup is unchanged from the 1st edition's [[Setting Up New Followers]]. **Everything about object storage is new** — WAL archiving to object stores, the four benefits, the four trade-offs, FUSE's POSIX gaps, tiered storage, WAL-on-EBS hybrids, and **zero-disk architecture** with its system roster. This is one of the clearest places where the 2nd edition absorbs the cloud-native shift.

## Related
- up: [[Single-Leader Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Cloud Native System Architecture (2e)]] — separation of storage and compute, stated generally
- [[Object Stores (2e)]] — object storage from the batch-processing side
- [[Handling Node Outages (2e)]] — the other reason you need a new follower
- 1st edition: [[Setting Up New Followers]] — the same four steps, no object storage
