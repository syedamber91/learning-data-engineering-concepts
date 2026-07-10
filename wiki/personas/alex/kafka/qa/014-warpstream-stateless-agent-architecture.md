---
persona: alex
kind: concept
sources:
- vutr/warpstream-stateless-agent-architecture
last_updated: '2026-07-10'
qc: passed
slug: 014-warpstream-stateless-agent-architecture
topics:
- kafka
learner: alex
source_note: warpstream-stateless-agent-architecture
mastery: mastered
---

*What Alex understood:* Okay, let me try to rebuild this. The dumb version I had in my head was 'Kafka, but it dumps stuff in S3' — but you're saying that's tiered storage, where the brokers are still real machines holding recent data. WarpStream is more like they gutted the whole thing and rebuilt the Kafka *protocol* so the only thing running is these identical, disposable agents that don't remember anything. Think of it like a call center where every operator is interchangeable and all the actual records live in a shared filing warehouse (S3) plus a little ledger (the metadata store) that tracks where every folder is.

The part that clicked for me is the lying. Normal Kafka is like a class where each kid is assigned to be 'captain' of one subject, and if you have a question about math you *must* go to the math captain. WarpStream has no captains — anyone can answer — but the students (clients) were trained to expect captains, so the office (control plane) just tells each kid 'yeah, that agent over there is your math captain' even though it's a lie, and it deliberately points them at an agent in their own building (AZ) so they don't pay to walk across campus.

And the write path is basically: don't ack immediately, instead collect a bunch of letters for 250ms or until you have 8 MiB, staple them into one file, drop it in the warehouse, write down in the ledger 'here's where it is and here's the order,' and *only then* say 'got it.' The ordering is invented at that ledger-commit moment because the letters themselves arrived scattered with no built-in order. That's why it's slow-ish — ~400ms to produce, ~1s end to end — but way cheaper, like 5–10x cheaper per GiB, because you're batching S3 PUTs instead of paying cross-AZ and replicated-disk taxes. Reads then use a hashing ring so a specific agent 'owns' certain data and caches ~16MB chunks in memory, which is honestly them sneaking leaders back in through the side door to get locality.

## Follow-up questions

**Alex:** If the metadata store is the single leader that sequences every partition's batches at commit time, isn't that one component now the bottleneck and single point of failure for the whole cluster — the exact stateful thing they said they were escaping? What stops it from becoming the new broker they were trying to kill?

**vutr:** You've spotted the real tension, and the note is partly honest about it. What it does tell us: the metadata store is deliberately a *strongly consistent database combined with object storage* — DynamoDB + S3 on AWS, Cloud Spanner + GCS on GCP, Cosmos DB + Blob on Azure — and it lives in WarpStream's own cloud account, not the customer's VPC. It is described as the 'leader for all topic partitions' that sequences batches at commit time, so yes, it is genuinely a stateful, centralized point in the design — the note frames statelessness as belonging to the *agents*, not to the whole system. WarpStream's answer to 'isn't that the broker again?' is that they moved the stateful part *out* of the data plane and into a managed, strongly consistent store built on cloud primitives that are themselves highly available (DynamoDB, Spanner, Cosmos), while keeping most of what it holds as lightweight *pointers* to batches in object storage rather than the data itself. But whether that store's throughput or availability becomes the practical bottleneck — the note does not give latency, throughput, or failure numbers for the metadata store, so I can't quantify that for you.

**Alex:** You said reads use a consistent-hashing ring where agent A forwards a Fetch to the 'responsible' agent B for cache locality — but writes are fully leaderless and any agent writes any partition. So when a consumer wants to read data that was just written moments ago by some random agent, how does agent B already have the right ~16MB chunk cached, and doesn't that forwarding hop add even more latency on top of the ~1s?

**vutr:** Great catch on the seam between leaderless writes and locality-based reads — the note actually calls this out as a caveat. The mechanism it gives: reads go through a *consistent-hashing ring* where each agent owns a subset of data, so agent A forwards the Fetch to the responsible agent B, and B asks the *metadata store* for the right files, loads ~16 MB chunks into memory, and serves from memory afterward. The caching key point is that ownership is assigned by the hashing ring, so the same agent consistently ends up responsible for the same data and therefore builds up the relevant cache. The note is explicit that this consistent-hashing cache assignment is 'in effect a fall back to leader-based ideas to recover data locality' — because leaderless writes fragment a partition across many small objects, they need this workaround to get locality back. On the extra-hop latency: the note gives the ~400ms produce P99 and ~1s end-to-end P99 as the headline figures and mentions the forwarding hop and the cache, but it does not break out how much latency the A→B forwarding hop itself adds, so I can't put a number on that specific cost.
