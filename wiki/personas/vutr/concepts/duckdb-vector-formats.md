---
persona: vutr
kind: concept
sources:
- raw/duckdb-polars-single-node-engines/i-made-110-in-duckdb.md
last_updated: '2026-07-15'
qc: passed
slug: duckdb-vector-formats
topics:
- single-node-engines-duckdb-polars-vs-distributed-systems
---

This is about how DuckDB represents data in memory for processing — comparable in spirit to Apache Arrow, a standardized column-oriented memory format, but DuckDB has its own standard for this called `Vector`. A Vector is a logically represented array holding data of a single type. The important distinction to hold onto: this `Vector` in-memory format and the vectorized execution engine ([[vectorized-execution-engine]]) are two different concepts that happen to share a name.

Internally, DuckDB supports several different vector formats, which lets the system store the same *logical* data using different *physical* representations depending on the situation:

- **Flat Vectors** — physically stored as a contiguous array; this is the standard, uncompressed vector format. For flat vectors, the logical and physical representations are identical.
- **Constant Vectors** — physically stored as a single constant value. These are useful when data elements are repeated — for example, representing the result of a constant expression in a function call lets DuckDB store the value only once rather than once per row.
- **Dictionary Vectors** — physically stored as a child vector plus a selection vector containing indices into that child vector. Dictionary vectors are emitted by the storage layer when decompressing data that was stored dictionary-encoded.
- **Sequence Vectors** — useful for efficiently storing incremental sequences; these are generally emitted for row identifiers.

The point of having multiple physical formats behind one logical representation is that it allows for a more compressed representation, and potentially allows for compressed execution throughout the system — operators can work directly against a dictionary- or constant-encoded vector without first expanding it back into a flat array.

*See also: [[vectorized-execution-engine]] · [[duckdb-embedded-analytics-model]]*
