---
persona: alex
kind: concept
sources:
- vutr/warpstream-stateless-agent-architecture
last_updated: '2026-07-10'
qc: passed
slug: warpstream-stateless-agent-architecture
topics:
- kafka
learner: alex
source_note: warpstream-stateless-agent-architecture
mastery: mastered
---

Okay, let me try to rebuild this. The dumb version I had in my head was 'Kafka, but it dumps stuff in S3' — but you're saying that's tiered storage, where the brokers are still real machines holding recent data. WarpStream is more like they gutted the whole thing and rebuilt the Kafka *protocol* so the only thing running is these identical, disposable agents that don't remember anything. Think of it like a call center where every operator is interchangeable and all the actual records live in a shared filing warehouse (S3) plus a little ledger (the metadata store) that tracks where every folder is.

The part that clicked for me is the lying. Normal Kafka is like a class where each kid is assigned to be 'captain' of one subject, and if you have a question about math you *must* go to the math captain. WarpStream has no captains — anyone can answer — but the students (clients) were trained to expect captains, so the office (control plane) just tells each kid 'yeah, that agent over there is your math captain' even though it's a lie, and it deliberately points them at an agent in their own building (AZ) so they don't pay to walk across campus.

And the write path is basically: don't ack immediately, instead collect a bunch of letters for 250ms or until you have 8 MiB, staple them into one file, drop it in the warehouse, write down in the ledger 'here's where it is and here's the order,' and *only then* say 'got it.' The ordering is invented at that ledger-commit moment because the letters themselves arrived scattered with no built-in order. That's why it's slow-ish — ~400ms to produce, ~1s end to end — but way cheaper, like 5–10x cheaper per GiB, because you're batching S3 PUTs instead of paying cross-AZ and replicated-disk taxes. Reads then use a hashing ring so a specific agent 'owns' certain data and caches ~16MB chunks in memory, which is honestly them sneaking leaders back in through the side door to get locality.

*Source: [[warpstream-stateless-agent-architecture]] (vutr)*
