---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Describing Performance
type: subtopic
tags: [ddia2, percentiles, tail-latency, p99, jitter, histograms]
sources:
  - raw/ch02.md
---
# Average, Median, and Percentiles
> The mean tells you about the system. Percentiles tell you about the users. Report percentiles.

## The Idea
Because response time varies from request to request, it must be treated as a **distribution of values**, not a single number. Most requests are reasonably fast with occasional much slower outliers; variation in network delay specifically is known as **jitter**.

It is common to report the **average** (arithmetic mean) response time. The mean is useful for estimating throughput limits, but it is a poor metric for the "typical" response time, because it doesn't tell you how many users actually experienced that delay.

## How It Works
- Sort response times fastest to slowest. The **median** is the halfway point: a median of 200 ms means half the requests return in under 200 ms and half take longer. This makes it a good answer to "how long do users typically wait." It is also the **50th percentile**, abbreviated **p50**.
- Higher percentiles show how bad the outliers are. The 95th, 99th, and 99.9th are common — **p95**, **p99**, **p999**. A p95 of 1.5 seconds means 95 of 100 requests finish in under 1.5 seconds and 5 of 100 take 1.5 seconds or longer.
- High percentiles are **tail latencies**, and they matter because they directly shape users' experience. Amazon specifies internal service response-time requirements at the **99.9th percentile**, even though that affects only 1 request in 1,000 — because the customers with the slowest requests are often those with the most data on their accounts, having made many purchases. They are the most valuable customers, so keeping the site fast for them matters.
- Amazon judged optimising the **99.99th** percentile (slowest 1 in 10,000) too expensive for insufficient benefit. Very high percentiles are hard to reduce because they are easily affected by random events outside your control, and the returns diminish.

## Trade-offs & Pitfalls
- **Averaging percentiles is mathematically meaningless** — whether to reduce time resolution or to combine data from several machines. The right way to aggregate response-time data is to **add the histograms**. This is one of the most commonly violated rules in real monitoring dashboards.
- Computing percentiles continuously needs care. The simplest implementation keeps every response time in the window and sorts it each minute; if that is too costly, approximation algorithms give good estimates cheaply. Open source libraries: **HdrHistogram, t-digest, OpenHistogram, DDSketch**.
- **The user-impact statistics are less solid than folklore suggests**, and the book takes an unusual amount of space to say so. Google reported in 2006 that slowing search results from 400 ms to 900 ms cost 20% of traffic and revenue — but a 2009 Google study found a 400 ms latency increase produced only 0.6% fewer searches per day, and Bing that year found a two-second load-time increase cut ad revenue by 4.3%. Newer data from these companies appears not to be public. A more recent Akamai study claims 100 ms of added response time cut ecommerce conversion by up to 7%, but the same study shows *very fast* page loads also correlate with lower conversion — explained by the fact that the fastest-loading pages are often those with no useful content, such as 404 pages. Since the study makes no effort to separate content effects from load-time effects, its results are probably not meaningful. The one study the book credits is Yahoo's, which compared click-through rates on fast versus slow search results *while controlling for result quality*, and reported 20–30% more clicks on fast searches when the difference was 1.25 seconds or more.

## Examples & Systems
HdrHistogram, t-digest, OpenHistogram, DDSketch for streaming percentile estimation; Amazon's p999 internal requirement as the canonical tail-latency policy.

## Since the 1st Edition
The percentile material — median, p95/p99/p999, tail latencies, the Amazon p999 rationale, the "don't average percentiles" rule, and the approximation libraries — is largely carried over from the 1st edition's [[Describing Performance]]. What is genuinely new is the **skeptical audit of the latency-versus-revenue statistics**: the 1st edition cited such figures more or less at face value, while the 2nd edition works through which of them survive scrutiny and concludes that most do not.

## Related
- up: [[Describing Performance (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Use of Response Time Metrics (2e)]] — what you do with these numbers once you have them
- [[Latency and Response Time (2e)]] — the quantity being summarised
