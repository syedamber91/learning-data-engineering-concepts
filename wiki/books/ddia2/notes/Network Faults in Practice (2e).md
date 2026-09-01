---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Networks
type: subtopic
tags: [ddia2, network-faults, netsplit, asymmetric-faults, datacenter]
sources:
  - raw/ch09.md
---
# Network Faults in Practice
> Twelve faults a month in a medium-sized datacenter. Round-trip times of several minutes at high percentiles. And a network interface that drops all inbound packets while sending outbound ones fine.

## The Idea
**We have been building computer networks for decades — one might hope we would have figured out how to make them reliable. We have not yet succeeded.** Systematic studies and plenty of anecdotal evidence show **network problems are surprisingly common, even in controlled environments like a datacenter operated by one company.**

## How It Works
The empirical record the book assembles:
- **One study in a medium-sized datacenter found about 12 network faults per month**, half disconnecting a single machine and half disconnecting an entire rack.
- **Another measured failure rates of top-of-rack switches, aggregation switches, and load balancers**, finding that **adding redundant networking gear doesn't reduce faults as much as you might expect, since it doesn't guard against human error** — misconfigured switches — **which is a major cause of outages.**
- **Interruptions of wide-area fiber links have been blamed on cows, beavers, and sharks** (shark bites have become rarer with better shielding of submarine cables). **Humans are also often at fault**, via accidental misconfiguration, scavenging, or sabotage.
- **Across cloud regions, round-trip times of up to several minutes have been observed at high percentiles.** Even within a single datacenter, **packet delay of more than a minute can occur during a network topology reconfiguration** triggered by a problem during a switch software upgrade. **Thus we have to assume messages might be delayed arbitrarily.**
- **Communications are sometimes partially interrupted**, depending on who you're talking to — **A and B can communicate, and B and C can communicate, but A and C cannot.** Other surprising faults include **a network interface that sometimes drops all inbound packets but sends outbound packets successfully.** **Just because a link works in one direction doesn't guarantee it works in the other.**
- **Even a brief network interruption can have repercussions lasting much longer than the original issue.**

> **Network partitions.** The term *network partition* or *netsplit* is sometimes used when one part of the network is cut off from the rest by a fault. **This is not fundamentally different from other kinds of network interruption.** And network partitions are **not related to sharding of a storage system**, which is sometimes also called partitioning.

## Trade-offs & Pitfalls
- **Even if network faults are rare in your environment, the fact that they can occur means your software must handle them.** Whenever communication happens over a network, **it may fail — there is no way around it.**
- **If error handling of network faults is not defined and tested, arbitrarily bad things could happen** — the cluster could become **deadlocked and permanently unable to serve requests even after the network recovers**, or it could **potentially delete all of your data.** **If software is put in an unanticipated situation, it may do arbitrary unexpected things.**
- **Handling network faults doesn't necessarily mean tolerating them.** If your network is normally fairly reliable, **a valid approach may be to simply show an error message to users** while it misbehaves. **But you do need to know how your software reacts and ensure the system can recover** — and it may make sense to **deliberately trigger network problems and test the response.**

## Examples & Systems
Cows, beavers, and sharks as documented causes of fiber interruptions; asymmetric interfaces that send but don't receive.

## Since the 1st Edition
Close to the 1st edition's [[Network Faults in Practice]] — the same 12-faults-per-month study, the same redundancy-doesn't-help-with-human-error finding, the same sharks, and the same netsplit terminology note. **Updated:** the observation that **shark bites have become rarer with better cable shielding**, and the cross-region high-percentile round-trip figures, which are newer measurements.

## Related
- up: [[Unreliable Networks (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Fault Detection (2e)]] — deciding whether a node is dead given all this
- [[Fault Tolerance (2e)]] — deliberately triggering these problems
- 1st edition: [[Network Faults in Practice]] — the same subtopic
