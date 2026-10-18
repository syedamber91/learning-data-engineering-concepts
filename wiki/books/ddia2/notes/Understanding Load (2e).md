---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Scalability
type: subtopic
tags: [ddia2, load-parameters, throughput, linear-scalability]
sources:
  - raw/ch02.md
---
# Understanding Load
> You cannot answer "what happens if our load doubles?" until you can say what your load *is*. Most scalability arguments are really arguments about undefined units.

## The Idea
First you need a clear understanding of the current load on the system; only then can you discuss growth questions. Load is often a measure of **throughput** — requests per second to a service, gigabytes of new data arriving per day, shopping cart checkouts per hour. Sometimes what matters is the **peak** of a variable quantity, such as the number of simultaneously online users in the social network case study.

## How It Works
Other statistical characteristics of the load often affect access patterns, and therefore scalability requirements. Examples the book gives:
- The **ratio of reads to writes** in a database.
- The **hit rate** on a cache.
- The **number of data items per user** — followers, in the case study.

Perhaps the average case is what matters for you; perhaps your bottleneck is dominated by a small number of extreme cases. It depends entirely on the details of the application. (The case study is the worked example: the average of 200 followers is nearly irrelevant next to the celebrity with 100 million.)

Once load is understood, examine what happens when it increases, in two directions:
1. Increase load in a certain way and hold resources (CPUs, memory, network bandwidth) unchanged — how is performance affected?
2. Increase load in a certain way — how much must resources increase to keep performance unchanged?

The goal is usually to keep performance within SLA requirements while minimising running cost. **Linear scalability** means doubling resources handles twice the load at the same performance. Sublinear cost growth is occasionally possible through economies of scale or better distribution of peak load; superlinear cost growth is much more likely, for reasons such as a single write request involving more work when the dataset is large, even if the request size is identical.

## Trade-offs & Pitfalls
- Choosing the wrong load parameter is the failure mode. "Requests per second" hides the fan-out that actually dominates cost in the timeline example.
- Averages hide tails, and in load characterisation the tail is frequently the bottleneck.

## Examples & Systems
Requests per second, GB/day ingested, checkouts per hour, peak concurrent online users, read/write ratio, cache hit rate, items per user.

## Since the 1st Edition
This is the 1st edition's [[Describing Load]] renamed and slimmed. The Twitter example that dominated the 1st-edition version has been promoted out into [[Case Study - Social Network Home Timelines (2e)]], leaving this subtopic to state the general method. The two framings of the growth question and the linear/superlinear cost discussion carry over largely intact.

## Related
- up: [[Scalability (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Case Study - Social Network Home Timelines (2e)]] — load characterisation worked through in full
- [[Describing Performance (2e)]] — the performance side of the same measurement
- 1st edition: [[Describing Load]] — the same subtopic under its old name
