---
persona: alex
kind: concept
sources:
- vutr/photon
last_updated: '2026-07-09'
qc: passed
slug: 015-photon
topics:
- spark
learner: alex
source_note: photon
mastery: mastered
---

*What Alex understood:* Let me say it back the way I actually understand it. Photon is a bolt-in speed engine: it doesn't rewrite how Spark plans a query, it just supplies faster C++ versions of the physical operators, and JNI stitches the C++ and JVM sides together (measured at only 0.06% overhead, so basically free). The 'why columnar' clicked for me — vectorization means doing one operation over a whole batch of one column's values at once, and you can only do that cleanly if those values are packed together, which is exactly what columnar layout gives you and row-oriented doesn't. The part that surprised me is the interpreted-vs-codegen choice. My gut said 'generate custom compiled code, that's fastest.' But Databricks optimized for ENGINEERING VELOCITY and DEBUGGABILITY, not just peak theoretical speed: interpreted vectorized C++ prototyped in weeks vs two months, and you can print-debug plain native code, while codegen makes code at runtime that you can't easily inspect — you'd have to bolt on extra tooling just to see what went wrong. So the real lesson is that the vectorization (columnar batches on the CPU) is where the speed comes from, and going interpreted rather than codegen was a deliberate trade of a bit of theoretical ceiling for a much faster, more debuggable path to a working engine.

## Follow-up questions

**Alex:** If vectorization is what makes Photon fast, and Spark's Catalyst already does code generation for speed, are vectorization and code generation two competing ways to reach the same goal (beating row-at-a-time interpretation), and could an engine in principle combine both — codegen'd loops over columnar batches?

**vutr:** Good instinct — you've spotted that they're two answers to the same enemy: the overhead of processing one row at a time through generic interpreted machinery. Code generation attacks it by writing bespoke compiled code so there's no per-row interpretation overhead. Vectorization attacks it differently — by amortizing overhead across a whole batch of column values and letting the CPU chew through them cache-efficiently. They are not mutually exclusive in theory; you could generate code that loops over columnar batches, and some engines do blend the ideas. But the source is about a specific PRODUCT decision, not theory: Databricks deliberately picked interpreted vectorization ALONE, because for their engineering constraints — a working engine in weeks and the ability to print-debug native C++ — that path won over the two-month, hard-to-debug codegen path. So: same goal, different mechanisms, and Photon consciously took the vectorized-interpreted lane for velocity and debuggability, accepting whatever theoretical ceiling codegen might have offered.

**Alex:** The source says Photon integrates as physical operators and only some of a query runs in it. When part of a query runs in Photon (columnar C++) and part runs in Spark's row-oriented JVM operators, doesn't the data have to be converted between columnar and row layouts at the seam — and is that conversion cost part of, or separate from, the 0.06% JNI figure?

**vutr:** You've put your finger on exactly the seam that matters, and here I have to be honest about the limits of the source. The source tells us three hard facts: Photon is columnar in-memory, Spark SQL is row-oriented, and Photon integrates as physical operators (so mixed plans exist). It's a sound INFERENCE that a boundary between a columnar Photon operator and a row-oriented Spark operator would require a row/columnar transition, and real engines do pay a transition cost there. But the source does NOT state that this cost exists, quantify it, or say whether it's folded into the 0.06% number. The 0.06% figure in the source is specifically labeled JNI overhead — the cost of crossing the Java/native call boundary — not row/columnar layout conversion. So the accurate answer is: your instinct about a conversion seam is reasonable and matches how such engines generally work, but treat the existence and cost of that conversion as UNVERIFIED against this source; only the JNI-crossing cost (0.06%) is actually stated.
