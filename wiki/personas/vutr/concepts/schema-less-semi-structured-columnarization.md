---
persona: vutr
kind: concept
sources:
- raw/snowflake-internals/i-spent-another-6-hours-understanding.md
last_updated: '2026-07-15'
qc: passed
slug: schema-less-semi-structured-columnarization
topics:
- snowflake-internals
---

Snowflake SQL adds three types on top of the native SQL ones specifically to handle semi-structured data: `VARIANT`, `ARRAY`, and `OBJECT`. `VARIANT` can hold any native SQL type as well as nested `ARRAY`/`OBJECT` values, and both `ARRAY` and `OBJECT` share the same internal representation — a self-describing binary serialization built for fast key-value lookup, efficient type tests, comparisons, and hashing. That shared representation is what lets a `VARIANT` column be used exactly like a regular column: it can appear in a join, a `GROUP BY`, or an `ORDER BY` without special-casing. Data arriving as JSON, Avro, or XML loads straight into a `VARIANT` column with no schema declared up front — Snowflake handles parsing and type inference on its own — and users can extract from it using functional SQL notation or a JavaScript-like path syntax, or construct it in the first place with `ARRAY_AGG`/`OBJECT_AGG`.

The interesting engineering problem is making schema-less ingestion perform like a normal columnar table, and Snowflake's answer is an automated type-inference step done per table file: it statistically analyzes the collection of documents within that file, infers which typed paths are common enough to be worth pulling out, and physically removes those columns from the documents to store them separately in the same compressed columnar format used for native relational data — complete with the same min-max chunk statistics used elsewhere for pruning (see [[min-max-pruning-and-dynamic-data-skipping]]). Because most queries against semi-structured data only care about a handful of paths, Snowflake pushes the projection and cast expressions for those paths down into the scan operator itself, so only the needed columns are read and cast directly to their target SQL type — the full `VARIANT` document never has to be reconstructed just to pull one field out of it.

Doing this optimization per-file rather than globally creates a real gap: the "common" paths are decided separately for each table file, so a path that's common in most files might be missing from the metadata of a few files where it wasn't frequent enough to warrant extraction. A query that wants to prune on that path can't trust the metadata alone, because some files simply won't have it recorded — even though the path and its data are still present in those files' raw documents. The naive fix is to scan every file lacking that metadata just in case; Snowflake instead computes Bloom filters over all paths present across a file's documents and stores them alongside the rest of the file metadata, so the optimizer can use a Bloom filter to recognize when a file provably lacks a queried path and skip it outright, closing most of the gap without falling back to a full scan.

A related trick handles typed values that arrive as strings — dates and times in JSON, for instance, which have to be converted to their real type before they're useful for filtering or before min-max metadata can be built for them. Because schema is optional at ingestion time, Snowflake performs this conversion optimistically and keeps *both* the converted value and the original string in separate columns. Since unused columns are never loaded or scanned, storing both doesn't cost query performance — only extra storage volume.

*See also: [[min-max-pruning-and-dynamic-data-skipping]] · [[snowflake]]*
