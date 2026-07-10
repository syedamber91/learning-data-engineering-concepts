---
persona: alex
kind: concept
sources:
- vutr/tungsten-and-jvm-object-overhead
last_updated: '2026-07-10'
qc: passed
slug: 010-tungsten-and-jvm-object-overhead
topics:
- spark
learner: alex
source_note: tungsten-and-jvm-object-overhead
mastery: mastered
---

*What Alex understood:* Wait, so... okay let me try this. Normal Spark rows are just regular Java objects sitting on the heap, right? And Java objects are like shipping something in this giant padded crate even when the actual item is tiny — that's the 48-bytes-for-4-bytes thing, the crate itself (the header, the boxing) costs way more than what's inside it. And because it's a real object on the heap, the garbage collector has to come around, open every crate, check what's still needed, and throw out the rest — and while it's doing that, the whole warehouse (the executor) just... stops. Nobody can grab anything until GC's done walking the aisles.

So Tungsten's fix isn't 'get a faster GC guy' — it's 'stop putting things in crates that GC has to open.' First move: even staying on the same shelf (on-heap), it repackages rows as these specialized Spark SQL type objects instead of raw boxed Java objects, so there's way less stuff for GC to walk through. Second move, the bigger one: it can move the whole shelf off the building's inventory system entirely — off-heap — but only if I flip it on myself with spark.memory.offHeap.enabled and give it a size. And off-heap looks simpler once it's on: no separate reserved/user split like on-heap has, just execution and storage, still divided by that same storageFraction knob.

The binary format itself is called UnsafeRow, and this is where the HashAggregate vs SortAggregate thing clicked for me. HashAggregate is like a mail-sorting system where every mailbox slot is the exact same size, so the carrier can walk straight to slot #47 and swap the letter in place — that only works if every letter (every aggregation buffer) is a fixed size, which Integer/Long/Double are, but a String isn't, since it can stretch. So the second a GroupBy includes even one column that isn't fixed-size — like Vu's 20GB job with l_comment and l_returnFlag — Spark can't do the slot trick anymore, so it falls back to SortAggregate, sorting first. And the UDF thing is basically saying all of this only applies while you stay inside Spark's own engine — the moment a row goes into a Python UDF it has to leave UnsafeRow format entirely, get serialized, shipped out, and rebuilt row by row, so none of the GC-avoidance survives that trip.

## Follow-up questions

**Alex:** If off-heap memory is completely outside the JVM heap, what actually frees it back up once Spark's done with a shuffle or a cached partition — since there's no GC out there to walk it, doesn't it just leak forever unless something else is cleaning it?

**vutr:** The buffer HashAggregate updates in place is one structure per key, not one slot per column — it's the whole aggregation result for that key, addressed by a single fixed byte layout so UnsafeRow can jump straight to it and update it. The note is explicit that 'the buffer needs a fixed byte size' for that in-place update to work, and that Integer/Long/Double qualify because they're always the same number of bytes while a String isn't and 'can't be mutated in place inside a fixed-size slot.' Since a String breaks the fixed-size requirement for the buffer as a whole, not just for its own field, the whole buffer's layout stops being addressable the fast way — so the fallback to SortAggregate happens at the level of the whole aggregation (the operator Spark picks for that GroupBy), not per column. That's exactly what the 20GB case study shows: it only took l_comment and l_returnFlag being in the touched columns for Spark to pick SortAggregate for the entire GroupBy.

**Alex:** You said Spark falls back to SortAggregate the instant ANY column in the GroupBy is a String, even if most of the other columns are fixed-size Longs — why does one non-fixed-size column ruin the fixed-size trick for the WHOLE aggregation, instead of Spark just hash-aggregating the fixed-size columns and sort-handling only the string ones?

**vutr:** (the wiki does not cover this — see open questions)
