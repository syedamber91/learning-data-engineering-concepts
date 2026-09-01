---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
type: chapter-moc
tags: [ddia2, performance, reliability, scalability, maintainability, moc]
sources:
  - raw/ch02.md
---
# Ch 02 – Defining Nonfunctional Requirements
Every application is driven by **functional requirements** — what screens and buttons exist and what each operation does. Alongside them sit **nonfunctional requirements**: that the app be fast, reliable, secure, legally compliant, and easy to maintain. These often go unwritten because they seem obvious, but they matter as much as functionality, since an app that is unbearably slow or unreliable might as well not exist. This chapter takes four of them — performance, reliability, scalability, maintainability — and gives you the vocabulary to state them precisely rather than gesture at them. (Security is acknowledged as important and declared out of scope.) Because abstract definitions are dry, the chapter opens with a concrete case study and keeps returning to it.

## Map
- [[Case Study - Social Network Home Timelines (2e)]] — a Twitter-shaped service used to make performance and scalability concrete
  - [[Representing Users, Posts, and Follows (2e)]] — the naive relational schema and the query that kills it
  - [[Materializing and Updating Timelines (2e)]] — fan-out, materialized views, and the celebrity problem
- [[Describing Performance (2e)]] — response time versus throughput, and why queueing links them
  - [[Latency and Response Time (2e)]] — the book's precise vocabulary: response time, service time, queueing delay, latency
  - [[Average, Median, and Percentiles (2e)]] — why the mean misleads and tail latency matters
  - [[Use of Response Time Metrics (2e)]] — tail latency amplification, SLOs, and SLAs
- [[Reliability and Fault Tolerance (2e)]] — "continuing to work correctly, even when things go wrong"
  - [[Fault Tolerance (2e)]] — faults versus failures, single points of failure, fault injection, chaos engineering
  - [[Hardware and Software Faults (2e)]] — real failure rates, redundancy, and why software faults correlate
  - [[Humans and Reliability (2e)]] — configuration changes as the leading cause of outages, and blameless postmortems
- [[Scalability (2e)]] — the ability to cope with increased load
  - [[Understanding Load (2e)]] — measuring load before arguing about growth
  - [[Shared-Memory, Shared-Disk, and Shared-Nothing Architectures (2e)]] — scaling up versus scaling out
  - [[Principles for Scalability (2e)]] — there is no magic scaling sauce
- [[Maintainability (2e)]] — most of software's cost is after the first release
  - [[Operability - Making Life Easy for Operations (2e)]] — what a data system can do to help its operators
  - [[Simplicity - Managing Complexity (2e)]] — accidental versus essential complexity, and abstraction as the tool
  - [[Evolvability - Making Change Easy (2e)]] — agility at the system level, and minimizing irreversibility

## Chapter Summary
The chapter builds a measuring vocabulary before it builds anything else. **Performance** has two metrics — response time (what the client waits) and throughput (requests or bytes per second) — and they are linked by queueing: response time stays low until throughput nears hardware capacity, then rises sharply. Response time is a *distribution*, so report percentiles rather than a mean; p95, p99, and p999 tail latencies are what users feel, and they amplify when one user request fans out into many backend calls. Percentiles are the raw material of SLOs and SLAs.

**Reliability** means continuing to work correctly when things go wrong, which requires separating a **fault** (one part stops working) from a **failure** (the system stops serving the user). Fault tolerance is always bounded — some number of some types of fault — and is best kept honest by deliberately injecting faults. Hardware faults are frequent enough at scale to be normal operation and are handled by redundancy; software faults are far more dangerous because many nodes run the same code and therefore share bugs. Human factors dominate in practice: configuration changes by operators are the leading cause of outages, and the productive response is blameless postmortems rather than blame.

**Scalability** is not a label a system either has or lacks; it is a set of questions about how load grows and what it costs to keep up. Understand the current load first (throughput plus the statistical shape of it), then choose between vertical scaling / shared-memory, shared-disk, and shared-nothing / horizontal scaling. There is no generic scalable architecture, and it is rarely worth planning more than one order of magnitude ahead. **Maintainability** — where most of software's lifetime cost lives — decomposes into operability, simplicity, and evolvability.

## Since the 1st Edition
This is the 1st edition's opening chapter, rewritten and demoted to second place. Reliability, scalability, and maintainability survive with the same three-way maintainability split ([[Operability - Making Life Easy for Operations]], [[Simplicity - Managing Complexity]], [[Evolvability - Making Change Easy]]). The differences are substantial, though: the Twitter case study has been promoted from an inline example inside "Describing Load" to a full topic with its own subtopics; the fault/failure distinction is stated far more carefully; SLOs and SLAs, metastable failures and retry storms, fault injection and chaos engineering, hardware error rates for SSDs and CPU cores, and the shared-memory/shared-disk/shared-nothing taxonomy are new or greatly expanded; and the Post Office Horizon scandal replaces the 1st edition's gentler framing of why reliability matters. The 1st edition's [[Thinking About Data Systems]] topic has no direct successor — its work is now done by [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]].

## Related
- home: [[Home (2e)]] · previous: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]] · next: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[Ch 09 - The Trouble with Distributed Systems (2e)]] — the faults this chapter names, examined in depth
- [[Ch 07 - Sharding (2e)]] — the main technique behind shared-nothing scaling
- 1st edition: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]] — the chapter this one rewrites
