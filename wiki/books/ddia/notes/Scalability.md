---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
type: topic
tags: [ddia, scalability, load, performance]
sources:
  - raw/ch01.md
---
# Scalability
> Scalability is not a yes/no label but a structured conversation: describe load precisely, measure performance honestly, then choose an architecture that copes when specific load parameters grow.

A system that is reliable today can degrade tomorrow simply because load grew — 10k concurrent users becoming 100k, a million becoming ten million, or data volumes ballooning. Kleppmann's key framing move is that "X is scalable" is a meaningless sentence. Scalability is the *ability to cope with increased load*, and discussing it means answering conditional questions: if the system grows along a particular dimension, what are the options? How much extra resource keeps performance flat? The topic proceeds in three steps that mirror its subtopics: quantify the load, quantify the performance, then reason about architectures — a discipline that underpins [[Partitioning]] and [[Replication]] throughout the rest of the book.

## Subtopics
- [[Describing Load]] — load parameters, and Twitter's fan-out problem as the worked example of choosing the *right* parameter.
- [[Describing Performance]] — throughput vs. response time, why percentiles beat averages, and tail latency's outsized impact.
- [[Approaches for Coping with Load]] — scaling up vs. out, elasticity, stateful vs. stateless distribution, and why there is no one-size-fits-all architecture.

## Key Takeaways
- Never call a system "scalable" in the abstract; name the load parameter and the growth scenario.
- The right load parameter is architecture-specific — requests/sec, read/write ratio, cache hit rate, or something as particular as followers-per-user.
- Measure response time as a distribution (percentiles), never as an average.
- Expect to rethink architecture roughly every order-of-magnitude load increase.
- Scaling decisions embed assumptions about which operations are common; wrong assumptions make scaling effort wasted or counterproductive.

## Related
- chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Reliability]] — growth is a common way reliable systems degrade
- [[Maintainability]] — distributed designs trade simplicity for scale
- [[Partitioning]] — the book's core mechanism for scaling out
- [[Replication]] — companion mechanism for distributing load
