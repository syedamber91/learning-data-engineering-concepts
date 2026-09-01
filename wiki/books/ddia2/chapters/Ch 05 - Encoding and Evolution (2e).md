---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 5
chapter_title: Encoding and Evolution
type: chapter-moc
tags: [ddia2, encoding, schema-evolution, compatibility, rolling-upgrade, moc]
sources:
  - raw/ch05.md
---
# Ch 05 – Encoding and Evolution
Applications inevitably change: features are added or modified as products launch, requirements are better understood, or business circumstances change — the **evolvability** idea from Chapter 2. A change to an application's features usually requires a change to the data it stores, and the data models of Chapter 3 cope with that differently: relational databases assume all data conforms to **one schema** in force at any point in time (changeable through migrations), while **schema-on-read** databases don't enforce a schema, so a mixture of older and newer formats can coexist.

Application code must change too, and in a large application code changes **cannot happen instantaneously**. Server-side you may want a **rolling upgrade** (staged rollout): deploy to a few nodes at a time, monitor, and continue — which allows releases without downtime, encourages frequent small releases over rare big ones, and makes deployments less risky by letting faulty releases be caught and rolled back early. Client-side you are at the mercy of the user, who may not install the update for some time. So **old and new versions of code and of data formats coexist**, and you need compatibility in both directions:

- **Backward compatibility** — newer code can read data written by older code.
- **Forward compatibility** — older code can read data written by newer code.

For APIs: an older client calling a newer service needs backward compatibility on the request and forward compatibility on the response; a newer client calling an older service needs forward compatibility on the request and backward compatibility on the response.

**Backward compatibility is normally not hard**: as the author of newer code you know the older format and can explicitly handle it. **Forward compatibility is trickier**, because it requires older code to ignore additions made by newer code — and there is a subtler hazard: if newer code adds a field, writes the record, and then *older* code reads it, updates it, and writes it back, the desirable behaviour is for the old code to **keep the unknown field intact**. If the record is decoded into a model object that doesn't preserve unknown fields, **data is silently lost**.

## Map
- [[Formats for Encoding Data (2e)]] — the encoding/decoding problem and the format landscape
  - [[Language-Specific Formats (2e)]] — convenient, and a bad idea for anything non-transient
  - [[JSON, XML, and Binary Variants (2e)]] — the textual standards, their flaws, JSON Schema, and binary JSON
  - [[Protocol Buffers (2e)]] — field tags, and schema evolution built on them
  - [[Avro (2e)]] — no tag numbers; writer's and reader's schemas resolved at decode time
  - [[The Merits of Schemas (2e)]] — why schema-driven binary encodings earn their keep
- [[Modes of Dataflow (2e)]] — who encodes, who decodes, and what that implies
  - [[Dataflow Through Databases (2e)]] — data outlives code
  - [[Dataflow Through Services - REST and RPC (2e)]] — web services, IDLs, why RPC's location transparency fails, and service discovery
  - [[Durable Execution and Workflows (2e)]] — workflow engines and exactly-once semantics across services
  - [[Event-Driven Architectures (2e)]] — message brokers and distributed actors

## Chapter Summary
Encoding details affect not only efficiency but **the architecture of applications and your options for evolving them**. Because rolling upgrades mean different nodes run different code versions, all data flowing around the system must be encoded to provide **backward compatibility** (new code reads old data) and **forward compatibility** (old code reads new data).

The formats divide three ways. **Language-specific encodings** are restricted to one language and often fail at compatibility. **Textual formats** — JSON, XML, CSV — are widespread, with compatibility depending on how you use them; their optional schema languages are sometimes helpful and sometimes a hindrance, and they are vague about datatypes, so numbers and binary strings need care. **Binary schema-driven formats** — Protocol Buffers and Avro — give compact, efficient encoding with clearly defined compatibility semantics, and their schemas are useful for documentation and for code generation in statically typed languages; the downside is that data must be decoded before it is human-readable.

The **modes of dataflow** are three: through **databases** (the writer encodes, the reader decodes), through **RPC and REST APIs** (client encodes request, server decodes and encodes response, client decodes response), and through **event-driven architectures** using message brokers or actors (sender encodes, recipient decodes). The chapter's closing verdict is optimistic: with a bit of care, backward/forward compatibility and rolling upgrades are quite achievable.

## Since the 1st Edition
This is the 1st edition's Chapter 4, and its spine is unchanged: the same compatibility definitions, the same format survey, the same encoded-record example (`userName` / `favoriteNumber` / `interests`), the same byte-count comparison, and the same dataflow taxonomy. **Substantially new:** [[Durable Execution and Workflows (2e)]] as an entire subtopic (Temporal, Restate, Airflow, BPMN — none in the 1st edition); **JSON Schema** treated at length, with open/closed content models and its evolution difficulties; **service discovery, load balancing, and service meshes** (Istio, Linkerd, etcd, ZooKeeper), which the 1st edition did not cover here; **OpenAPI/Swagger and service frameworks** (FastAPI, Spring Boot, gRPC) with worked examples; and **AsyncAPI** and schema registries for messaging. **Renamed and merged:** the 1st edition's separate [[Thrift and Protocol Buffers]] becomes [[Protocol Buffers (2e)]] with Thrift demoted to a mention, and [[Message-Passing Dataflow]] becomes [[Event-Driven Architectures (2e)]]. **Dropped:** the 1st edition's extended discussion of Thrift's BinaryProtocol versus CompactProtocol, and its MapReduce/dataflow-through-services material that moved to other chapters.

## Related
- home: [[Home (2e)]] · previous: [[Ch 04 - Storage and Retrieval (2e)]] · next: [[Ch 06 - Replication (2e)]]
- [[Evolvability - Making Change Easy (2e)]] — the quality this chapter serves
- [[When to Use Which Model (2e)]] — schema-on-read versus schema-on-write
- 1st edition: [[Ch 04 - Encoding and Evolution]] — the chapter this one revises
