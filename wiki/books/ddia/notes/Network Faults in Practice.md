---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Networks
type: subtopic
tags: [ddia, network-faults, network-partition, chaos-engineering]
sources:
  - raw/ch08.md
---
# Network Faults in Practice
> Decades of networking have not produced reliable networks — faults are routine even inside one company's datacenter, and software with undefined fault handling can do arbitrarily bad things.

## The Idea
It is tempting to treat network failure as an exotic edge case. Measurement says otherwise: network problems are surprisingly frequent even in controlled, single-operator environments, so every piece of software that communicates must have a known, tested reaction to them.

## How It Works
The evidence Kleppmann assembles: one study of a medium-sized datacenter counted roughly 12 network faults per month — about half cutting off a single machine, the other half an entire rack. Another study of top-of-rack switches, aggregation switches, and load balancers found that adding redundant gear helps less than hoped, because much downtime stems from human error (misconfigured switches), which redundancy cannot absorb. Public clouds like EC2 are known for frequent transient glitches; private datacenters can be calmer but are not immune — a switch software upgrade can trigger a topology reconfiguration during which packets stall for over a minute. Failures can also be bizarrely asymmetric: a network interface that drops every inbound packet while sending outbound packets fine, meaning a link working one way proves nothing about the other direction. Terminology note: a network cut isolating one part of the cluster is a *network partition* or netsplit, though the book prefers "network fault" to avoid collision with storage [[Partitioning]].

## Trade-offs & Pitfalls
The dangerous mistake is not that faults happen, but that software meets them in an untested state. Undefined error handling has caused clusters to deadlock permanently even after the network recovered, and in one case to delete all data. Handling faults does not require tolerating them — if your network is normally solid, surfacing an error to users during an outage is a legitimate strategy — but you must *know* how the system reacts and that it can recover. That argues for deliberately injecting network faults and observing the response, the philosophy behind Chaos Monkey (see [[Reliability]]).

## Examples & Systems
Sharks biting undersea cables; the 12-faults-per-month datacenter study; redundant-gear study undermined by human misconfiguration; EC2's transient glitches; the minute-long packet delay during a switch upgrade; the one-directional NIC failure; Chaos Monkey-style fault injection.

## Related
- up: [[Unreliable Networks]] · chapter: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Reliability]] — Chaos Monkey and fault-injection testing
- [[Partitioning]] — the storage sense of "partition" this term clashes with
- [[Split Brain]] — the classic disaster a network partition can trigger
- [[Detecting Faults]] — sibling: what signals you get when things break
