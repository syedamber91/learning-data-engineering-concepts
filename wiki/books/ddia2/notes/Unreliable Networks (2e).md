---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
type: topic
tags: [ddia2, networks, asynchronous, packet-loss, timeout, shared-nothing]
sources:
  - raw/ch09.md
---
# Unreliable Networks
Older computers such as mainframes were made reliable by **redundancy of components within a single machine** — RAID to survive disk failures. The distributed systems this book focuses on are mostly **shared-nothing**: a bunch of machines connected by a network, using **replication across separate machines** for redundancy instead. **The network is the only way these machines can communicate**: each has its own memory and disk, and **one machine cannot access another's memory or disk except by making requests over the network.** Even with shared storage such as object storage, machines talk to it over the network.

**The internet and most datacenter networks (often Ethernet) are asynchronous packet networks.** One node can send a packet to another, **but the network gives no guarantees as to when it will arrive or whether it will arrive at all.** If you send a request expecting a response, six things could go wrong:
- **Your request may have been lost** — perhaps someone unplugged a network cable.
- **Your request may be waiting in a queue** and delivered later — perhaps the network or recipient is overloaded.
- **The remote node may have failed** — crashed or powered down.
- **The remote node may have temporarily stopped responding** — perhaps a long GC pause — but will respond again later.
- **The remote node processed your request, but the response was lost** — perhaps a misconfigured switch.
- **The remote node processed your request, but the response was delayed** and will be delivered later.

## Subtopics
- [[The Limitations of TCP (2e)]] — what "reliable delivery" does and does not buy you.
- [[Network Faults in Practice (2e)]] — the empirical record of how often and how strangely networks fail.
- [[Fault Detection (2e)]] — automatically deciding a node is dead, and the few explicit signals available.
- [[Timeouts and Unbounded Delays (2e)]] — choosing the timeout, and queueing as the source of variability.
- [[Synchronous Versus Asynchronous Networks (2e)]] — why we can't just make the network deliver on time.

## Key Takeaways
- **The sender can't even tell whether the packet was delivered.** The only option is for the recipient to send a response, **which may in turn be lost or delayed.**
- **These issues are indistinguishable in an asynchronous network**: the only information you have is that you haven't received a response yet. **If you send a request and don't receive a response, it is impossible to tell why.**
- **The usual way of handling this is a timeout**: after some time you give up and assume no response is coming. **But when a timeout occurs you still don't know whether the remote node got your request** — and if it is still queued somewhere, **it may still be delivered even though you've given up on it.**
- That last point is what makes retries dangerous and idempotence necessary throughout the rest of the book.

## Since the 1st Edition
The 1st edition's [[Unreliable Networks]] listed essentially the same six failure modes and made the same "indistinguishable, so use a timeout" argument. **The structural change is the addition of [[The Limitations of TCP (2e)]] as a first subtopic** — the 1st edition assumed the reader knew what TCP guarantees and moved straight to network faults in practice.

## Related
- chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Unreliable Clocks (2e)]] — the second source of uncertainty
- [[Shared-Memory, Shared-Disk, and Shared-Nothing Architectures (2e)]] — why the network is the only channel
- 1st edition: [[Unreliable Networks]] — the same topic
