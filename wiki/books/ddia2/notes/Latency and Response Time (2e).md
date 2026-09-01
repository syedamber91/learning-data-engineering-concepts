---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Describing Performance
type: subtopic
tags: [ddia2, latency, response-time, queueing-delay, head-of-line-blocking]
sources:
  - raw/ch02.md
---
# Latency and Response Time
> "Latency" and "response time" get used interchangeably in the wild. The book refuses to, and the distinction pays off immediately.

## The Idea
Four terms, used precisely throughout the book:
- **Response time** is what the client sees. It includes all delays incurred anywhere in the system.
- **Service time** is the duration for which the service is actively processing the request.
- **Queueing delay** can occur at several points: after a request is received it may wait for a CPU to become available; a response packet may be buffered before transmission if other tasks on the same machine are saturating the outbound network interface.
- **Latency** is a catchall for time during which a request is *not being actively processed* — that is, during which it is latent. **Network latency** (or network delay) specifically means time a request and response spend travelling through the network.

## How It Works
- Response time varies significantly from one request to the next even when you repeat the identical request. Many things add random delay: a context switch to a background process, a lost network packet and TCP retransmission, a garbage collection pause, a page fault forcing a disk read, or mechanical vibrations in the server rack.
- **Queueing delays often account for a large part of that variability.** A server processes only a small number of things in parallel — limited, for instance, by CPU core count — so it takes only a few slow requests to hold up everything behind them. This is **head-of-line blocking**: subsequent requests may have fast service times, but the client still sees a slow response because it waited for the request in front.
- The book draws the operational conclusion sharply: **queueing delay is not part of service time, and for that reason it is important to measure response times on the client side.** A server measuring its own service time will report that everything is fine while clients are timing out.

## Trade-offs & Pitfalls
- Measuring on the server is the classic self-deception. Server-side timing excludes exactly the delay that head-of-line blocking creates.
- Treating a single measured response time as "the" response time ignores that it is a distribution — the subject of the next subtopic.

## Examples & Systems
The book's request/response timing diagram (nodes as horizontal lines, messages as diagonal arrows) is introduced here and reused throughout the book.

## Since the 1st Edition
Present in the 1st edition's [[Describing Performance]] in less structured form. The 2nd edition splits it into its own subtopic, adds **service time** as a named term distinct from response time, and adds head-of-line blocking explicitly — the 1st edition described the effect but did not name it here.

## Related
- up: [[Describing Performance (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Average, Median, and Percentiles (2e)]] — how to summarise a distribution of these
- [[Timeouts and Unbounded Delays (2e)]] — the same delays as a distributed-systems hazard
- [[Process Pauses (2e)]] — garbage collection pauses, one of the named random-delay sources
