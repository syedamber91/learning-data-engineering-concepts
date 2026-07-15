---
persona: vutr
kind: entity
sources:
- raw/apache-arrow-additional/apache-arrow-for-data-engineers.md
- raw/apache-arrow-additional/i-spent-6-hours-learning-apache-arrow.md
last_updated: '2026-07-15'
qc: passed
slug: record-batch
topics:
- apache-arrow
---

A Record Batch is the Arrow specification's abstraction for representing tabular data, and it is used across many of Arrow's serialization and computation functions — it is also the unit of serialized data in Arrow IPC (see [[arrow-ipc]]). A Record Batch has two parts: a **Schema**, which describes each column's name and type, and a list of **Arrays**, where each array corresponds to one column defined in the schema (see [[arrow-columnar-array-layout]] for what an array itself contains). Equivalently, in IPC terms, a Record Batch's arrays are called its fields, and the field names and types collectively form the batch's schema.

The Record Batch is immutable — because its arrays are immutable — and Vu draws out what that buys: concurrent access is safe by construction, and there's no need to copy data just to share it, since nothing holding a reference to a Record Batch has to worry about another reader mutating it underneath them.

Record Batches are also the building block one level down from Arrow's higher-level Table abstraction, which combines one or more Record Batches (or their underlying array chunks) into a single logical dataset — see [[arrow-table-and-chunked-arrays]] for that distinction and why it matters.

*See also: [[arrow-columnar-array-layout]] · [[arrow-table-and-chunked-arrays]] · [[arrow-ipc]] · [[arrow-flight]] · [[apache-arrow]]*
