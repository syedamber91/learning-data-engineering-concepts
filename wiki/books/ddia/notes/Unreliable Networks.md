---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
type: topic
tags: [ddia, networking, timeouts, packet-switching]
sources:
  - raw/ch08.md
---
# Unreliable Networks

The systems in this book are shared-nothing: independent machines, each with private memory and disk, that can only cooperate by exchanging messages over a network. That network — the internet, and datacenter Ethernet alike — is an *asynchronous packet network*: it gives no guarantee that a packet will arrive, or when. Send a request and wait for a reply, and any of six things may have happened: the request was lost, the request is queued behind congestion, the remote node crashed, the remote node is temporarily frozen (say, in a garbage-collection pause), the response was lost, or the response is merely delayed. From the sender's seat these cases are indistinguishable — the only observable fact is "no response yet." The standard coping mechanism is the timeout, but a timeout tells you nothing about whether the remote side actually processed your request. This topic works through how often networks actually fail, how faults can (and mostly cannot) be detected, why choosing a timeout is a genuine trade-off with no correct answer, and why packet-switched networks have unbounded delays while circuit-switched telephone networks do not.

## Subtopics
- [[Network Faults in Practice]] — measured fault rates, weird asymmetric failures, and why fault handling must be defined and tested.
- [[Detecting Faults]] — the few explicit failure signals you might get (RST/FIN, ICMP, switch queries) and why none is dependable.
- [[Timeouts and Unbounded Delays]] — the short-vs-long timeout dilemma, queueing as the root of delay variability, and adaptive detectors.
- [[Synchronous Versus Asynchronous Networks]] — circuit switching's bounded delay vs packet switching's bursty-traffic efficiency.

## Key Takeaways
- In an asynchronous network, "no response" is compatible with every possible failure story; you cannot tell which one occurred.
- Network faults are common even inside a single well-run datacenter — software must have defined, tested behavior for them.
- Handling a fault need not mean tolerating it; showing users an error is fine, but undefined behavior (deadlock, data loss) is not.
- Timeout choice trades detection speed against false positives, and false positives can cascade under load.
- Unbounded delay is not a law of nature but the price of packet switching's high utilization for bursty traffic.

## Related
- up: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Faults and Partial Failures]] — the framing this topic instantiates
- [[Handling Node Outages]] — failover decisions that hinge on fault detection
- [[Backpressure]] — TCP flow control as a source of sender-side queueing
- [[Detecting Concurrent Writes]] — what happens when messages race
