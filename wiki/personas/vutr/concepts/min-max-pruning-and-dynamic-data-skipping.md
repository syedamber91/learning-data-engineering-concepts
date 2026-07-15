---
persona: vutr
kind: concept
sources:
- raw/snowflake-internals/i-spent-8-hours-diving-deep-into.md
- raw/snowflake-internals/i-spent-another-6-hours-understanding.md
last_updated: '2026-07-15'
qc: passed
slug: min-max-pruning-and-dynamic-data-skipping
topics:
- snowflake-internals
---

Traditional databases narrow the amount of data they touch with indexes like B+Trees, but the posts are explicit about why that approach doesn't transfer to OLAP: B+Tree-style indexes serve random or point access well — the OLTP pattern — while OLAP workloads scan large volumes of data restricted to a handful of columns, a pattern indexes don't help with, and maintaining an index on already-huge analytical tables just adds more volume on top. Snowflake's substitute is min-max-based pruning: for a given chunk of data (a record, file, or block), it tracks the minimum and maximum value present. A query filtering for values between 8 and 15 can then skip any chunk whose max is below 8 or whose min is above 15, without ever reading that chunk's contents. This is described as one instance of a much wider pattern — the same statistic shows up in Parquet's own metadata, in BigQuery's proprietary Capacitor format, and in table formats like Iceberg and Delta Lake, plus DuckDB's native format.

What's easy to miss is that Snowflake applies this pruning both statically and dynamically. Static pruning is the version above — chunk statistics are already known before the query runs, and the optimizer just consults them. Dynamic pruning happens *during* execution: in a hash join, Snowflake can collect statistics on the distribution of join keys from the build side, then push that information over to the probe side and use it to filter out files on the probe side that can't possibly contain a matching key — a form of pruning that couldn't be planned ahead of time because it depends on data seen mid-query. This dynamic variant is part of the same broader capability the posts call runtime adaptivity (see [[cascades-optimizer-and-runtime-adaptivity]]): decisions that traditional, purely static query planning can't make because they need information only available once execution is already underway.

Min-max pruning also resurfaces, in a more elaborate form, inside Snowflake's handling of semi-structured data — see [[schema-less-semi-structured-columnarization]], where the same min/max chunk statistics get computed for automatically-extracted VARIANT paths, and Bloom filters are layered on top to solve a gap min-max pruning alone can't close.

*See also: [[schema-less-semi-structured-columnarization]] · [[cascades-optimizer-and-runtime-adaptivity]] · [[snapshot-isolation-and-immutable-file-versioning]] · [[snowflake]]*

## Related in the other wiki
- [[Bloom Filters]] — DDIA's general concept note on Bloom filters; Snowflake's own use of them (over semi-structured document paths, see [[schema-less-semi-structured-columnarization]]) is a concrete instance of the same probabilistic-skip idea applied to query pruning rather than to key lookups.
