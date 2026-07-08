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
- storage-models-nsm-dsm-pax-and-column-store
---

PAX (Partition Attributes Across) is the hybrid storage model: data is first split horizontally into row groups, and within each group the column values are stored next to each other. The core lesson is that 'columnar' is not one thing — true DSM only splits vertically, with each column stored completely separately, whereas PAX partitions horizontally first and only then stores columns together. Most systems that claim 'column store' are actually running PAX under the hood, not true DSM, and most blogs and docs conflate the two — so verifying which one a product actually uses matters. Parquet is the example that surprises people: I used to think it was purely columnar, and I suspect many of you do too, but it partitions horizontally into row groups first, then columnar into column chunks — the design intent from its [[parquet-origin]] onward, which is why calling it 'purely columnar' is imprecise. Next time someone says 'storing data in a columnar fashion,' ask them the real question: is this PAX or DSM?

*See also: [[parquet-origin]] · [[rle-dictionary]] · [[footer-filemetadata]] · [[column-by-name]] · [[row-group]] · [[page]]*
