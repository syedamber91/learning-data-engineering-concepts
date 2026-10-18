---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Networks
type: subtopic
tags: [ddia2, timeout, queueing, congestion, jitter, phi-accrual, udp]
sources:
  - raw/ch09.md
---
# Timeouts and Unbounded Delays
> How long should the timeout be? There is no simple answer — and the reason variability is so wide is queueing, at five different points in the path.

## The Idea
**A long timeout means a long wait until a node is declared dead**, during which users may wait or see errors. **A short timeout detects faults faster but carries a higher risk of incorrectly declaring a node dead** when it has only suffered a temporary slowdown from a load spike.

**Prematurely declaring a node dead is problematic.** If the node is actually alive and in the middle of an action — sending an email, say — **and another node takes over, the action may end up being performed twice.**

**And when a node is declared dead, its responsibilities transfer to other nodes, placing additional load on them and the network.** If the system is already struggling, **declaring nodes dead prematurely makes the problem worse.** In particular, **the node may not have been dead but only slow because of overload; transferring its load elsewhere can cause a cascading failure** — in the extreme, **all nodes declare each other dead and everything stops working.**

**Imagine a fictitious system** where every packet is either delivered within time *d* or lost, and a non-failed node always handles a request within time *r*. Then **every successful request receives a response within 2d + r**, and no response within that time means the network or node is broken — **so 2d + r would be a reasonable timeout.**

**Unfortunately, most systems have neither guarantee.** **Asynchronous networks have unbounded delays** — they try to deliver packets as quickly as possible, **but there is no upper limit on how long a packet may take** — and **most server implementations cannot guarantee handling requests within a maximum time.** **For failure detection, it's not sufficient for the system to be fast most of the time: if your timeout is low, it takes only a transient spike in round-trip times to throw the system off balance.**

## How It Works
**Network congestion and queueing.** Like traffic on roads, **the variability of packet delays is most often due to queueing**, at five points:
- **If several nodes simultaneously send to the same destination, the switch must queue them** and feed them into the destination link one by one. On a busy link a packet waits for a slot — **network congestion** — **and if the switch queue fills up the packet is dropped and must be resent, even though the network is functioning fine.**
- **At the destination machine, if all CPU cores or application threads are busy, the incoming request is queued by the OS** until the application is ready. **Depending on load this may take an arbitrary length of time.**
- **In virtualized environments, an OS is often paused for tens of milliseconds while another VM uses a CPU core.** During this time the VM can't consume data from the network, so **incoming data is buffered by the VM monitor**, further increasing variability.
- **TCP limits its own send rate to avoid overloading the network**, meaning **additional queueing at the sender before data even enters the network.**
- **When TCP retransmits a lost packet, the application doesn't see the loss directly but does see the resulting delay** — waiting for the timeout, then for the retransmitted packet to be acknowledged.

> **TCP versus UDP.** Some latency-sensitive applications — videoconferencing, VoIP — **use UDP rather than TCP**, trading reliability for lower delay variability: **UDP does no flow control and doesn't retransmit lost packets**, avoiding some causes of variable delay (though still susceptible to switch queues and scheduling delays). **UDP is a good choice when delayed data is worthless**: in a VoIP call there isn't time to retransmit a lost packet before its audio is due, **so the application fills the missing slot with silence and moves on. The retry happens at the human layer instead** — "Could you repeat that please? The sound just cut out."

**Variability of network delays.** **Queueing delays have an especially wide range when a system is close to maximum capacity.** A system with plenty of spare capacity easily drains queues; **in a highly utilized system, long queues build up very quickly.**

**In public clouds and multitenant datacenters, resources are shared among many customers** — network links, switches, and even each machine's network interface and CPUs when on VMs. **Because you have no control over or insight into other customers' usage, network delays can be highly variable if a noisy neighbor is using a lot of resources.**

## Trade-offs & Pitfalls
- **In such environments you can choose timeouts only experimentally**: measure the distribution of round-trip times over an extended period and over many machines to determine the expected variability, then **trade off failure-detection delay against risk of premature timeouts** given your application's characteristics.
- **Better still, don't use constant timeouts at all.** Systems can **continually measure response times and their variability (jitter) and automatically adjust timeouts** to the observed distribution. **The Phi Accrual failure detector** — used in **Akka and Cassandra** — is one way; **TCP retransmission timeouts work similarly.**

## Examples & Systems
Phi Accrual failure detector (Akka, Cassandra); TCP retransmission timeouts; UDP for VoIP and videoconferencing.

## Since the 1st Edition
Very close to the 1st edition's [[Timeouts and Unbounded Delays]] — the same 2d + r thought experiment, the same five queueing sources, the same TCP-versus-UDP box, and the same Phi Accrual recommendation. **Added:** the **noisy neighbor** framing for multitenant clouds, stated more explicitly than in the 1st edition.

## Related
- up: [[Unreliable Networks (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Synchronous Versus Asynchronous Networks (2e)]] — why unbounded delay is a design choice
- [[Describing Performance (2e)]] — retry storms and metastable failure
- [[Process Pauses (2e)]] — the same problem inside the process
- 1st edition: [[Timeouts and Unbounded Delays]] — the same subtopic
