---
persona: vutr
kind: entity
sources:
- raw/data-pipeline-design-framework-additional/my-framework-to-build-a-data-pipeline.md
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9-4c5.md
last_updated: '2026-07-15'
qc: passed
slug: dead-letter-queue-and-bad-data-isolation
topics:
- data-pipeline-design-framework
---

Vu Trinh's rule for bad data is that it "is not needed and must be discarded as soon as possible" — but with an explicit carve-out: some cases still require looking at the low-quality data later, for debugging or for health-checking the source it came from. That carve-out is why bad data needs a specific destination rather than simply being dropped: it must be stored somewhere isolated, so it can serve the debugging/health-check purpose without contaminating the good output.

His two named destinations map to the two processing modes: a dead-letter queue for stream processing, and a dedicated dataset for batch processing. He repeats this identical guidance verbatim across both his sink/source/middle-steps framework and his deeper processing-layer piece, treating it as settled practice rather than something worth re-litigating — the open design questions live elsewhere (what counts as bad in the first place, covered under [[data-quality-rules-and-anomaly-detection]]), not in where quarantined data goes once it's been flagged.

*See also: [[data-quality-rules-and-anomaly-detection]] · [[processing-layer-observability]] · [[pipeline-failure-recovery-and-checkpointing]]*
