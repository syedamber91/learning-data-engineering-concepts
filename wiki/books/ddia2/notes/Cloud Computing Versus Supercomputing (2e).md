---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
topic: Distributed Versus Single-Node Systems
type: subtopic
tags: [ddia2, hpc, supercomputing, fault-tolerance, network-topology]
sources:
  - raw/ch01.md
---
# Cloud Computing Versus Supercomputing
> High-performance computing is also large-scale distributed computing — but it assumes trust, co-location, and that you may stop the whole cluster to fix a node. None of those hold for a service that must stay up.

## The Idea
Cloud computing is not the only way to build large-scale computing systems. The alternative tradition is **high-performance computing (HPC)**, also called supercomputing. There are overlaps, but HPC has different priorities and techniques, and knowing the differences prevents importing assumptions that quietly do not hold.

## How It Works
The book lists five contrasts:
- **Workload.** Supercomputers run computationally intensive scientific work — weather forecasting, climate modelling, molecular dynamics, complex optimisation, partial differential equations. Cloud computing serves online services and business data systems that must answer user requests with high availability.
- **Fault handling.** A supercomputer runs large batch jobs that periodically checkpoint state to disk. When a node fails, the common solution is to stop the entire cluster workload, repair the faulty node, and restart from the last checkpoint. With cloud services, stopping the whole cluster is usually unacceptable, because the services must keep serving users with minimal interruption.
- **Communication and trust.** Supercomputer nodes typically communicate through shared memory and RDMA, giving high bandwidth and low latency but assuming a high level of trust among users. In cloud computing the network and machines are often shared by mutually untrusting organisations, requiring stronger mechanisms: resource isolation (e.g. virtual machines), encryption, and authentication.
- **Network topology.** Cloud datacenter networks are usually IP and Ethernet in **Clos topologies**, providing high *bisection bandwidth* — a common measure of overall network performance. Supercomputers often use specialised topologies such as multidimensional meshes and toruses, which perform better for HPC workloads with known communication patterns.
- **Geography.** Cloud computing distributes nodes across geographic regions; supercomputers generally assume all nodes are close together.

## Trade-offs & Pitfalls
- The checkpoint-and-restart model is the sharpest incompatibility. It is a perfectly good fault-tolerance strategy — for a job with an end. It is useless for a service that must never stop.
- Large-scale analytical systems sometimes share characteristics with supercomputing, so these techniques are worth knowing if you work in that area. But the book is explicit that it is mostly concerned with continually available services.

## Examples & Systems
Clos topologies in cloud datacenter networks; multidimensional meshes and toruses in supercomputer interconnects; RDMA and shared memory as HPC communication primitives.

## Since the 1st Edition
Retained and updated. The 1st edition made a similar cloud-versus-supercomputing comparison inside its Chapter 8 discussion of unreliable networks; the 2nd edition moves it forward into the architecture chapter and expands the network-topology and trust/isolation contrasts.

## Related
- up: [[Distributed Versus Single-Node Systems (2e)]] · chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Reliability and Fault Tolerance (2e)]] — the availability model cloud systems are held to instead
- [[Unreliable Networks (2e)]] — what the cloud network gives you to work with
