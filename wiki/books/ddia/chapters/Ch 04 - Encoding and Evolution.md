---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 4
chapter_title: Encoding and Evolution
type: chapter-moc
tags: [ddia, encoding, schema-evolution, dataflow, moc]
sources:
  - raw/ch04.md
---
# Ch 04 – Encoding and Evolution
Applications never stop changing, and every change to features tends to drag the stored data format along with it. Because rolling upgrades on servers and slow-updating clients guarantee that old and new code (and old and new data) coexist in one running system, every byte that crosses a process boundary must be readable in both directions: backward compatibility (new code reads old data) and forward compatibility (old code reads new data) — the machinery behind [[Schema Evolution]]. This chapter examines the encoding formats that make that possible — from language-native serializers through JSON/XML and their binary variants to the schema-driven trio of Thrift, Protocol Buffers, and [[Avro]] — and then follows encoded data through the three great channels of [[Dataflow]]: databases, request/response services (REST and RPC), and asynchronous message passing.

## Map
- [[Formats for Encoding Data]] — turning in-memory structures into bytes, and why the format choice shapes evolvability
  - [[Language-Specific Formats]] — built-in serializers (Java, pickle, Marshal): convenient, insecure, versioning-hostile
  - [[JSON, XML, and Binary Variants]] — ubiquitous textual formats, their datatype vagueness, and MessagePack-style binary siblings
  - [[Thrift and Protocol Buffers]] — field tags as the compatibility contract; compact binary encodings from IDL schemas
  - [[Avro]] — no tags at all; writer's vs reader's schema resolution, ideal for dynamically generated schemas
  - [[The Merits of Schemas]] — why schema-driven binary beats "schemaless": compactness, documentation, guaranteed compatibility checks
- [[Modes of Dataflow]] — the three channels where one process's encoding meets another's decoding
  - [[Dataflow Through Databases]] — messages to your future self; data outlives code; preserving unknown fields
  - [[Dataflow Through Services - REST and RPC]] — web services, the flawed location-transparency dream of RPC, and evolvable APIs
  - [[Message-Passing Dataflow]] — brokers and the actor model: decoupled senders and recipients, one-way asynchronous messages

## Chapter Summary
The chapter's core argument: how you turn data structures into bytes is not a low-level detail — it determines whether you can deploy new versions gradually and without downtime. Rolling upgrades (a few nodes at a time, faulty releases rolled back before they spread) are what make frequent, low-risk releases possible, and they only work if every encoding in flight tolerates version skew in both directions.

Three families of formats were compared. Language-specific serializers lock you into one language and usually neglect compatibility altogether. Textual formats (JSON, XML, CSV) are everywhere, but compatibility is up to how you use them, their optional schema languages cut both ways, and their fuzziness about numbers and binary strings bites in practice. Schema-driven binary formats — Thrift, Protocol Buffers, [[Avro]] — give compact encodings with precisely defined forward/backward compatibility rules, plus schemas that double as documentation and code-generation input for statically typed languages; the price is that the raw bytes are unreadable without decoding.

Finally, three dataflow scenarios show where these compatibility properties matter: databases (the writer encodes, a possibly much later reader decodes — data outlives code), REST/RPC services (client encodes request, server decodes and responds, client decodes the response), and asynchronous message passing via brokers or actors (sender encodes, recipient decodes, with the broker decoupling them). The reassuring conclusion is that bidirectional compatibility, and therefore fearless frequent deployment, is entirely achievable with a little care.

## Related
- part: [[Part I - Foundations of Data Systems]] · home: [[Home]]
- previous: [[Ch 03 - Storage and Retrieval]] — how bytes are laid out and indexed once stored; this chapter covers how they're encoded in the first place
- next: [[Ch 05 - Replication]] — encoded data flowing between nodes becomes copies of data across nodes
- [[Evolvability - Making Change Easy]] — Ch 1's design goal that this chapter's compatibility rules operationalize
- [[Relational Model Versus Document Model]] — schema-on-write vs schema-on-read, the data-model side of schema change
- [[Messaging Systems]] — Ch 11 deepens the broker-based dataflow introduced here
