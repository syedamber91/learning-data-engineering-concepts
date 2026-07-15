---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/i-spent-8-understanding-how-parquet.md
- raw/parquet-file-format/why-parquet-is-the-go-to-format-for.md
last_updated: '2026-07-15'
qc: passed
slug: delta-encodings
topics:
- parquet
---

Parquet has a family of delta-based schemes, each targeting a specific data shape. `DELTA_BINARY_PACKED` works on INT32/INT64 physical types: instead of storing absolute values, it stores the first value of a block followed by a stream of deltas — the difference between each value and the one before it. It works best on sorted data, which is why it's the go-to choice for event timestamps, auto-incrementing primary keys, or any other monotonically increasing sequence; smaller deltas need fewer bits than the original absolute values.

`DELTA_LENGTH_BYTE_ARRAY` targets `BYTE_ARRAY` columns and solves a specific waste in `PLAIN` encoding: `PLAIN` always prefixes a byte array with a fixed 4-byte length, which for columns of many short strings (e.g. "NY", "CA", "TX") means the length prefixes take up more space than the actual data. This scheme instead collects all the lengths into their own stream, delta-encodes that stream, and concatenates the raw byte-array data into one contiguous block afterward.

`DELTA_BYTE_ARRAY` goes further for strings that share common prefixes. For each string in a sequence, it stores the prefix length shared with the *previous* string plus the remaining suffix. Worked example from a list of URLs: `"www.google.com/search"` (first string, prefix 0, full string as suffix), then `"www.google.com/images"` (shares a 17-character prefix with the previous string, so prefix length 17, suffix "images"), then `"www.google.com/maps"` (prefix 17, suffix "maps"), then `"www.yahoo.com/news"` (shares only "www." — prefix 4, suffix "yahoo.com/news"). The prefix lengths are then bunched together and delta-encoded via `DELTA_BINARY_PACKED`, and the suffixes are encoded with `DELTA_LENGTH_BYTE_ARRAY`.

A related but distinct scheme, [[byte-stream-split-encoding]], also targets fixed-width numeric types (FLOAT/DOUBLE) but works by byte transposition rather than delta — it's grouped here as a sibling encoding rather than a delta variant.

*See also: [[byte-stream-split-encoding]] · [[rle-dictionary]] · [[plain-encoding]] · [[column-chunk]]*
