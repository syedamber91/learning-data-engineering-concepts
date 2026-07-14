---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Networks
type: subtopic
tags: [ddia, circuit-switching, packet-switching, latency, utilization]
sources:
  - raw/ch08.md
---
# Synchronous Versus Asynchronous Networks
> Telephone networks achieve bounded delay by reserving a fixed circuit per call; datacenter networks accept unbounded delay because packet switching squeezes far more value out of the wires for bursty traffic.

## The Idea
Why not fix unreliability in hardware so software never worries about it? The fixed-line telephone network proves bounded, reliable delivery is *possible*: dropped calls and delayed audio are rare. Understanding why computer networks nonetheless behave differently reveals that variable delay is an economic choice, not physics.

## How It Works
A phone call establishes a *circuit*: a fixed bandwidth allocation reserved along the whole route for the call's duration. An ISDN network runs 4,000 frames per second, and a call gets 16 bits reserved in every frame per direction — guaranteed delivery of 16 bits of audio every 250 microseconds. Because the space in the next hop is pre-reserved, there is no queueing, and hence a fixed maximum end-to-end latency: a *bounded delay*. This is a synchronous network. TCP could hardly be more different: packets grab whatever bandwidth happens to be free, an idle connection uses none, and a variable-sized blob (email, web page) is transferred as fast as conditions allow. Ethernet and IP are packet-switched and have no circuit concept, so queueing — and unbounded delay — is intrinsic. The reason is workload shape: circuits suit constant-rate audio/video; web requests and file transfers are bursty with no natural bandwidth requirement. Forcing bursty traffic onto circuits means guessing an allocation — too low wastes time, too high may make the circuit impossible to establish. Packet switching maximizes wire utilization, and since the wire's cost is fixed, better utilization makes every byte cheaper.

## Trade-offs & Pitfalls
The general principle: variable delay is a consequence of *dynamic resource partitioning*. Static partitioning (one of 10,000 fixed call slots on a trunk wire; a fixed CPU-cycle allocation per thread) gives latency guarantees at the cost of idle capacity; dynamic sharing (internet bandwidth, CPU run queues, virtual machines) buys high utilization at the cost of queueing and jitter. Hybrids exist — ATM in the 1980s; InfiniBand with link-layer flow control; quality of service (packet prioritization/scheduling) plus admission control (rate-limiting senders) can emulate circuits or give statistically bounded delay — but none of this is enabled in multi-tenant datacenters, public clouds, or the internet. The engineering consequence: assume congestion, queueing, and unbounded delays will happen, and pick timeouts experimentally rather than expecting a "correct" constant.

## Examples & Systems
ISDN's 4,000 frames/second circuits; ATM as Ethernet's failed 1980s competitor; InfiniBand; BGP-level bandwidth purchases resembling circuit switching; QoS and admission control; CPU-thread scheduling as the same trade-off in miniature.

## Related
- up: [[Unreliable Networks]] · chapter: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Timeouts and Unbounded Delays]] — sibling: the queueing this design permits
- [[Process Pauses]] — the same static-vs-dynamic trade-off applied to CPUs
- [[Backpressure]] — flow control in packet networks
- [[Describing Performance]] — latency percentiles shaped by these choices
