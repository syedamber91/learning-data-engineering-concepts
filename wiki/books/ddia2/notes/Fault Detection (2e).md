---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Networks
type: subtopic
tags: [ddia2, failure-detection, timeout, icmp, false-positive]
sources:
  - raw/ch09.md
---
# Fault Detection
> There are four ways the system might explicitly tell you a node is down. You can't count on any of them, so you end up with a timeout anyway.

## The Idea
**Many systems need to automatically detect faulty nodes.** A **load balancer** must stop sending requests to a dead node; a **single-leader database** must promote a follower when the leader fails. **Unfortunately, uncertainty about the network makes it difficult to tell whether a node is working.**

## How It Works
**In specific circumstances you might get explicit feedback:**
- **If you can reach the machine but no process is listening on the destination port** — because the process crashed — **the operating system will helpfully close or refuse TCP connections by sending an RST or FIN packet.**
- **If a node process crashed but the node's OS is still running, a script can notify other nodes** so another can take over quickly **without waiting for a timeout to expire.** **HBase does this.**
- **If you have access to the management interface of your datacenter's network switches, you can query them to detect link failures at a hardware level** — for example if the remote machine is powered down. **Ruled out if you're connecting via the internet, in a shared datacenter with no switch access, or if a network problem blocks the management interface.**
- **If a router is sure the IP address is unreachable, it may reply with an ICMP Destination Unreachable packet.** **But the router doesn't have a magic failure detection capability either; it is subject to the same limitations as other participants.**

## Trade-offs & Pitfalls
- **Rapid feedback about a remote node being down is useful, but you can't count on it.** You may get an error response at some level of the stack, **but in general you have to assume you will get no response at all.** So: **retry a few times, wait for a timeout, and eventually declare the node dead.**
- **Since the node could actually be alive, you must strike a balance between false positives and false negatives**: **too short a timeout causes alive nodes to be incorrectly suspected dead; too long a timeout causes unnecessary delays waiting for dead nodes.**
- The four explicit signals are worth knowing precisely because **each one narrows the uncertainty in a specific case** — but none covers the general case, which is why the next subtopic is entirely about choosing a timeout.

## Examples & Systems
TCP RST/FIN on a closed port; HBase's crash-notification script; switch management interfaces; ICMP Destination Unreachable.

## Since the 1st Edition
Essentially unchanged from the 1st edition's treatment inside [[Unreliable Networks]], where it appeared as a "Detecting faults" section rather than a named subtopic. The four signals and the false-positive/false-negative balance are the same; the 2nd edition promotes it to its own subtopic.

## Related
- up: [[Unreliable Networks (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Timeouts and Unbounded Delays (2e)]] — the fallback you always end up using
- [[Handling Node Outages (2e)]] — what happens once you declare a leader dead
- [[Single-Leader Versus Leaderless Replication Performance (2e)]] — the architecture that avoids the decision
