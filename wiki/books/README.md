# wiki/books/

Book-derived study-note trees, siblings of `wiki/personas/<persona>/`. Unlike
a persona wiki, content here is attributed to the book's actual author, not
to any persona examined in this repo — a book tree is never fed into a
persona's `raw/` or synthesized in a persona's voice (see the Global
Constraints in `docs/superpowers/plans/2026-07-15-ddia-vutr-cross-link.md`
in the SOIC_Scraper repo for why).

## Trees
- `ddia/` — *Designing Data-Intensive Applications* (Martin Kleppmann).
  `raw/` = markitdown-converted chapter text (the receipt); `chapters/` =
  chapter/part MOCs; `notes/` = topic + subtopic notes (max granularity);
  `concepts/` = cross-cutting glossary notes. Cross-linked with
  `wiki/personas/vutr/` wherever the two overlap (Kafka, replication,
  partitioning, LSM-trees, batch/stream processing, CDC).
