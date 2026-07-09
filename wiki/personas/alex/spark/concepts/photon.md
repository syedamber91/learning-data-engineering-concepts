---
persona: alex
kind: concept
sources:
- vutr/photon
last_updated: '2026-07-09'
qc: passed
slug: photon
topics:
- spark
learner: alex
source_note: photon
mastery: mastered
---

Let me say it back the way I actually understand it. Photon is a bolt-in speed engine: it doesn't rewrite how Spark plans a query, it just supplies faster C++ versions of the physical operators, and JNI stitches the C++ and JVM sides together (measured at only 0.06% overhead, so basically free). The 'why columnar' clicked for me — vectorization means doing one operation over a whole batch of one column's values at once, and you can only do that cleanly if those values are packed together, which is exactly what columnar layout gives you and row-oriented doesn't. The part that surprised me is the interpreted-vs-codegen choice. My gut said 'generate custom compiled code, that's fastest.' But Databricks optimized for ENGINEERING VELOCITY and DEBUGGABILITY, not just peak theoretical speed: interpreted vectorized C++ prototyped in weeks vs two months, and you can print-debug plain native code, while codegen makes code at runtime that you can't easily inspect — you'd have to bolt on extra tooling just to see what went wrong. So the real lesson is that the vectorization (columnar batches on the CPU) is where the speed comes from, and going interpreted rather than codegen was a deliberate trade of a bit of theoretical ceiling for a much faster, more debuggable path to a working engine.

*Source: [[photon]] (vutr)*
