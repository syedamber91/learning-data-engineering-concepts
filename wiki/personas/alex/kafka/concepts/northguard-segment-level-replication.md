---
persona: alex
kind: concept
sources:
- vutr/northguard-segment-level-replication
last_updated: '2026-07-10'
qc: passed
slug: northguard-segment-level-replication
topics:
- kafka
learner: alex
source_note: northguard-segment-level-replication
mastery: mastered
---

Wait, so let me try this. Kafka's problem is like a moving company where the *only* box size is a giant shipping container. If one truck (broker) is overloaded, you can't just hand it a small parcel — you have to heave an entire container off it onto another truck, and that's slow and disruptive, and if you buy a new truck it just sits in the lot empty until you manually reload containers onto it. Northguard's whole trick is: use small boxes instead. A segment is one 1GB box; you keep stacking records into the active box until it's full (or an hour old, or replication fails), then you *seal* it and start a new one. Because you're sealing and opening new boxes constantly, whenever a truck is struggling you don't move any existing box at all — you just say "the *next* box gets loaded onto the new truck," and fresh incoming stuff instantly flows there. So the overloaded truck stops getting new weight immediately, and nobody had to lift a heavy container. Ranges are like a shelf grouping boxes that hold a certain alphabet slice of keys (A→D), and a topic is all the shelves covering A→Z, and you can split or merge shelves. They did the same "small pieces spread evenly" thing to metadata — no single manager node, instead a bunch of Raft groups on vnodes each owning a shard decided by consistent hashing. And they flipped delivery: producers get told a window and only get an ACK when all replicas have it, and consumers get data pushed to them instead of pulling. The catch is they threw away Kafka-protocol compatibility to get this, so it's a LinkedIn-only thing.

*Source: [[northguard-segment-level-replication]] (vutr)*
