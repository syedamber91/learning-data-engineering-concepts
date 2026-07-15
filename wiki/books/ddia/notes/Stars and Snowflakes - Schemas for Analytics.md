---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
topic: Transaction Processing or Analytics?
type: subtopic
tags: [ddia, star-schema, dimensional-modeling, fact-table, data-warehouse]
sources:
  - raw/ch03.md
---
# Stars and Snowflakes: Schemas for Analytics
> Nearly all warehouses converge on one shape: a giant fact table of events at the center, ringed by dimension tables describing who, what, where, when, how, and why.

## The Idea
Transaction processing uses a wide variety of data models tuned to each application, but analytics is strikingly uniform. Most warehouses follow the **star schema** (a.k.a. dimensional modeling): pick the events you care about, record each one as a row in a central table, and factor the descriptive context out into surrounding lookup tables. Capturing facts as raw individual events — rather than pre-summarized — preserves maximum analytical flexibility later.

## How It Works
- **Fact table:** one row per event — e.g., each customer purchase of a product at a grocery chain (`fact_sales`), or each page view/click in web analytics. Some columns are attributes of the event itself (sale price, supplier cost — enabling margin calculations); the rest are foreign keys into dimension tables.
- **Dimension tables:** the event's context. A `dim_product` row carries SKU, description, brand, category, fat content, package size, and so on; the fact row just references it. Even date and time are usually dimensions, so metadata like public holidays can be attached and queried (holiday vs non-holiday sales).
- A multi-item shopping basket becomes multiple fact rows, one per product.
- The name: diagrammed, the fact table sits at the center with dimension tables radiating outward like a star's rays.
- **Snowflake schema:** the normalized variant — dimensions decompose further into sub-dimensions (brand and category get their own tables that `dim_product` references, instead of storing strings inline). More normalized, but analysts generally prefer plain stars for simplicity; the star accepts some [[Denormalization]] deliberately.
- **Scale and width:** fact tables at giants like Apple, Walmart, or eBay reach tens of petabytes. Tables run very wide — fact tables often exceed 100 columns, sometimes several hundred, and dimension tables carry every attribute that could conceivably matter to analysis (store square footage, in-store bakery, distance to the nearest highway…).

## Trade-offs & Pitfalls
- Star vs snowflake is a normalization trade-off: snowflakes avoid redundancy but multiply joins and analyst confusion; stars duplicate strings but keep queries simple.
- Event-grain fact tables grow enormous — which is precisely the storage/query problem [[Column-Oriented Storage]] exists to solve, since a typical query touches only 4–5 of those 100+ columns.

## Examples & Systems
The grocery-retailer example (`fact_sales` with date, product, store, promotion, customer dimensions) is the canonical illustration; dimensional modeling is codified in Kimball's *Data Warehouse Toolkit* tradition and used across Teradata-, Vertica-, and RedShift-class warehouses.

## Related
- up: [[Transaction Processing or Analytics]] · chapter: [[Ch 03 - Storage and Retrieval]]
- [[Data Warehousing]] — where these schemas live and how data arrives
- [[Column-Oriented Storage]] — physical layout for querying wide fact tables
- [[Aggregation - Data Cubes and Materialized Views]] — precomputed summaries over the star
- [[Relational Model Versus Document Model]] — the modeling-diversity contrast on the OLTP side
- [[dbt]] — vutr's notes work through this chapter's star schema as a hands-on dbt project: Kimball's four-step design process, surrogate-key-driven SCD Type 2 dimension tables, and a `fact_sale` table built with dbt incremental models rather than the grocery-retailer textbook example.
