---
persona: alex
kind: concept
sources:
- vutr/jvm-object-overhead
last_updated: '2026-07-09'
qc: passed
slug: jvm-object-overhead
topics:
- spark
learner: alex
source_note: jvm-object-overhead
mastery: learning
---

So basically — Java forces every little piece of data to carry a bunch of extra baggage (labels, blank spacers, and pointer-arrows), which makes it about 10x bigger than it really is. Since Spark holds tons of data in memory, that baggage makes it run out of memory fast, so Spark built special tricks (Tungsten, and later Photon in C++) to store data without the Java baggage.

*Source: [[jvm-object-overhead]] (vutr)*
