---
persona: vutr
kind: concept
sources:
- raw/history-of-data-engineering-and-hadoop-ecosystem/8-minutes-to-understand-presto.md
last_updated: '2026-07-15'
qc: passed
slug: presto-columnar-execution-optimizations
topics:
- history-of-data-engineering
---

Presto is written in Java, so its optimizations start with living inside the JVM rather than fighting it: Presto leans on the JVM's Just-In-Time compiler for performance-critical code, avoids allocating large objects to sidestep performance issues, and uses flat memory arrays for critical data structures specifically to reduce garbage-collection overhead.

At the file-format level, Presto exploits the structure of columnar formats like ORC and Parquet in two ways. Data skipping uses the statistics stored in a file's header and footer — min-max ranges, Bloom filters — so custom readers can skip whole sections of irrelevant data without reading them. Direct block conversion lets those readers convert compressed data straight into Presto's own native block format, avoiding a separate decompression step entirely.

Presto goes further and processes data in its compressed form whenever it can, rather than decompressing eagerly. Dictionary and Run-Length-Encoded (RLE) blocks are operated on directly: dictionaries are processed in fast, unconditional loops, and their structure is exploited again when building hash tables for joins and aggregations. Presto also produces compressed intermediate results — for example, its join processor generates dictionary or RLE blocks as output, reusing the same compressed structures rather than materializing plain data — which minimizes both data movement and storage as results flow between stages.

The same philosophy extends to when data gets touched at all: Presto supports lazy materialization, only decompressing and decoding the contents of a compressed (dictionary or RLE) block when a cell inside it is actually accessed. Combined, these techniques mean Presto often does real work — filtering, skipping, even parts of joins — without ever fully expanding the data into its raw, decompressed form, which is where the bulk of its performance gains over a naively eager reader come from.

*See also: [[presto]] · [[presto-coordinator-worker-scheduling]] · [[presto-resource-management-and-fault-tolerance]]*
