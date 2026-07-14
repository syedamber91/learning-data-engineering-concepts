---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Networks
type: subtopic
tags: [ddia, timeouts, queueing, congestion, failure-detection]
sources:
  - raw/ch08.md
---
# Timeouts and Unbounded Delays
> There is no "correct" timeout value: long timeouts mean slow failure detection, short ones mean falsely burying live-but-slow nodes — and packet delays are unbounded because queueing can happen at every hop.

## The Idea
If a timeout is the only dependable fault detector, how long should it be? A long timeout makes users wait through errors while a dead node stays undeclared; a short one detects faults fast but risks declaring a node dead when it merely hit a load spike. A premature declaration is dangerous twice over: the "dead" node may be mid-action (e.g., sending an email), so a takeover performs the action twice; and shifting its responsibilities adds load to already-strained nodes, potentially triggering a cascading failure where, at the extreme, every node declares every other node dead.

## How It Works
In a fantasy network where every packet arrives within bounded time *d* or is lost, and every live node responds within time *r*, the timeout 2d + r would be provably right. Real asynchronous networks offer neither bound. The dominant cause of delay variability is queueing, which stacks up at several layers: switch queues when multiple senders target one port (overflow means drops and resends even though the network is "fine"); the OS queue on a destination whose CPU cores are all busy; virtual-machine monitor buffering while a VM is paused tens of milliseconds so another VM can use the core; and TCP flow control ([[Backpressure]]), which queues data at the sender before it even leaves. TCP also retransmits packets unacknowledged within a timeout derived from observed round-trips — invisible as loss to the application, fully visible as delay. Queueing delays explode near capacity: a lightly loaded system drains queues quickly; a highly utilized one builds long ones fast. In multi-tenant clouds, a noisy neighbor sharing your links, switches, NICs, and CPUs makes delays swing even with no fault anywhere.

## Trade-offs & Pitfalls
Because delay distributions are environment-specific, timeouts can only be chosen experimentally — measure round-trip distributions over time and many machines, then pick your point on the detection-speed vs false-positive curve. Better still, adapt continuously: measure response times and jitter and adjust timeouts automatically, as the Phi Accrual failure detector does (used in Akka and Cassandra); TCP's retransmission timeout works on the same principle. Latency-critical apps like VoIP sidestep TCP entirely: UDP skips retransmission and flow control — delayed audio is worthless, so a lost packet becomes a moment of silence and the retry moves to the human layer.

## Examples & Systems
Phi Accrual detector in Akka and Cassandra; TCP adaptive retransmission; UDP for videoconferencing/VoIP; MapReduce-style batch jobs saturating shared cloud links; the 2d + r thought experiment.

## Related
- up: [[Unreliable Networks]] · chapter: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Backpressure]] — flow control as sender-side queueing
- [[Detecting Faults]] — sibling: signals that precede timeout fallback
- [[Synchronous Versus Asynchronous Networks]] — sibling: why no delay bound exists
- [[Describing Performance]] — percentile thinking behind response-time distributions
