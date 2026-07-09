---
persona: alex
kind: concept
sources:
- vutr/jvm-object-overhead
last_updated: '2026-07-09'
qc: passed
slug: 012-jvm-object-overhead
topics:
- spark
learner: alex
source_note: jvm-object-overhead
mastery: mastered
---

*What Alex understood:* Alex: Okay, let me say it back the way I actually get it now. The trick is separating the DATA from the BOX it comes in. My real data is 4 bytes. But a JVM object isn't just the data — it's the data plus a header (identity bits + a pointer to what class it is), plus a pointer to the actual char array, plus padding to round up to 8 bytes. All that packaging is 48+ bytes, so ~90% of what I'm storing is box, not content — a 10x blowup. And the key thing that made it click: this isn't once, it's PER object, and Spark does billions of rows, so I'm paying the tax billions of times. Two things break because of that. First, memory: Spark's execution memory is a fixed budget (that 0.6 fraction after the 300MB reserved), so if headers eat it, way fewer real rows fit before Spark has to spill to disk or throw OOM. Second, speed: every pointer means the CPU jumps to a random spot in memory to find the value, which misses the cache and kills fast looping. So the fix isn't 'buy more RAM' — the fix is stop using JVM objects. Store the values as raw packed bytes off-heap in columns (Tungsten), where a value is just bytes at an offset — no header, no pointer, no padding. Photon does the same in C++ with a columnar layout instead of Spark's row layout. So the 10x overhead is literally the REASON columnar off-heap execution exists — it's the tax they built the engine to dodge.

## Follow-up questions

**Alex:** You said Spark's execution memory is a fixed slice — the unified region is spark.memory.fraction 0.6 after the 300MB reserved. So is the whole point of Tungsten going *off-heap* partly to escape that budget entirely — like, off-heap bytes don't count against that 0.6 execution slice and also don't get scanned by garbage collection?

**vutr:** vutr: Exactly the right instinct, and both halves are true. The heap object model is what creates the pressure — headers and references eat the unified execution slice, so you fit fewer real rows before spilling. Going off-heap with Tungsten's binary layout sidesteps that in two ways. First, the raw bytes are packed with no per-value header or padding, so the same budget holds far more actual data. Second — and this is the part people underrate — objects on the JVM heap are tracked by garbage collection; billions of tiny objects means the GC is constantly walking the heap to see what's still alive, which stalls the executor. Off-heap bytes are opaque to the GC: it doesn't scan or trace them, so you dodge the GC pauses that scale with object count. I'll flag the strict budget-accounting detail — whether off-heap is literally excluded from the 0.6 fraction versus managed as a separate off-heap region — as something to confirm; the source establishes the fixed on-heap budget and the object overhead, and the off-heap escape is the direct consequence, but the exact accounting line isn't spelled out in the material.

**Alex:** Photon 'chose vectorized (interpreted) over code generation.' But Spark already has Catalyst's Code Generation stage turning plans into Java bytecode. If codegen already exists to make things fast, why did Photon deliberately pick the *interpreted* vectorized path instead — doesn't interpreted usually mean slower?

**vutr:** vutr: Great catch, because on paper codegen 'should' win. The reason Photon went interpreted-vectorized is engineering economics, straight from the source: 'Chosen vectorized (interpreted) over code generation: weeks to prototype vs two months.' Codegen generates executing code at runtime, and the source is explicit about the cost: 'Code generation is more complicated to build and debug because the approach generates executing code at runtime; Databricks engineers need to add extra code manually to find issues. In contrast, the interpreted approach only deals with native C++ code; print debugging was much more manageable.' So the win isn't that interpreted is faster in the abstract — it's that a *vectorized* interpreted engine over *columnar* data is already extremely fast (it loops over packed column bytes, which is exactly the layout that beats the pointer-chasing object model), and it's far cheaper to build and debug than runtime codegen. And crucially the C++/JNI boundary they worried about turned out to be a non-issue: 'JNI overhead measured at 0.06% of execution time.' So Photon gets most of the speed from columnar vectorization — the same escape from JVM-object overhead we just discussed — without paying the codegen complexity tax.
