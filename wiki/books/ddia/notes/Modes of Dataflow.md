---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 4
chapter_title: Encoding and Evolution
type: topic
tags: [ddia, dataflow, compatibility, system-architecture]
sources:
  - raw/ch04.md
---
# Modes of Dataflow
Whenever data must reach a process that shares no memory with the sender, it becomes bytes — and compatibility is always a relationship between the *encoding* process and the *decoding* process. This topic maps the three most common channels through which encoded data flows and shows how the backward/forward-compatibility requirements shift with each: who writes, who reads, in what order they get upgraded, and how long old data or old clients linger. This is [[Dataflow]] as an architectural concern, in service of [[Evolvability - Making Change Easy]] — upgrading parts of a system independently instead of all at once.

## Subtopics
- [[Dataflow Through Databases]] — the writer messages its future self; data outlives code, so both compatibility directions plus unknown-field preservation matter.
- [[Dataflow Through Services - REST and RPC]] — request/response between independently deployed clients and servers; REST vs SOAP, why RPC's location transparency misleads, and API versioning.
- [[Message-Passing Dataflow]] — brokers and actor frameworks decouple senders from recipients; compatible encodings let either side deploy first.

## Key Takeaways
- Databases demand the longest memory: five-year-old bytes are still live data, so migrations are avoided and schema evolution papers over historical encodings.
- Services allow one simplifying assumption — servers upgrade before clients — yielding the asymmetric rule: backward-compatible requests, forward-compatible responses.
- A network request is not a function call: timeouts leave outcomes unknown, retries demand [[Idempotence]], latency varies wildly, and references can't cross the wire.
- Brokers give the greatest deployment freedom: with a両-way-compatible encoding, producers and consumers ship in any order.
- The recurring trap across all modes is the read-modify-write cycle that silently drops fields added by newer code.

## Related
- [[Ch 04 - Encoding and Evolution]] — parent chapter MOC
- [[Formats for Encoding Data]] — the encodings these channels carry
- [[Messaging Systems]] — Chapter 11 expands the broker story
- [[Request Routing]] — service discovery in partitioned systems
