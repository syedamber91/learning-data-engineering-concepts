---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Scalability
type: subtopic
tags: [ddia2, shared-nothing, vertical-scaling, horizontal-scaling, nas, san]
sources:
  - raw/ch02.md
---
# Shared-Memory, Shared-Disk, and Shared-Nothing Architectures
> Three ways to add hardware: one big machine, several machines sharing storage, or many machines sharing nothing. The third won, but the cloud has quietly revived a version of the second.

## The Idea
The simplest way to increase a service's hardware resources is to move it to a more powerful machine. Individual CPU cores are no longer getting significantly faster, but you can buy (or rent) a machine with more cores, more RAM, and more disk. This is **vertical scaling** or **scaling up**.

## How It Works
**Shared-memory architecture.** Parallelism on a single machine via multiple processes or threads; all threads in a process access the same RAM, hence the name. The problem is that **cost grows faster than linearly** — a high-end machine with twice the hardware of a lower-spec one typically costs significantly more than twice as much — and because of bottlenecks, it is unlikely to actually handle twice the load.

**Shared-disk architecture.** Several machines with independent CPUs and RAM, but data stored on an array of disks shared among them over a fast network: **network-attached storage (NAS)** or a **storage area network (SAN)**. Traditionally used for on-premises data warehousing. **Contention and the overhead of locking limit its scalability.**

**Shared-nothing architecture** — also called **horizontal scaling** or **scaling out**. A distributed system of multiple nodes, each with its own CPUs, RAM, and disks. Any coordination between nodes happens at the software level over a conventional network.

Its advantages, and why it gained popularity:
- Potential to scale linearly.
- Can use whatever hardware offers the best price/performance ratio, especially in the cloud.
- Can more easily adjust hardware resources as load rises and falls.
- Can achieve greater fault tolerance by spreading across multiple datacenters and regions.

## Trade-offs & Pitfalls
- Shared-nothing's downsides are real: it requires **explicit sharding**, and it incurs all the complexity of distributed systems.
- **The cloud has blurred the taxonomy.** Some cloud native database systems use separate services for storage and transaction execution, with multiple compute nodes sharing access to the same storage service. This resembles shared-disk, but avoids the scalability problems of older systems — because instead of offering a filesystem (NAS) or block device (SAN) abstraction, the storage service exposes a **specialized API designed for the specific needs of the database**. The abstraction, not the topology, was the bottleneck.

## Examples & Systems
NAS and SAN as shared-disk storage; cloud native databases with disaggregated storage services as the modern reprise of shared-disk.

## Since the 1st Edition
Substantially new. The 1st edition's corresponding subtopic, [[Approaches for Coping with Load]], discussed scaling up versus scaling out and shared-nothing in general terms but did not lay out the three-way taxonomy, did not name NAS/SAN, and — necessarily — did not have the observation that cloud storage/compute separation revives shared-disk without its historical penalty.

## Related
- up: [[Scalability (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Cloud Native System Architecture (2e)]] — the separation-of-storage-and-compute detail
- [[Ch 07 - Sharding (2e)]] — the explicit sharding shared-nothing requires
- 1st edition: [[Approaches for Coping with Load]] — the looser predecessor
