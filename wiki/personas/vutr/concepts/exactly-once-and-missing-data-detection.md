---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/data-engineering-system-design-11.md
last_updated: '2026-07-15'
qc: passed
slug: exactly-once-and-missing-data-detection
topics:
- change-data-capture-cdc-and-data-sourcing
---

The ideal is exactly-once: for a given real-world event, exactly one data record should reflect it — not zero, not more than once. Vu is direct that this ideal is rarely reality, and the two failure modes it splits into behave very differently. Duplicates arrive when the same record shows up more than once — common in streaming systems, where at-least-once delivery is Kafka's default, or when a retry causes data to be ingested into the source twice. Missing data is the quieter failure: records that should have arrived never do, and you don't find out until you cross-check against the source. Vu's examples are a batch window that silently drops records, an API that mis-paginates and skips a page, or a Kafka consumer that commits its offset before processing finishes and then crashes — leaving those records marked "consumed" even though they were never actually processed.

Handling duplicates usually means deduplication on read, but Vu flags that the hard part isn't the dedup logic — it's finding the right key to dedup on, which sometimes isn't explicit in the source and requires profiling the data or asking around. For missing data, the practical countermeasures are tracking record counts at ingestion and comparing them against the source, validating that API pagination returns the expected total, and — for streams — committing offsets only after processing actually succeeds, rather than before.

*See also: [[incremental-extraction-strategies]] · [[source-delete-handling]] · [[data-quality-contract-with-source]]*
