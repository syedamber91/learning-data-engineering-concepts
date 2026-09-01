---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
topic: Distributed Versus Single-Node Systems
type: subtopic
tags: [ddia2, partial-failure, observability, tracing, latency]
sources:
  - raw/ch01.md
---
# Problems with Distributed Systems
> Every network call can fail in a way that leaves you not knowing whether it happened. That single fact generates most of the cost of distribution.

## The Idea
Every request and API call that crosses the network must handle the possibility of failure: the network may be interrupted, or the service overloaded or crashed, so any request may time out with no response. In that case **you do not know whether the service received the request**, and simply retrying may not be safe. This is the seed of everything in Chapter 9.

## How It Works
- **Latency.** Datacenter networks are fast, but calling another service is still vastly slower than calling a function in the same process. When operating on large volumes of data it can be faster to bring the computation to the machine that already holds the data than to move the data to a separate processing machine.
- **More nodes are not always faster.** A simple single-threaded program on one computer can significantly outperform a cluster with over 100 CPU cores.
- **Troubleshooting is hard.** If the system is slow to respond, locating the problem is genuinely difficult. The techniques developed for this fall under **observability**: collecting data about a system's execution and allowing it to be queried so that both high-level metrics and individual events can be analysed. Tracing tools — OpenTelemetry, Zipkin, Jaeger — let you track which client called which server for which operation, and how long each call took.
- **Consistency across services.** Databases provide mechanisms for consistency within themselves, but when each service owns its own database, keeping data consistent *across* services becomes the application's problem. Distributed transactions are one technique, but they are rarely used in a microservices context: they run counter to the goal of keeping services independent, and many databases don't support them.

## Trade-offs & Pitfalls
- The conclusion the book draws is a recommendation, not just an observation: for all these reasons, performing a task on a single machine is often much simpler and cheaper than setting up a distributed system.
- The retry-safety question ("we don't know whether the service received the request, and simply retrying might not be safe") is the reason idempotence becomes load-bearing later in the book.

## Examples & Systems
OpenTelemetry, Zipkin, and Jaeger for tracing; DuckDB, SQLite, and KùzuDB as the single-node engines that make staying undistributed viable.

## Since the 1st Edition
The problems themselves are the 1st edition's Chapter 8 material, unchanged in substance. What is new is putting the warning *up front* — before any distributed technique is taught — and the observability/tracing toolchain, which the 1st edition did not cover.

## Related
- up: [[Distributed Versus Single-Node Systems (2e)]] · chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Faults and Partial Failures (2e)]] — the full treatment, in Chapter 9
- [[Distributed Transactions (2e)]] — the technique named here and examined in Chapter 8
- [[Observability (2e)]] — the cross-cutting concept note
