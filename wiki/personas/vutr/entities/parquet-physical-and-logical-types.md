---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/i-spent-8-understanding-how-parquet.md
last_updated: '2026-07-15'
qc: passed
slug: parquet-physical-and-logical-types
topics:
- parquet
---

Parquet distinguishes physical types (how data is actually stored on disk) from logical types (what the data semantically means), and only physical types are what encoding and compression schemes operate on. The physical type set is deliberately small: `BOOLEAN`, `INT32`, `INT64`, `FLOAT`, `DOUBLE`, `BYTE_ARRAY`, `FIXED_LEN_BYTE_ARRAY`, and the now-deprecated `INT96` (legacy timestamps). Keeping this list short is a stated implementation-simplicity choice — a smaller set of physical types makes writing and reading Parquet simpler across implementations.

Logical types are wrappers around a physical type carrying extra metadata that tells the engine how to interpret the raw bytes correctly. A `STRING` logical type, for example, is stored as a `BYTE_ARRAY` physical type, with the raw bytes interpreted as UTF-8; a `DATE` logical type annotates an `INT32`, storing the number of days since the Unix epoch rather than an arbitrary integer.

This split is what lets Parquet's richer application-facing type system (strings, dates, and other logical types) sit on top of a small, uniform set of on-disk representations that every encoding scheme — [[plain-encoding|PLAIN]], [[rle-dictionary]], [[delta-encodings]], [[byte-stream-split-encoding]] — only has to be written against once.

*See also: [[plain-encoding]] · [[rle-dictionary]] · [[delta-encodings]] · [[byte-stream-split-encoding]]*
