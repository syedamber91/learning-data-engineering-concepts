---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
type: topic
tags: [ddia2, distributed-systems, single-node, scalability, elasticity]
sources:
  - raw/ch01.md
---
# Distributed Versus Single-Node Systems
A system in which several machines communicate over a network is a **distributed system**, and each participating process is a **node**. The book lists eight reasons you might want one, and they are worth separating because they call for different designs:

- **Inherent distribution** — if two or more users interact through their own devices, communication must cross a network; the system is distributed whether you like it or not.
- **Requests between cloud services** — data stored in one service and processed in another must move over the network, so cloud native systems and microservices are distributed by construction.
- **Fault tolerance / high availability** — redundancy across machines so that when one fails (or several, or the network, or a whole datacenter), another takes over.
- **Scalability** — spreading load when data volume or compute demand outgrows one machine.
- **Latency** — servers in several regions so users are served from somewhere geographically close, instead of waiting for packets to cross the world.
- **Elasticity** — scaling up and down with demand so you pay only for what you use, which is hard on a single machine that must be provisioned for peak.
- **Specialized hardware** — matching machine types to workloads: an object store wants many disks and few CPUs, an analysis system wants CPU and memory and no disks, an ML system wants GPUs.
- **Legal compliance** — data residency laws requiring data about people in a jurisdiction to be stored and processed inside it; scope varies (sometimes only medical or financial data), so a service with users across such jurisdictions must distribute.
- **Sustainability** — flexibility about where and when jobs run lets you follow renewable electricity and avoid straining the grid, cutting carbon emissions and cost.

These apply equally to services you write yourself and to off-the-shelf software such as databases.

## Subtopics
- [[Problems with Distributed Systems (2e)]] — partial failure, network cost, observability, and cross-service consistency.
- [[Microservices and Serverless (2e)]] — the dominant client/server decomposition, and function-as-a-service.
- [[Cloud Computing Versus Supercomputing (2e)]] — a contrasting large-scale computing tradition, and why its assumptions don't carry over.

## Key Takeaways
- "Distributed" is not one decision. Inherent distribution and legal compliance leave you no choice; scalability and elasticity are choices you can defer.
- The book's standing advice is explicit: doing a task on a single machine is often much simpler and cheaper, and you should not rush into distributing if a single machine can still do it.
- Single-node capability has grown enough to make that advice practical — CPUs, memory, and disks are larger, faster, and more reliable, and single-node engines like DuckDB, SQLite, and KùzuDB now cover many workloads.
- More nodes are not always faster: a simple single-threaded program on one computer can significantly outperform a cluster with over 100 CPU cores.

## Since the 1st Edition
The 1st edition assumed distribution as the default framing (its Part II was literally titled "Distributed Data") and had no comparable "should you even distribute?" section. The 2nd edition adds the counterargument explicitly, names modern single-node engines, and adds sustainability and legal compliance as first-class reasons — neither of which appeared in 2017.

## Related
- chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Ch 09 - The Trouble with Distributed Systems (2e)]] — the full accounting of what goes wrong
- [[Shared-Memory, Shared-Disk, and Shared-Nothing Architectures (2e)]] — the architectural taxonomy behind these choices
- [[Single-Node Systems (2e)]] — the cross-cutting concept note
