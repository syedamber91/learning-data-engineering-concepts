---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/i-spent-8-understanding-how-parquet.md
last_updated: '2026-07-15'
qc: passed
slug: plain-encoding
topics:
- parquet
---

`PLAIN` is Parquet's baseline encoding: the specification requires every physical type to support it. It serializes values back-to-back in a standardized little-endian binary layout with no transformation at all — `BOOLEAN` as 1 bit per value, `INT32`/`FLOAT` as 4 bytes each, `INT64`/`DOUBLE` as 8 bytes each, `BYTE_ARRAY` as a 4-byte length prefix followed by the raw bytes, and `FIXED_LEN_BYTE_ARRAY` as just the raw bytes.

It is the default choice precisely when nothing else has a clear advantage: data with high cardinality, randomness, or no exploitable pattern. It is also what dictionary pages are internally encoded with inside [[rle-dictionary]]. The Parquet specification describes `PLAIN` as the universal fallback once other encodings become ineffective, but in practice the Java and Rust implementations fall back to other schemes instead — for instance, Java falls back to `DELTA_BINARY_PACKED` for `INT32`/`INT64` columns rather than dropping all the way to `PLAIN`.

*See also: [[rle-dictionary]] · [[delta-encodings]] · [[parquet-physical-and-logical-types]]*
