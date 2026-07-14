---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
topic: Faults and Partial Failures
type: subtopic
tags: [ddia, hpc, cloud-computing, fault-tolerance]
sources:
  - raw/ch08.md
---
# Cloud Computing and Supercomputing
> Two ends of a design spectrum: supercomputers treat any fault as total failure and restart from a checkpoint, while internet services must absorb node failures without ever going offline.

## The Idea
Large-scale computing sits on a spectrum. At one end, high-performance computing (HPC): supercomputers with thousands of CPUs running scientific jobs like weather forecasting or molecular dynamics. At the other, cloud computing: multi-tenant datacenters full of commodity boxes on IP/Ethernet, with elastic allocation and metered billing. Traditional enterprise datacenters sit in between. The interesting part is how differently each end handles faults — and why this book sides with the cloud philosophy.

## How It Works
An HPC job periodically checkpoints its state to durable storage. When a node dies, the standard move is to halt the *entire* cluster workload, repair the node, and resume from the last checkpoint. A supercomputer thus behaves like one giant single-node machine: partial failure is deliberately escalated into total failure, the same instinct as a kernel panic. Internet services cannot do this, for structural reasons:
- They are *online* — users expect low-latency service at all times, so "stop the cluster for maintenance" is off the table; offline batch jobs can be paused cheaply.
- HPC uses specialized, individually reliable hardware with shared memory and RDMA; clouds use commodity machines that are cheaper per unit of performance but fail more often.
- Datacenter networks favor Clos topologies for high bisection bandwidth; supercomputers use meshes and toruses tuned to known communication patterns.
- At thousands of nodes, something is *always* broken. If the response to every fault is to give up, the system spends its life recovering instead of working.
- Tolerating dead nodes enables rolling upgrades (restart one node at a time), and in a cloud you can simply kill an underperforming VM and request a fresh one.
- Geo-distributed deployments talk over the slow, unreliable internet; supercomputers assume all nodes sit side by side.

## Trade-offs & Pitfalls
The HPC strategy buys simplicity — no partial-failure reasoning needed — at the cost of availability, which is unacceptable for a service. The cloud strategy demands that fault handling be designed into the software itself, and operators must know how it behaves under each fault. The classic wrong assumption is treating faults as rare exceptions: at scale they are the steady state, so it pays to inject faults deliberately in testing rather than hope.

## Examples & Systems
Weather simulation and molecular-dynamics jobs (checkpoint/restart); EC2-style clouds built on commodity gear; rolling upgrades as a routine payoff of fault tolerance; RDMA and torus interconnects on the HPC side.

## Related
- up: [[Faults and Partial Failures]] · chapter: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Reliability]] — no perfect reliability, only realistic promises
- [[Approaches for Coping with Load]] — scaling philosophy behind commodity clusters
- [[MapReduce]] — batch workloads that expect and survive node failures
- [[Hardware Faults]] — component failure rates that motivate this design
