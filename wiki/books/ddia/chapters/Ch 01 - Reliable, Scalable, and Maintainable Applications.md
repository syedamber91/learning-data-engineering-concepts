---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
type: chapter-moc
tags: [ddia, reliability, scalability, maintainability, moc]
sources:
  - raw/ch01.md
---
# Ch 01 – Reliable, Scalable, and Maintainable Applications

Most modern applications are limited by data — its volume, complexity, and rate of change — rather than by raw CPU. They are assembled from standard building blocks (databases, caches, search indexes, stream and batch processors) whose category boundaries are blurring: Redis doubles as a message queue, [[Apache Kafka]] offers database-grade durability. Once an application stitches several such tools together behind one API, its developers are effectively designing a new data system — and they inherit the data-system designer's questions. This chapter frames the three nonfunctional concerns the whole book keeps returning to: **reliability** (correct operation despite hardware, software, and human faults), **scalability** (sane strategies for growth in load), and **maintainability** (a system that operations, new engineers, and future requirements can all live with). It supplies the vocabulary — faults vs. failures, load parameters, response-time percentiles, operability/simplicity/evolvability — used everywhere else in the book.

## Map
- [[Thinking About Data Systems]] — why databases, queues, and caches belong under one umbrella, and how composing them makes you a data-system designer
- [[Reliability]] — continuing to work correctly when things go wrong; faults vs. failures, fault tolerance over fault prevention
  - [[Hardware Faults]] — disk MTTF math, redundancy (RAID, dual PSUs, generators), and the shift to software fault tolerance on clouds
  - [[Software Errors]] — correlated, systematic faults: bad-input crashes, runaway processes, cascading failures, dormant assumption bugs
  - [[Human Errors]] — config mistakes as the leading outage cause; sandboxes, testing, fast rollback, telemetry
  - [[How Important Is Reliability]] — mundane apps carry real stakes; when cutting corners is a conscious choice
- [[Scalability]] — coping with growth is a question ("if load grows this way, what are our options?"), not a yes/no label
  - [[Describing Load]] — load parameters; Twitter's fan-out problem and its read-path vs. write-path timeline designs
  - [[Describing Performance]] — throughput vs. response time, percentiles over averages, tail latency and its amplification
  - [[Approaches for Coping with Load]] — scaling up vs. out, shared-nothing, elasticity, and why there is no one-size-fits-all architecture
- [[Maintainability]] — most software cost is maintenance; design so the legacy system you create is a pleasant one
  - [[Operability - Making Life Easy for Operations]] — visibility, automation, good defaults, predictable behavior
  - [[Simplicity - Managing Complexity]] — accidental complexity, the big ball of mud, and abstraction as the antidote
  - [[Evolvability - Making Change Easy]] — agility at data-system scale; requirements never stop changing

## Chapter Summary
The chapter separates an application's functional requirements (what it must do) from nonfunctional ones (security, compliance, and the three studied here). *Reliability* means the system keeps doing the right thing even when faults occur — hardware faults being mostly random and independent, software bugs systematic and correlated, and human mistakes inevitable — with fault-tolerance techniques masking certain fault classes from users rather than trying to prevent every fault. *Scalability* means having concrete options when load grows, which first requires describing load quantitatively (load parameters, illustrated by Twitter's home-timeline fan-out) and measuring performance honestly (response-time percentiles rather than means); a scalable system can add capacity to stay reliable under higher load. *Maintainability* is about the humans who live with the system: good abstractions tame complexity and ease change, while good operability means health is visible and manageable. None of the three has a silver-bullet fix, but recurring patterns and techniques get you there — and the rest of the book examines those patterns system by system.

## Related
- part: [[Part I - Foundations of Data Systems]] · home: [[Home]]
- next: [[Ch 02 - Data Models and Query Languages]] — the first layer of design decisions: how data is represented and queried
- [[Ch 08 - The Trouble with Distributed Systems]] — the fault taxonomy introduced here, taken to its distributed extreme
- [[Ch 12 - The Future of Data Systems]] — revisits the Twitter timeline example after the full technical tour
