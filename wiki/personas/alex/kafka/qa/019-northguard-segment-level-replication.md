---
persona: alex
kind: concept
sources:
- vutr/northguard-segment-level-replication
last_updated: '2026-07-10'
qc: passed
slug: 019-northguard-segment-level-replication
topics:
- kafka
learner: alex
source_note: northguard-segment-level-replication
mastery: mastered
---

*What Alex understood:* Wait, so let me try this. Kafka's problem is like a moving company where the *only* box size is a giant shipping container. If one truck (broker) is overloaded, you can't just hand it a small parcel — you have to heave an entire container off it onto another truck, and that's slow and disruptive, and if you buy a new truck it just sits in the lot empty until you manually reload containers onto it. Northguard's whole trick is: use small boxes instead. A segment is one 1GB box; you keep stacking records into the active box until it's full (or an hour old, or replication fails), then you *seal* it and start a new one. Because you're sealing and opening new boxes constantly, whenever a truck is struggling you don't move any existing box at all — you just say "the *next* box gets loaded onto the new truck," and fresh incoming stuff instantly flows there. So the overloaded truck stops getting new weight immediately, and nobody had to lift a heavy container. Ranges are like a shelf grouping boxes that hold a certain alphabet slice of keys (A→D), and a topic is all the shelves covering A→Z, and you can split or merge shelves. They did the same "small pieces spread evenly" thing to metadata — no single manager node, instead a bunch of Raft groups on vnodes each owning a shard decided by consistent hashing. And they flipped delivery: producers get told a window and only get an ACK when all replicas have it, and consumers get data pushed to them instead of pulling. The catch is they threw away Kafka-protocol compatibility to get this, so it's a LinkedIn-only thing.

## Follow-up questions

**Alex:** You said writes route to the *next active segment* on the new broker to relieve a hot node — but the hot node is still storing and serving reads from all the *old* sealed segments it already owns. So doesn't it stay overloaded on reads and storage even though new writes went elsewhere, or is there something that eventually moves those sealed segments off it too?

**vutr:** Great catch on the seam here. What the note actually claims is narrower than 'the hot node is now fully fixed.' It says that when a broker is buckling under *write* pressure, Northguard assigns the next active segment to the new broker so that *ingest traffic routes there immediately, relieving the struggling node* — the relief is specifically about new incoming writes stopping, not about reclaiming what's already stored. The note does add that because segments are smaller than Kafka's partitions, any data that *does* need to move is cheaper to move, and that fewer clients are affected by rebalancing. So the design's answer to 'what about the old sealed segments' is that moving them, if needed, is now cheap and low-disruption — but the note frames the immediate relief as redirecting ingest, and does not spell out a specific mechanism that automatically migrates already-sealed segments off the hot node, so I won't invent one.

**Alex:** A segment can be sealed early because it 'fails to replicate' — but if replication is failing, how does the new segment you open right after it succeed at replicating? What's different about the next one, versus just hitting the same failure again?

**vutr:** The note tells us one of the three triggers for sealing a segment is that it 'fails to replicate' — alongside hitting max size or being active more than an hour — but it does not explain what happens next: why opening a fresh segment would then succeed, or how the failed replication is recovered. That's genuinely outside what this note covers.
