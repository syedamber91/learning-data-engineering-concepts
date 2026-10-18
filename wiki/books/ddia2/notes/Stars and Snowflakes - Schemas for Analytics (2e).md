---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
topic: Relational Versus Document Models
type: subtopic
tags: [ddia2, star-schema, snowflake-schema, fact-table, dimension-table, obt]
sources:
  - raw/ch03.md
---
# Stars and Snowflakes: Schemas for Analytics
> A fact table of events in the middle, dimension tables radiating outward. Optimised for analysts, not for writers.

## The Idea
Data warehouses are usually relational, and a few conventions dominate their table structure: the **star schema**, the **snowflake schema**, **dimensional modeling**, and **one big table (OBT)**. All are optimised for the needs of business analysts, and ETL processes translate operational data into the chosen schema.

## How It Works
- At the centre sits a **fact table** — the book's example is `fact_sales` for a grocery retailer. Each row represents **an event that occurred at a particular time**: here, a customer's purchase of a product. For website traffic analysis, each row might be a page view or a click.
- Facts are usually captured as **individual events**, because that allows maximum flexibility of analysis later. The cost is size: a big enterprise may have **many petabytes** of transaction history, mostly in fact tables.
- Some fact-table columns are **attributes** — the price the product sold for, the cost of buying it from the supplier (so profit margin can be computed). Others are foreign keys into **dimension tables**. Since each fact row is an event, the dimensions represent the **who, what, where, when, how, and why** of that event.
- For example, `dim_product` has one row per type of product for sale, with its SKU, description, brand name, category, fat content, and package size; each `fact_sales` row uses a foreign key to say which product was sold. Queries often involve multiple joins to multiple dimension tables.
- **Even date and time are often dimension tables**, because that lets additional information about dates — public holidays, for instance — be encoded, so queries can distinguish holiday from non-holiday sales.
- The name **star schema** comes from the visualisation: fact table in the middle, dimension tables around it, connections radiating like a star's rays.
- The **snowflake schema** breaks dimensions into subdimensions — separate tables for brands and product categories, with `dim_product` referencing them by foreign key rather than storing strings. Snowflake schemas are more normalized, but **star schemas are often preferred because they are simpler for analysts to work with**.
- Warehouse tables are typically **wide**: fact tables frequently have over a hundred columns, sometimes several hundred. Dimension tables can be wide too, holding all metadata that might be relevant — `dim_store` might include which services each store offers, whether it has an in-store bakery, square footage, opening date, last remodel date, and distance from the nearest highway.

## Trade-offs & Pitfalls
- A star or snowflake schema consists mostly of **many-to-one relationships** — many sales for one product, in one store — expressed as fact-to-dimension or dimension-to-subdimension foreign keys. Other relationship types could exist in principle but are often denormalized to simplify queries. A multi-item transaction is not represented explicitly: the fact table simply has a separate row per product purchased, and those rows happen to share a customer ID, store ID, and timestamp.
- **One big table (OBT)** takes denormalization further and drops dimension tables entirely, folding their information into denormalized columns of the fact table — essentially precomputing the fact-to-dimension join. It requires more storage but sometimes enables faster queries.
- **Denormalization is unproblematic here**, and the reason is worth internalising: analytics data is typically a log of historical data that will not change, except to correct an occasional error. The consistency and write-overhead issues that make denormalization dangerous in OLTP are not as pressing in analytics.

## Examples & Systems
`fact_sales`, `dim_product`, `dim_store` as the worked grocery-retailer schema; dimensional modeling and OBT as the named alternatives.

## Since the 1st Edition
The content largely survives from the 1st edition's [[Stars and Snowflakes - Schemas for Analytics]], but **the chapter it lives in has changed** — it was a subtopic of "Transaction Processing or Analytics?" inside the storage chapter, and is now part of data modelling, which is where a schema convention belongs. **New:** dimensional modeling and one big table named as alternatives, and the explicit argument for why denormalization is safe in analytics but not in OLTP.

## Related
- up: [[Relational Versus Document Models (2e)]] · chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[Data Warehousing (2e)]] — the system this schema lives inside
- [[Event Sourcing and CQRS (2e)]] — compared explicitly against fact tables
- [[Column-Oriented Storage (2e)]] — the physical layout these wide tables demand
- 1st edition: [[Stars and Snowflakes - Schemas for Analytics]] — the same subtopic, in the storage chapter
