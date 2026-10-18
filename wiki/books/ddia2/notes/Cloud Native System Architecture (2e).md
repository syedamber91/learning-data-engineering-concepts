---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
topic: Cloud Versus Self-Hosting
type: subtopic
tags: [ddia2, cloud-native, object-storage, storage-compute-separation, multitenancy]
sources:
  - raw/ch01.md
---
# Cloud Native System Architecture
> The cloud didn't just change who owns the servers — it changed how data systems are built. Cloud native means building *on top of other cloud services* rather than on top of an operating system.

## The Idea
Beyond the economic shift from buying hardware to subscribing to a service, the cloud had a profound technical effect. **Cloud native** describes an architecture designed to take advantage of cloud services. In principle almost anything self-hostable could be offered as a managed service, and managed versions of most popular data systems now exist — but systems *designed from the ground up* for the cloud demonstrably do better: better performance on the same hardware, faster recovery from failures, faster scaling of compute to match load, and support for larger datasets.

| Category | Self-hosted systems | Cloud native systems |
|---|---|---|
| Operational / OLTP | MySQL, PostgreSQL, MongoDB | AWS Aurora, Azure SQL DB Hyperscale, Google Cloud Spanner |
| Analytical / OLAP | Teradata, ClickHouse, Spark | Snowflake, Google BigQuery, Azure Synapse Analytics |

## How It Works
**Layering of cloud services.** Self-hosted data systems mostly have simple requirements: a conventional OS, files on a filesystem, TCP/IP. A few need special hardware (GPUs for ML, RDMA network interfaces), but on the whole they use generic resources — CPU, RAM, filesystem, IP network. Run in IaaS, such software gets VMs (*instances*) with an allocation of CPU, memory, disk, and bandwidth; those provision faster and come in more sizes than physical machines, but you still administer them yourself. The cloud native idea is different: build higher-level services **on top of lower-level cloud services**, not just on top of the OS. Object storage — Amazon S3, Azure Blob Storage, Cloudflare R2 — is the base layer. Its API is more limited than a filesystem's (basic reads and writes), but it hides the physical machines: the service spreads data across many machines, so you never worry about one disk filling up, and entire machine or disk failures lose no data. Other services then build on object storage: Snowflake is a cloud data warehouse relying on S3 for storage, and further services build on Snowflake in turn.

**Separation of storage and compute.** Traditionally disk is treated as durable, with RAID keeping copies across several disks on the same machine, transparently to applications. In the cloud, local instance disks are treated more like an **ephemeral cache** — they become inaccessible if the instance fails, or if it is swapped for a bigger or smaller one on different physical hardware. Virtual disks that detach and reattach (Amazon EBS, Azure managed disks, Google persistent disks) are an alternative: not physical disks but a cloud service run by a separate set of machines emulating a block device (typically 4 KiB blocks). That emulation lets traditional disk-based software run in the cloud, but adds overhead a purpose-built system avoids, and makes the application very sensitive to network glitches, since every I/O on a virtual block device is a network call. Cloud native services therefore generally avoid virtual disks and build on dedicated storage services instead. Object stores suit large files (hundreds of kilobytes to several gigabytes); individual database rows are far smaller, so cloud databases typically manage small values in a separate service and pack larger blocks of many values into an object store. The result is that storage and compute — one machine's disk and one machine's CPU/RAM in the traditional design — become **disaggregated**: S3 only stores files, so analysing that data means running code somewhere else and moving the data over the network.

**Multitenancy.** Cloud native systems are often multitenant: rather than a separate machine per customer, several customers' data and computation share the same hardware and service.

## Trade-offs & Pitfalls
- Higher-level abstractions are more oriented toward particular use cases. If your needs match what a higher-level system was designed for, using it beats building from lower-level parts; if no high-level system fits, building from lower-level components is the only option. There is no universally right layer.
- Disaggregation implies transferring data over the network, with all the cost that carries.
- Multitenancy can improve hardware utilisation, scalability, and manageability for the provider, but requires careful engineering so one customer's activity does not affect another's performance or security.

## Examples & Systems
S3, Azure Blob Storage, Cloudflare R2 (object storage); Amazon EBS, Azure managed disks, GCP persistent disks (virtual block devices); Aurora, Azure SQL DB Hyperscale, Spanner, Snowflake, BigQuery, Synapse Analytics (cloud native databases).

## Since the 1st Edition
Entirely new, and arguably the most consequential addition to the book's architectural vocabulary. In 2017 the 1st edition discussed replication and partitioning on machines with their own disks; this section explains why a decade of systems stopped being built that way.

## Related
- up: [[Cloud Versus Self-Hosting (2e)]] · chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Object Stores (2e)]] — the same technology seen from the batch-processing side
- [[Cloud Data Warehouses (2e)]] — storage/compute separation applied to analytics
- [[Separation of Storage and Compute (2e)]] — the cross-cutting concept note
