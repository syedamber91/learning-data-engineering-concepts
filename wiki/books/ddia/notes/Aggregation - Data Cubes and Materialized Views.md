---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
topic: Column-Oriented Storage
type: subtopic
tags: [ddia, materialized-views, olap-cube, aggregation]
sources:
  - raw/ch03.md
---
# Aggregation - Data Cubes and Materialized Views
> If many queries recompute the same COUNT/SUM/AVG over the raw data, cache the aggregates once — as a materialized view, or in grid form as an OLAP cube.

## The Idea
Warehouse queries lean heavily on aggregate functions — COUNT, SUM, AVG, MIN, MAX. When dozens of reports need the same sums, crunching through billions of raw fact rows for each one is waste. The fix is a cache of precomputed aggregates. Its relational form is the *materialized view*: defined like an ordinary (virtual) view — a table-shaped object standing for a query — but where a virtual view is a mere shorthand that the SQL engine expands into the underlying query at read time, a materialized view is an **actual copy of the query results written to disk**.

## How It Works
Because a materialized view is a [[Denormalization|denormalized]] copy, it must be refreshed whenever the underlying data changes; the database can automate that, at the cost of more expensive writes — which is why [[Materialized Views]] are rare in OLTP systems but sensible in read-heavy warehouses (whether they actually pay off is case-by-case).

The signature special case is the *data cube* (OLAP cube): a grid of aggregates grouped by dimensions. Picture facts with foreign keys to just two dimensions, date and product: lay dates on one axis, products on the other, and fill each cell with, say, SUM(net_price) over all facts with that date–product pair. Summing along a row or column then collapses one dimension — sales per product across all dates, or per date across all products. Real fact tables have more dimensions (the grocery example has five: date, product, store, promotion, customer), making the cube a hard-to-visualize hypercube, but the principle is unchanged: each cell holds the aggregate for one combination, repeatedly summarizable along any axis.

## Trade-offs & Pitfalls
- **Speed:** queries answered from the cube are effectively precomputed — total sales per store yesterday is a lookup along one dimension, not a scan of millions of rows.
- **Lost flexibility:** the cube can only answer questions expressible in its dimensions. What fraction of sales came from items over $100? Unanswerable if price isn't a dimension.
- Consequently most warehouses keep as much *raw* data as possible and treat cubes and materialized aggregates purely as a performance boost for known-hot queries.

## Examples & Systems
The star-schema grocery warehouse of [[Stars and Snowflakes - Schemas for Analytics]] supplies the running example: a fact_sales table whose five dimension keys become cube axes.

## Related
- up: [[Column-Oriented Storage]] · chapter: [[Ch 03 - Storage and Retrieval]]
- [[Data Warehousing]] — the read-heavy setting where aggregate caches earn their keep
- [[Materialization of Intermediate State]] — materialization as a theme in batch dataflow (Ch 10)
- [[Observing Derived State]] — Ch 12 reframes materialized views as derived, incrementally-maintained data
- [[airbnb-data-infrastructure]] — vutr's notes describe this exact pattern in production: Airbnb's Minerva computes a shared dimension once in its join stage and reuses it across every dimension set that needs it, rather than recomputing the aggregate per consumer
