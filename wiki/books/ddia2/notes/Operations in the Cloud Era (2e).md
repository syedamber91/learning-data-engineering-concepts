---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
topic: Cloud Versus Self-Hosting
type: subtopic
tags: [ddia2, devops, sre, operations, capacity-planning]
sources:
  - raw/ch01.md
---
# Operations in the Cloud Era
> The machines disappear behind an API, so capacity planning becomes financial planning and performance optimisation becomes cost optimisation. The need for operations does not shrink.

## The Idea
The people who traditionally managed server-side data infrastructure were **database administrators (DBAs)** and **system administrators (sysadmins)**. More recently many organisations merged development and operations into teams sharing responsibility for both backend services and data infrastructure, guided by the **DevOps** philosophy; **site reliability engineers (SREs)** are Google's implementation of that idea. The role of operations is to ensure services are reliably delivered — configuring infrastructure, deploying applications — and to keep production stable, which means monitoring and diagnosing anything that threatens reliability.

## How It Works
For self-hosted systems, operations traditionally means a lot of per-machine work: capacity planning (watch disk space, add disks before running out), provisioning new machines, moving services between machines, installing OS patches. Cloud services present an API that hides the individual machines: cloud storage replaces fixed-size disks with **metered billing**, so you store data without planning capacity ahead and are charged for space used, and many cloud services stay available even when individual machines fail. The high-level goal of operations is unchanged; the processes and tools have evolved.

The DevOps/SRE philosophy emphasises:
- Setting up automation, preferring repeatable processes over manual one-off jobs.
- Using ephemeral VMs and services rather than long-running servers.
- Enabling frequent application updates.
- Learning from incidents.
- Preserving the organisation's knowledge about the system even as individual people come and go.

A **bifurcation of roles** followed. Operations teams at infrastructure companies specialise in delivering a reliable service to many customers; the customers of that service try to spend as little time and effort on infrastructure as possible. Customers still need operations, but focused differently: choosing the right service for a task, integrating services with each other, and migrating between them.

## Trade-offs & Pitfalls
- Metered billing removes traditional capacity planning but not the need to know what you are using and why — otherwise you waste money on resources nobody needs. **Capacity planning becomes financial planning, and performance optimisation becomes cost optimisation.**
- Cloud services impose **resource limits or quotas** (for example, the maximum number of concurrently running processes) that you need to know about and plan for *before* you hit them.
- Adopting a service can be quicker than running your own infrastructure, but you still have to learn the service and often work around its limitations.
- **Integration is the growing pain.** As more vendors offer ever broader ranges of services, integrating them is a particular challenge, and at present there are no standards to facilitate it — so it often takes significant manual effort. ETL is only part of the story; operational cloud services need integrating with each other too.
- Several things cannot be outsourced at all: maintaining the security of your application and its libraries, managing interactions between your own services, monitoring load, and tracking down the causes of performance degradations or outages. The cloud changes the role of operations; it does not remove it.

## Examples & Systems
Google's SRE practice as the named implementation of DevOps for reliability.

## Since the 1st Edition
New as a section. The 1st edition discussed operability as a facet of maintainability (see [[Operability - Making Life Easy for Operations]]), but had nothing on how cloud economics reshape the operations role, metered billing, quotas, or the vendor/customer split in operational expertise. The maintainability material itself survives, relocated to [[Operability - Making Life Easy for Operations (2e)]].

## Related
- up: [[Cloud Versus Self-Hosting (2e)]] · chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Operability - Making Life Easy for Operations (2e)]] — operability as a design goal, in the next chapter
- [[Reliability and Fault Tolerance (2e)]] — the reliability target operations exists to hit
