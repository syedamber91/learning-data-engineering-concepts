---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, fault-tolerance, correctness]
sources:
  - raw/ch12.md
---
# Idempotence

An operation is idempotent if doing it twice has the same effect as doing it once.
That single property converts unreliable at-least-once delivery into effectively
exactly-once processing: if a consumer may see duplicates (after retries or
recovery), making the effect idempotent — via natural semantics (set x = 5) or
deduplication keys/offsets — neutralizes them.

In the book: the backbone of [[Fault Tolerance]] in stream processing and of the
end-to-end argument in [[The End-to-End Argument for Databases]] — TCP dedup or
database transactions alone don't dedupe across user retries; you need an end-to-end
operation identifier. See also [[Exactly-Once Semantics]].

## Referenced In
- [[Ch 12 - The Future of Data Systems]]
- [[Combining Specialized Tools by Deriving Data]]
- [[Composing Data Storage Technologies]]
- [[Data Integration]]
- [[Dataflow Through Services - REST and RPC]]
- [[Fault Tolerance]]
- [[Message-Passing Dataflow]]
- [[Modes of Dataflow]]
- [[Processing Streams]]
- [[Single-Object and Multi-Object Operations]]
- [[The End-to-End Argument for Databases]]
- [[Timeliness and Integrity]]

## Related in the other wiki
- [[idempotency]] — vutr's concept covers exactly this property at the data-pipeline level, with concrete techniques (overwrite instead of append, MERGE/upsert, avoid non-deterministic functions like NOW()) for making a processing step idempotent end-to-end.
- [[safe-writes-and-schema-evolution-in-serving]] — vutr's concept is the serving-layer instance of this same page: four named strategies (MERGE/upsert, overwrite-by-partition, dedup-on-write, append-with-dedup-on-read) for what a sink does when it receives the same logical write twice.
- [[snowflake-copy-into-and-event-driven-orchestration]] — a concrete case where this property arrives "for free": Snowflake's COPY INTO tracks already-loaded files internally, so a repeated load doesn't duplicate rows without the pipeline author building any deduplication logic themselves.
