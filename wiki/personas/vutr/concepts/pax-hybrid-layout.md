---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: pax-hybrid-layout
topics:
- parquet
---

I used to think Parquet was purely columnar, and I suspect many of you do too — but it's really a PAX (Partition Attributes Across) hybrid layout. It partitions horizontally into row groups first, then columnar into column chunks, which is why calling it 'purely columnar' is imprecise. This was the design intent from its [[parquet-origin]] onward.
