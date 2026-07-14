---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
topic: Scalability
type: subtopic
tags: [ddia, percentiles, tail-latency, response-time, slo-sla]
sources:
  - raw/ch01.md
---
# Describing Performance
> Response time is a distribution, not a number — percentiles (p50/p95/p99/p999) expose the tail latencies that averages hide and that your most valuable users actually feel.

## The Idea
With load described, two questions follow: if a load parameter grows and resources stay fixed, what happens to performance? And how much resource keeps performance unchanged? Both need honest performance metrics. Batch systems like [[Hadoop]] care about *throughput* (records/sec, or total job time — ideally dataset size ÷ throughput, though skew and straggler tasks stretch it in practice). Online systems care about *response time*: the gap between a client sending a request and receiving the reply. A precise distinction: **response time** is what the client experiences (service time + network + queueing delays); **latency** is strictly the time a request spends *waiting* to be handled.

## How It Works
Identical requests return different times on every attempt — context switches, TCP retransmits after packet loss, GC pauses, page faults hitting disk, even rack vibration. So treat response time as a distribution. The **mean** is a poor "typical" figure because it says nothing about how many users saw a given delay. Use **percentiles**: the **median (p50)** — half of requests faster, half slower — is the honest typical-user number (per request, though: a user making several requests very likely hits something slower than the median). Outliers show up at **p95, p99, p999**: the thresholds below which 95%, 99%, 99.9% of requests complete. If p95 = 1.5s, 5 in 100 requests take at least that long.

High percentiles — *tail latencies* — matter commercially. Amazon specifies internal SLAs at p999 (1 in 1,000 requests) because the slowest requests belong to the customers with the most data — the biggest purchasers, i.e. the most valuable users. Amazon measured that +100ms of response time cuts sales by 1%; elsewhere a 1-second slowdown cut a satisfaction metric by 16%. Yet p9999 was judged too costly to chase — random uncontrollable events dominate there and returns diminish. Percentiles also anchor **SLOs/SLAs**: e.g. "up" means median < 200ms and p99 < 1s, met ≥99.9% of the time, with refunds when breached.

## Trade-offs & Pitfalls
- **Queueing dominates the tail**: a server processes few things in parallel (CPU-core bound), so a few slow requests block those behind them — *head-of-line blocking*. Measure client-side, since server-side numbers miss the waiting.
- **Load testing**: the generator must fire requests independently of responses; waiting for each reply before the next artificially shortens queues and flatters results.
- **Tail latency amplification**: one user request fanned into many parallel backend calls waits for the *slowest* — so slow backend calls, even if rare, hit a much higher share of end-user requests.
- **Never average percentiles** when aggregating across machines or time — it's mathematically meaningless; add histograms instead. Rolling-window percentile monitoring can use approximation algorithms: forward decay, t-digest, HdrHistogram.

## Related
- up: [[Scalability]] · chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Describing Load]] — the load parameters these metrics respond to
- [[Approaches for Coping with Load]] — architecture choices these numbers drive
- [[Timeouts and Unbounded Delays]] — Ch 8 on variable delay in distributed systems
