---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
topic: Distributed Versus Single-Node Systems
type: subtopic
tags: [ddia2, microservices, soa, serverless, faas, api-evolution]
sources:
  - raw/ch01.md
---
# Microservices and Serverless
> Microservices are primarily a technical solution to a people problem — letting teams make progress without coordinating. Judge them by that, not by their technical elegance.

## The Idea
The most common way of distributing a system is to split it into clients and servers and have clients make requests, most often over HTTP. The same process is frequently both: a server for incoming requests and a client for outbound ones. This style was traditionally called **service-oriented architecture (SOA)** and was later refined into **microservices**: each service has one well-defined purpose (S3's is file storage), exposes an API callable over the network, and has one team responsible for maintaining it. A complex application decomposes into interacting services, each owned by a separate team. Cloud native systems lean on this heavily, but on-premises systems can be service-oriented too.

## How It Works
**Advantages.** Each service can be updated independently, reducing cross-team coordination; each can be given the hardware resources it needs; and hiding implementation behind an API lets owners change the implementation without affecting clients. For storage, it is common for each service to have **its own database** and not share. Sharing a database would effectively make the database structure part of the service's API — and therefore hard to change — and one service's queries could hurt another's performance.

**Serverless / function as a service (FaaS)** outsources infrastructure management to the vendor. With VMs you explicitly choose when to start and stop an instance; with serverless the provider allocates and frees hardware automatically based on incoming requests. Just as cloud storage replaced capacity planning with metered billing, serverless brings metered billing to code execution: you pay for the time your code runs rather than provisioning in advance.

## Trade-offs & Pitfalls
- **Many services breed complexity.** Testing one during development is complicated because you also need to run everything it depends on. Each service needs infrastructure for deploying releases, adjusting hardware to load, collecting logs, monitoring health, and paging an on-call engineer. Orchestration frameworks like Kubernetes became popular because they provide a foundation for exactly this.
- **API evolution is hard.** Clients expect certain fields; adding or removing fields as business needs change can break them, and such failures are often not discovered until late — when the updated API reaches staging or production. API description standards such as OpenAPI and gRPC help manage the client/server relationship.
- **Scale sensitivity.** Because microservices solve a coordination problem, they are valuable in a large company and likely unnecessary overhead in a small one with few teams, where the simplest possible implementation is preferable.
- **Serverless limits.** Providers commonly impose a time limit on function execution and restrict runtime environments, and services can suffer slow start times on first invocation. The name is also misleading: each execution still runs on a server, just possibly a different one next time. Infrastructure services such as BigQuery and various Kafka offerings have adopted "serverless" language simply to signal autoscaling and usage-based billing.

## Examples & Systems
S3 as a single-purpose service; Kubernetes for orchestration; OpenAPI and gRPC for API description; BigQuery and managed Kafka as services using "serverless" to mean autoscaling plus metered billing.

## Since the 1st Edition
New. The 1st edition discussed service-oriented dataflow in its encoding chapter ([[Dataflow Through Services - REST and RPC]]) but did not treat microservices as an architectural choice with a people-problem justification, and serverless did not appear at all.

## Related
- up: [[Distributed Versus Single-Node Systems (2e)]] · chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Dataflow Through Services - REST and RPC (2e)]] — the encoding-level view of service calls
- [[Durable Execution and Workflows (2e)]] — what serverless functions grow into when they need reliability
- [[Problems with Distributed Systems (2e)]] — the costs this architecture signs you up for
