---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/i-spent-8-understanding-how-parquet.md
last_updated: '2026-07-15'
qc: passed
slug: byte-stream-split-encoding
topics:
- parquet
---

`BYTE_STREAM_SPLIT` is unusual among Parquet's encodings because it doesn't shrink the data by itself — it exists purely to make the *later* compression pass more effective. It applies to fixed-width types, mainly `FLOAT` (4 bytes) and `DOUBLE` (8 bytes): for a type of N bytes, it reorganizes the data into N separate byte streams, where the first stream holds the first byte of every value, the second stream holds the second byte of every value, and so on; the N streams are then concatenated.

The reasoning is about where the entropy actually sits inside a float or double. The first few bytes typically carry the exponent and sign — these tend to repeat or follow recognizable patterns (the sign bit, for instance, may stay the same value for long stretches). The last few bytes carry precision, and tend to be close to random. Under [[plain-encoding|PLAIN]] encoding, these two kinds of bytes are interleaved within every value, which makes it hard for a general-purpose compressor to find repeating patterns. `BYTE_STREAM_SPLIT` groups the patterned high-order bytes together (and the noisy low-order bytes together), giving the compressor a genuine opportunity to compress the patterned portion effectively.

*See also: [[plain-encoding]] · [[delta-encodings]] · [[parquet-physical-and-logical-types]]*
