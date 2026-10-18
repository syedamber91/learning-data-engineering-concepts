---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
type: topic
tags: [ddia2, performance, response-time, throughput, queueing, backpressure]
sources:
  - raw/ch02.md
---
# Describing Performance
Software performance discussions use two main metrics. **Response time** is the elapsed time from when a user makes a request until they receive the answer, measured in seconds, milliseconds, or microseconds. **Throughput** is the number of requests per second, or data volume per second, that the system processes; for a given hardware allocation there is a maximum throughput it can handle, measured in "somethings per second." In the case study, "posts per second" and "timeline writes per second" are throughput metrics; "time to load the home timeline" and "time until a post is delivered to followers" are response-time metrics.

The two are related, and the relationship is **queueing**. A service has low response time when throughput is low, but response time rises as load increases: an arriving request finds the CPU already handling an earlier one and must wait. As throughput approaches the hardware's maximum, queueing delays increase sharply.

Which metric you care about depends on the question. Response time is usually what users care about most; throughput determines the computing resources required (how many servers) and hence the cost of serving a workload. A system is **scalable** if its maximum throughput can be significantly increased by adding computing resources.

## Subtopics
- [[Latency and Response Time (2e)]] — the book's precise definitions, and why queueing delay means you must measure on the client side.
- [[Average, Median, and Percentiles (2e)]] — response time as a distribution; medians, tail latencies, and what the user-impact studies actually show.
- [[Use of Response Time Metrics (2e)]] — tail latency amplification across backend calls, and percentiles inside SLOs and SLAs.

## Key Takeaways
- Response time and throughput are not independent knobs; queueing couples them, and the coupling gets vicious near capacity.
- **When an overloaded system won't recover.** Pushed close to its limit, a system can enter a vicious cycle: long queues raise response times until clients time out and resend, raising the request rate further — a **retry storm**. Even after load drops, the system may stay overloaded until rebooted. This is a **metastable failure**, and it causes serious production outages.
- The defences are named and worth memorising. Client side: increase and randomise the gap between retries (**exponential backoff**), and temporarily stop sending to a service that recently errored or timed out (a **circuit breaker** or token bucket algorithm). Server side: detect approaching overload and proactively reject requests (**load shedding**), or tell clients to slow down (**backpressure**). Queueing and load-balancing algorithm choice matters too.
- If throughput will exceed current hardware capability, capacity must be expanded — which is the handover into [[Scalability (2e)]].

## Since the 1st Edition
The 1st edition's [[Describing Performance]] covered response time, throughput, percentiles, and the queueing explanation. The 2nd edition keeps all of that and adds a substantial new treatment of **overload dynamics**: metastable failure, retry storms, exponential backoff, circuit breakers, token buckets, load shedding, and backpressure. That vocabulary — much of it from the SRE and resilience-engineering literature of the intervening decade — is one of the clearest "this is what we learned since 2017" additions in the book.

## Related
- chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Scalability (2e)]] — what to do when throughput must grow
- [[Timeouts and Unbounded Delays (2e)]] — the distributed-systems view of the same delays
- [[Backpressure (2e)]] — the cross-cutting concept note
- 1st edition: [[Describing Performance]] — the same core, without the overload material
