---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Describing Performance
type: subtopic
tags: [ddia2, slo, sla, tail-latency-amplification, monitoring]
sources:
  - raw/ch02.md
---
# Use of Response Time Metrics
> One slow backend call is enough to make a whole user request slow — and the more calls you make, the more likely you are to hit one.

## The Idea
High percentiles matter most in backend services that are called multiple times while serving a single end-user request. Even when the calls are made in parallel, the request still waits for the slowest of them. It takes just one slow call to make the entire end-user request slow.

## How It Works
- **Tail latency amplification.** Even if only a small percentage of backend calls are slow, the chance of *hitting* a slow call rises with the number of backend calls an end-user request requires — so a higher proportion of end-user requests end up slow than the per-call percentile would suggest. A p99 backend, called ten times per user request, does not give you a p99 user experience.
- **SLOs and SLAs.** Percentiles are the usual currency for defining expected performance and availability. A **service level objective (SLO)** might target a median response time under 200 ms, a 99th percentile under 1 second, and at least 99.9% of valid requests resulting in non-error responses. A **service level agreement (SLA)** is a contract specifying what happens if the SLO is not met — for example, customers becoming entitled to a refund.

## Trade-offs & Pitfalls
- The book is careful not to oversell this: that is the basic idea "at least," and in practice **defining good availability metrics for SLOs and SLAs is not straightforward**. What counts as a "valid request," what counts as an error, and over what window, are all genuinely contested.
- Tail latency amplification argues against gratuitous service decomposition: every extra backend hop on the critical path multiplies your exposure to the tail. This is a direct tension with the microservices argument in [[Microservices and Serverless (2e)]].

## Examples & Systems
An SLO of "p50 < 200 ms, p99 < 1 s, ≥99.9% non-error responses" as the book's worked example of the form.

## Since the 1st Edition
Tail latency amplification appeared in the 1st edition. **SLOs and SLAs are treated far more seriously here** — the 1st edition mentioned SLAs briefly; the 2nd edition separates objective from agreement, gives a concrete SLO shape, and adds the honest caveat that defining availability metrics well is hard.

## Related
- up: [[Describing Performance (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Fault Tolerance (2e)]] — a failure is defined as no longer meeting the SLO
- [[Microservices and Serverless (2e)]] — the architecture that makes amplification worse
- [[Average, Median, and Percentiles (2e)]] — where these numbers come from
