---
persona: vutr
kind: concept
sources:
- raw/olap-cost-and-multi-engine-comparison/7-insights-to-help-you-learn-any.md
last_updated: '2026-07-15'
qc: passed
slug: olap-real-time-freshness-mechanisms
topics:
- olap-cost-and-multi-engine-comparison
---

vutr frames modern OLAP as shifting its central question from "how much data can you process?" to "how fresh is that data?", and names two mechanisms — not mutually exclusive — that different systems use to answer it.

The first is an in-memory buffer. Real-time-oriented engines like Apache Pinot, Apache Druid, and StarRocks don't wait for streamed data (arriving via Kafka or Pulsar) to land on disk before making it queryable: incoming records go straight into a volatile, in-memory structure, and a single query transparently reaches into both places at once — the "cold" historical data resting on disk and the "hot" just-arrived data still sitting in RAM.

The second is a hierarchical storage model, which starts from a different observation: ingestion and analytics genuinely want opposite physical layouts. Writes love row format, since appending one row at a time is fast; reads love columnar format, since scanning and aggregating a handful of columns is fast. BigQuery, per vutr's notes, resolves that tension by first landing incoming data into a memory buffer in row format — letting it absorb millions of small inserts per second without paying the cost of rewriting large columnar files on every single insert — and serving queries against recent data straight out of that buffer, which doubles as its own version of the "hot data in RAM" trick from the first mechanism. Only later, once the row-format data has accumulated and cooled, is it merged into blocks and "flipped" into column format, trading write-time flexibility early for read-time columnar efficiency once the data is no longer actively being appended to.

*See also: [[materialized-view-tradeoffs-and-streaming-convergence]] · [[real-time-olap]]*
