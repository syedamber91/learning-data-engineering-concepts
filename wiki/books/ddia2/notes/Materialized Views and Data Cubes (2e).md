---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
topic: Data Storage for Analytics
type: subtopic
tags: [ddia2, materialized-view, data-cube, olap-cube, aggregates, materialize]
sources:
  - raw/ch04.md
---
# Materialized Views and Data Cubes
> Precompute the aggregates everybody keeps asking for. Just don't throw away the raw data, because a cube can only answer questions along its own dimensions.

## The Idea
In a relational data model, a **materialized view** is a table-like object whose contents are the results of a query. The distinction that matters: a materialized view is an **actual copy of the query results, written to disk**, whereas a **virtual view** is just a shortcut for writing queries — reading from a virtual view makes the SQL engine expand it into the underlying query on the fly and process the expanded query.

## How It Works
- When the underlying data changes, a materialized view **must be updated**. Some databases do that automatically, and there are systems such as **Materialize** that specialise in materialized view maintenance.
- Performing those updates means **more work on writes**, but materialized views **improve read performance** in workloads that repeatedly run the same queries. This is the same read/write trade as every other derived structure in the chapter.
- **Materialized aggregates** are the warehouse-specific case. Warehouse queries often involve aggregate functions — `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. If many queries use the same aggregates, crunching the raw data every time is wasteful, so cache the counts and sums queries use most.
- A **data cube** (or **OLAP cube**) does this by creating a **grid of aggregates grouped by different dimensions**. If each fact has foreign keys to two dimension tables — say `date_key` and `product_sk` — you can draw a two-dimensional table with dates on one axis and products on the other, each cell holding the aggregate (a `SUM`, say) of an attribute (`net_price`) over all facts with that date-product combination. Then apply the same aggregate along each row or column to get a summary **reduced by one dimension**: sales by product regardless of date, or sales by date regardless of product.
- Facts often have more than two dimensions. In the grocery-retailer schema there are five: date, product, store, promotion, and customer. A five-dimensional hypercube is hard to picture but works the same way — each cell holds the sales for a particular date-product-store-promotion-customer combination, repeatedly summarizable along each dimension.

## Trade-offs & Pitfalls
- **The advantage** is that certain queries become very fast because they have effectively been precomputed. Total sales per store yesterday is a lookup along the appropriate dimension, with no need to scan millions of rows.
- **The disadvantage** is that a data cube lacks the flexibility of querying the raw data. There is **no way to calculate what proportion of sales came from items costing more than $100, because price isn't one of the dimensions**. A cube can only answer questions expressible in the dimensions it was built with.
- Hence the standard practice: **most data warehouses keep as much raw data as possible and use aggregates such as data cubes only as a performance boost for certain queries** — not as a replacement for the facts.

## Examples & Systems
Materialize as a specialist materialized-view maintenance system; the five-dimensional grocery cube (date, product, store, promotion, customer) as the worked example.

## Since the 1st Edition
The 1st edition's [[Aggregation - Data Cubes and Materialized Views]] covered the same virtual-versus-materialized distinction, data cubes, and the flexibility caveat, and the substance is unchanged. **New:** Materialize named as a dedicated view-maintenance system, and the forward link to view maintenance as a stream-processing problem — connecting this to [[Event Sourcing and CQRS (2e)]], which the 1st edition did not tie together here.

## Related
- up: [[Data Storage for Analytics (2e)]] · chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Materializing and Updating Timelines (2e)]] — the same idea in an OLTP setting
- [[Event Sourcing and CQRS (2e)]] — materialized views as the read side of a system
- 1st edition: [[Aggregation - Data Cubes and Materialized Views]] — the same subtopic
