---
persona: vutr
kind: concept
sources:
- raw/flink-additional/i-spent-8-hours-understanding-which.md
last_updated: '2026-07-15'
qc: passed
slug: flink-networking-and-flow-control
topics:
- flink
---

Because Flink is distributed, tasks constantly need to exchange data, and TaskManagers own that exchange. When both tasks live on the same TaskManager, the exchange is cheap: the sender serializes data into byte buffers and pushes them onto a queue, and the receiver simply pulls them off and deserializes — no network involved. Remote exchange is where the design gets interesting. Naively, every pair of communicating tasks would need its own TCP connection — 4 tasks on TaskManager A talking to 4 tasks on TaskManager B would be 16 connections — so Flink instead **multiplexes** all traffic between a given pair of TaskManagers onto a single physical TCP channel, regardless of how many individual task-pairs are actually communicating across it.

Records aren't sent one at a time either: they accumulate in a network buffer — 32KB by default, itself a [[flink-memorysegments|MemorySegment]] — before being shipped to the receiving task, which amortizes per-record send overhead the same way most I/O and networking does. But buffering directly works against low latency, so Flink adds **Credit-Based Flow Control** on top: the receiving task tells its sender how many ready-to-receive buffer slots it currently has (its *credit*), and the sender sends data up to that credit limit, tagging what it sends with its own *backlog* — how much more it still has queued to send next. The receiver then uses the backlog information reported by all of its senders to recompute credit allocations, deliberately steering more credit toward the senders reporting the biggest backlogs.

The payoff is twofold: senders can push data the instant a receiver signals it's ready (lower latency, higher throughput than static buffering alone), and if one sender is skewed and falling behind, the receiver notices its outsized backlog and allocates it a larger receiving buffer to help it drain faster — giving more "lane space" to the busiest path so it doesn't become a bottleneck that drags down the whole job's throughput.

*See also: [[apache-flink]] · [[flink-memorysegments]] · [[chandy-lamport-checkpointing]]*
