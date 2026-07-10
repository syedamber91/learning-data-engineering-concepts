---
persona: alex
kind: concept
sources:
- vutr/message-key-partitioning-strategies
last_updated: '2026-07-10'
qc: passed
slug: 005-message-key-partitioning-strategies
topics:
- kafka
learner: alex
source_note: message-key-partitioning-strategies
mastery: mastered
---

*What Alex understood:* Okay let me try this back. So a Kafka message isn't like a row with an ID column — there's no ID at all. It's found by where it sits, its offset, inside one partition. And a partition is basically a slice of the topic that can live on its own server, which is how one topic gets spread across many machines. The key is the thing that decides which slice a message drops into.

So here's the flow in my head: I hand the producer a ProducerRecord, kind of like an envelope. The envelope must say what's inside (value) and where it's going (topic), and it can optionally say a key. If I *didn't* already write a partition number on the envelope myself, then a sorting machine — the partitioner — looks at it and asks one yes/no question: is there a key or not?

If there's no key, on new Kafka it doesn't sprinkle messages evenly across partitions. It's more like a bartender filling one glass all the way before starting the next — the sticky partitioner dumps a whole batch into one partition, then moves on. And the reason is that Kafka would rather write one big sequential chunk to disk than a hundred tiny scattered writes, so keeping a batch together is cheaper.

If there *is* a key, Kafka hashes it — like running the key through a blender that always gives the same smoothie for the same fruit — so the same key always lands in the same partition. That's what buys you ordering, because one partition is read in order. So keys aren't about identity, they're about *co-locating* everything with the same key so it stays ordered and together. And DoorDash showed the flip side: all these choices trade safety for speed, like cutting from 3 copies to 2 and not waiting for the copies to confirm, which cut CPU by a third-ish.

## Follow-up questions

**Alex:** If the sticky partitioner deliberately jams a whole batch onto one partition for keyless messages, doesn't that pile all the load onto one consumer the same way a hot key does — so why is a hot key described as the load problem but stickiness isn't?

**vutr:** Good catch on the seam, and the note lets me answer the first half cleanly. Both sticky batching and a hot key concentrate messages onto one partition, and since each partition inside a consumer group is consumed by exactly one consumer, both concentrate load there. The difference the note draws is in *duration and scope*, not the mechanism. The sticky partitioner sticks to one partition only 'until a condition is met — such as the batch reaching its limit,' and then it switches to another partition; so keyless traffic still spreads across partitions over time, batch by batch. A hot key, by contrast, is 'always routed to the same partition' by the hash — there's no switch condition, it's permanent for that key. So stickiness is a temporary, rotating concentration chosen to make batches bigger and disk writes sequential; a hot key is a standing concentration you 'live with at consume time.' That's why the note frames the hot key as the load-distribution problem.

**Alex:** The same-key-same-partition guarantee gives me ordering — but what happens to that guarantee if I later add more partitions to the topic? Wouldn't the hash suddenly send an existing key somewhere new and break the ordering for that entity?

**vutr:** The note tells me the guarantee — same key always routes to the same partition via hashing the key — but it does not describe what happens when you add partitions to an existing topic, or whether repartitioning remaps existing keys and disturbs their ordering. I won't guess at that, so I'm putting it in gaps.
