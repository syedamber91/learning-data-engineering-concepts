---
persona: alex
kind: concept
sources:
- vutr/message-key-partitioning-strategies
last_updated: '2026-07-10'
qc: passed
slug: message-key-partitioning-strategies
topics:
- kafka
learner: alex
source_note: message-key-partitioning-strategies
mastery: mastered
---

Okay let me try this back. So a Kafka message isn't like a row with an ID column — there's no ID at all. It's found by where it sits, its offset, inside one partition. And a partition is basically a slice of the topic that can live on its own server, which is how one topic gets spread across many machines. The key is the thing that decides which slice a message drops into.

So here's the flow in my head: I hand the producer a ProducerRecord, kind of like an envelope. The envelope must say what's inside (value) and where it's going (topic), and it can optionally say a key. If I *didn't* already write a partition number on the envelope myself, then a sorting machine — the partitioner — looks at it and asks one yes/no question: is there a key or not?

If there's no key, on new Kafka it doesn't sprinkle messages evenly across partitions. It's more like a bartender filling one glass all the way before starting the next — the sticky partitioner dumps a whole batch into one partition, then moves on. And the reason is that Kafka would rather write one big sequential chunk to disk than a hundred tiny scattered writes, so keeping a batch together is cheaper.

If there *is* a key, Kafka hashes it — like running the key through a blender that always gives the same smoothie for the same fruit — so the same key always lands in the same partition. That's what buys you ordering, because one partition is read in order. So keys aren't about identity, they're about *co-locating* everything with the same key so it stays ordered and together. And DoorDash showed the flip side: all these choices trade safety for speed, like cutting from 3 copies to 2 and not waiting for the copies to confirm, which cut CPU by a third-ish.

*Source: [[message-key-partitioning-strategies]] (vutr)*
