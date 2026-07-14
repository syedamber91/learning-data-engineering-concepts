---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Networks
type: subtopic
tags: [ddia, failure-detection, timeouts, tcp]
sources:
  - raw/ch08.md
---
# Detecting Faults
> Systems must notice dead nodes — to take them out of a load balancer or promote a new leader — but the network's uncertainty means no detection signal is fully trustworthy except a positive reply from the application itself.

## The Idea
Automatic fault detection is a prerequisite for automatic recovery: a load balancer must stop routing to a dead node, and in single-leader replication a follower must be promoted when the leader dies (see [[Handling Node Outages]] and [[Leader Election]]). The catch is that network uncertainty makes "is that node up?" fundamentally hard to answer.

## How It Works
In lucky cases you get explicit negative feedback:
- If the target machine is reachable but no process listens on the port (the process crashed), the OS closes or refuses the TCP connection with an RST or FIN packet. But if the node crashed *mid-request*, this tells you nothing about how much it processed.
- If the process died but the OS survives, a script can proactively tell peers, letting another node take over without waiting out a timeout — HBase has done this.
- With access to datacenter switch management interfaces, you can query for hardware-level link failure (e.g., machine powered off). Unavailable over the internet, in shared datacenters, or when the network problem blocks the management path itself.
- A router that knows an IP is unreachable may answer with an ICMP Destination Unreachable packet — but routers have no magic detection powers either.

## Trade-offs & Pitfalls
None of these signals is reliable, and their absence proves nothing. Even a TCP acknowledgment only confirms the kernel got the packet — the application may have crashed before acting on it. The only proof that a request succeeded is a positive response from the application. The wrong engineering assumption is treating any transport-level signal as an application-level guarantee. In the general case you must assume you may hear nothing at all: retry a few times (TCP retries transparently; you can also retry at the application layer), wait out a timeout, and only then declare the node dead — which raises the question of how long that timeout should be (see [[Timeouts and Unbounded Delays]]).

## Examples & Systems
HBase's crash-notification scripts; RST/FIN behavior of TCP stacks; ICMP Destination Unreachable; switch management interfaces in owned datacenters versus their absence in shared or internet-connected environments.

## Related
- up: [[Unreliable Networks]] · chapter: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Handling Node Outages]] — failover flows that consume these detection signals
- [[Leader Election]] — promotion triggered by detected leader death
- [[Timeouts and Unbounded Delays]] — sibling: sizing the timeout fallback
- [[The Truth Is Defined by the Majority]] — who gets to decide a node is dead
