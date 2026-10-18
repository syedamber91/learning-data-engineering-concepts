---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Networks
type: subtopic
tags: [ddia2, circuit-switching, packet-switching, bounded-delay, utilization, isdn]
sources:
  - raw/ch09.md
---
# Synchronous Versus Asynchronous Networks
> The telephone network delivers audio with bounded delay because it reserves bandwidth. Datacenter networks don't, because bursty traffic makes reservation wasteful. Variable delay is a cost/benefit trade-off, not a law of nature.

## The Idea
**Distributed systems would be a lot simpler if the network delivered packets with a fixed maximum delay and never dropped them. Why can't we solve this at the hardware level?**

Compare datacenter networks to the **traditional fixed-line telephone network**, which is **extremely reliable** — delayed audio frames and dropped calls are very rare. **A phone call requires constantly low end-to-end latency and enough bandwidth to carry your voice.**

**When you make a call, the network establishes a circuit**: a **fixed, guaranteed amount of bandwidth allocated for the call along the entire route**, remaining in place until the call ends. **An ISDN network runs at a fixed 4,000 frames per second**, and an established call is **allocated 16 bits within each frame in each direction** — so each side is **guaranteed to send exactly 16 bits of audio every 250 microseconds.**

**This kind of network is synchronous**: even passing through several routers, **data does not suffer from queueing, because the 16 bits for the call have already been reserved at the next hop.** **And because there is no queueing, the maximum end-to-end latency is fixed — a bounded delay.**

## How It Works
**A circuit is very different from a TCP connection.** **A circuit has a fixed amount of reserved bandwidth nobody else can use while it is established**, whereas **TCP packets opportunistically use whatever bandwidth is available.** Give TCP a variable-sized block of data — an email, a web page — **and it will try to transfer it as quickly as possible; while idle, a TCP connection uses no bandwidth** except perhaps an occasional keepalive.

**If datacenter networks and the internet were circuit-switched, a guaranteed maximum round-trip time could be established at circuit setup. But they are not.** **Ethernet and IP are packet-switched protocols, which suffer from queueing and thus unbounded delays**, and **have no concept of a circuit.**

**Why packet switching? Because they are optimized for bursty traffic.** A circuit is good for an audio or video call needing a fairly constant bit rate. **Requesting a web page, sending an email, or transferring a file has no particular bandwidth requirement — we just want it to complete as quickly as possible.** **Transferring a file over a circuit would require guessing a bandwidth allocation**: **guess too low and the transfer is unnecessarily slow, leaving capacity unused; guess too high and the circuit cannot be set up at all**, since the network can't allow a circuit whose allocation it can't guarantee. **By contrast, TCP dynamically adapts to available capacity.**

## Trade-offs & Pitfalls
**Latency and resource utilization.** **Variable delays are a consequence of dynamic resource partitioning.** A wire between two telephone switches carrying up to 10,000 simultaneous calls **divides the resource statically**: **even if you are the only call and all 9,999 other slots are unused, your circuit still gets the same fixed bandwidth as when the wire is full.**

**The internet shares bandwidth dynamically.** Senders **push and jostle to get their packets over the wire as quickly as possible**, and switches decide moment to moment which packet to send. **The downside is queueing; the advantage is that it maximizes utilization of the wire.** **The wire has a fixed cost, so better utilization makes each byte cheaper.**

**The same applies to CPUs.** Sharing a core dynamically among threads means **a thread sometimes waits in the run queue and can be paused for varying lengths of time** — **but this utilizes the hardware better than allocating a static number of cycles to each thread.** **Better hardware utilization is also why cloud platforms run several customers' VMs on the same physical machine.**

**The conclusion the book draws is important:** **latency guarantees are achievable in certain environments, if resources are statically partitioned** — dedicated hardware, exclusive bandwidth allocations — **but these guarantees come at the cost of reduced utilization, i.e., they are more expensive.** **Multitenancy with dynamic partitioning gives better utilization and is cheaper, at the cost of variable delays.** **Variable delays in networks are not a law of nature but simply the result of a cost/benefit trade-off.**

## Examples & Systems
ISDN circuits at 4,000 frames/second with 16 bits per call; Ethernet and IP as packet-switched protocols.

## Since the 1st Edition
Close to the 1st edition's [[Synchronous Versus Asynchronous Networks]] — the same ISDN circuit explanation, the same bursty-traffic argument, and the same latency-versus-utilization box. **Compressed:** the 1st edition included a longer discussion of hybrid approaches combining circuit and packet switching (ATM, InfiniBand, quality-of-service and admission control), which the 2nd edition trims to a brief mention.

## Related
- up: [[Unreliable Networks (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Timeouts and Unbounded Delays (2e)]] — the consequence of packet switching
- [[Cloud Computing Versus Supercomputing (2e)]] — HPC's specialised interconnects
- 1st edition: [[Synchronous Versus Asynchronous Networks]] — the same subtopic
