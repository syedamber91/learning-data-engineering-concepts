---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 5
chapter_title: Encoding and Evolution
type: topic
tags: [ddia2, dataflow, compatibility, evolvability]
sources:
  - raw/ch05.md
---
# Modes of Dataflow
Whenever you send data to another process with which you don't share memory — over a network, or into a file — you must encode it as a sequence of bytes. Forward and backward compatibility matter because they enable **evolvability**: upgrading parts of your system independently rather than changing everything at once.

**Compatibility is a relationship between one process that encodes the data and another that decodes it.** That is a fairly abstract idea, because data can flow between processes in many ways. The organising question for this topic is simply: **who encodes the data, and who decodes it?**

## Subtopics
- [[Dataflow Through Databases (2e)]] — the writer encodes, the reader decodes, and the reader might be five years later.
- [[Dataflow Through Services - REST and RPC (2e)]] — clients and servers, IDLs, RPC's flaws, and finding the service in the first place.
- [[Durable Execution and Workflows (2e)]] — sequences of service calls that must happen exactly once.
- [[Event-Driven Architectures (2e)]] — asynchronous messages through brokers, and distributed actors.

## Key Takeaways
- The three canonical modes, as the chapter summarises them: **databases** (writer encodes, reader decodes), **RPC and REST APIs** (client encodes request, server decodes and encodes response, client decodes response), and **event-driven architectures** using message brokers or actors (sender encodes, recipient decodes).
- Each mode changes *which* direction of compatibility is load-bearing. Databases need both, indefinitely. Services can usually assume servers upgrade before clients, needing backward compatibility on requests and forward compatibility on responses. Cross-organisation APIs need everything, forever.
- The chapter's conclusion is deliberately upbeat: **with a bit of care, backward/forward compatibility and rolling upgrades are quite achievable.**

## Since the 1st Edition
The 1st edition's [[Modes of Dataflow]] had three subtopics — [[Dataflow Through Databases]], [[Dataflow Through Services - REST and RPC]], and [[Message-Passing Dataflow]]. The 2nd edition keeps the first two, **renames the third to [[Event-Driven Architectures (2e)]]**, and **adds a fourth, [[Durable Execution and Workflows (2e)]]**, covering workflow engines and durable execution frameworks — a category that barely existed in mainstream practice in 2017.

## Related
- chapter: [[Ch 05 - Encoding and Evolution (2e)]]
- [[Formats for Encoding Data (2e)]] — the encodings that flow through these channels
- [[Microservices and Serverless (2e)]] — the architecture that makes this matter
- 1st edition: [[Modes of Dataflow]] — the same topic, one subtopic fewer
