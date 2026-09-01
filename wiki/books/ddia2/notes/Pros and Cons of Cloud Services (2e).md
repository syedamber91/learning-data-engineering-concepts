---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
topic: Cloud Versus Self-Hosting
type: subtopic
tags: [ddia2, cloud, elasticity, vendor-lock-in, cost]
sources:
  - raw/ch01.md
---
# Pros and Cons of Cloud Services
> Using a cloud service outsources the *operation* of software. Whether that saves money depends on your skills and your load curve; what it definitely costs you is control.

## The Idea
Cloud providers claim their services save time and money and let you move faster than setting up your own infrastructure. The book's position is that this is true under specific conditions and false under others, and that the conditions are knowable in advance.

## How It Works
**When self-hosting wins.** If you already have experience setting up and operating the systems you need, *and* your load is fairly predictable (the machine count doesn't fluctuate wildly), it is often cheaper to buy your own machines and run the software yourself.

**When the cloud wins.**
- If you need a system you don't already know how to deploy and operate, adopting a service is usually easier and quicker than learning to manage it — hiring and training staff specifically to run it gets very expensive. You still need an operations team in the cloud, but outsourcing basic system administration frees the team for higher-level concerns.
- A specialist provider running the same service for many customers accumulates operational expertise you cannot match. (The counterweight: if you run it, you can tune it for *your* workload, and a cloud service is unlikely to make such customisations for you.)
- **Variable load** is the strongest case. Provisioning for peak load leaves resources idle most of the time, which is exactly what makes a system cost-ineffective. Analytical systems are the canonical example: a large query needs a lot of parallel compute, then those resources sit idle until the next query. Predefined queries (daily reports) can be enqueued and scheduled to smooth the load, but interactive queries get *more* variable the faster you want them to finish. For a dataset large enough that fast querying needs significant compute, returning unused resources to the provider saves real money. For smaller datasets the difference is less significant.

## Trade-offs & Pitfalls
The book's blunt summary is that the biggest downside is having **no control**, and it enumerates six failure modes:
- A missing feature: all you can do is politely ask the vendor; you generally cannot implement it yourself.
- An outage: all you can do is wait for recovery.
- A bug or performance problem you trigger: diagnosis is hard, because you lack the OS-level metrics, debugging information, and server logs you would have when running the software yourself.
- Shutdown, price rises, or unwelcome product changes: continuing to run an old version is usually not an option, so you are forced to migrate. Compatible APIs mitigate this, but many cloud services have no standard API, which raises switching cost and makes **vendor lock-in** a real problem.
- **Geopolitics**: if the provider is in another country and a political conflict arises, sanctions can lock you out.
- **Trust**: the provider must be trusted to keep data secure, which complicates compliance with privacy and security regulations.

Despite all of this, building new applications on cloud services — or a hybrid approach using cloud for some parts — has become steadily more popular.

## Examples & Systems
Analytical query workloads as the archetypal spiky load; high-frequency trading as the archetypal workload that must stay in-house because it requires full control of the hardware.

## Since the 1st Edition
New. The 1st edition contained no cost/control analysis of cloud services.

## Related
- up: [[Cloud Versus Self-Hosting (2e)]] · chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Operations in the Cloud Era (2e)]] — what the operations team does once the machines are someone else's
- [[Cloud Native System Architecture (2e)]] — the technical payoff that makes the trade worth considering
