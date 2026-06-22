---
title: "Star Schema"
area: "Data Modeling"
topic: "Warehouse Modeling"
tags: [star-schema, data-modeling, analytics, warehouse, dimensions, fact-table]
---

# Star Schema

*Part of [[warehouse-modeling-moc|Warehouse Modeling]] · [[data-modeling-moc|Data Modeling]]*

## In one line

A star schema is a way of organising tables in a data warehouse so that one central table holds your measurements (sales totals, click counts, revenue) and several surrounding tables hold the descriptions (who, what, when, where) — making it fast and simple to answer business questions.

## Picture this

Imagine a pizza at the centre of a table. The pizza is the main thing that happened — a sale, a booking, a page view. Around it sit four dipping sauces: one labelled *Customer*, one labelled *Product*, one labelled *Date*, one labelled *Store*. Each sauce adds detail to the pizza without changing what the pizza is.

Now look at the whole arrangement from above. Pizza in the middle, sauces pointing outward. That shape is a star.

That is a star schema. The pizza is the **fact table** — it holds your numbers. The sauces are **dimension tables** — they hold the descriptions that give those numbers meaning.

## How it actually works

A star schema has exactly two kinds of tables. Understanding the difference is the whole concept.

**Fact table** holds *measurements*: numbers you want to analyse — `revenue`, `quantity_sold`, `discount_amount`, `duration_seconds`. One row in the fact table represents one event: one sale, one flight booking, one song play. Because events pile up constantly, fact tables can have hundreds of millions of rows. They also hold **foreign keys** — integer columns that point to each dimension table, like a numbered ticket that says "look up row 4,291 in the product table for the full description."

**Dimension tables** hold *context*: descriptive, text-heavy columns that explain who or what was involved. `customer_name`, `city`, `product_category`, `day_of_week`, `store_region`. Dimension tables are much smaller than the fact table — you might have 80,000 customers, but 600 million sales.

When you ask a business question — *"How much revenue did we earn from teenage customers buying electronics in London in Q3?"* — the database joins the fact table to whichever dimension tables you need, filters on the dimension columns, and aggregates the fact column. One query, one answer.

**Why is this fast?** Dimension tables in a star schema are **denormalised** — the descriptive data is flattened into one wide table per dimension rather than split across many smaller ones. Fewer joins means faster queries, and that matters enormously when your fact table has 600 million rows.

## Worked example

You run a chain of bookshops. Here is a minimal star schema:

```sql
-- Central fact table: one row per sale
CREATE TABLE fact_sales (
  sale_id       INT PRIMARY KEY,
  date_id       INT,           -- FK → dim_date
  customer_id   INT,           -- FK → dim_customer
  product_id    INT,           -- FK → dim_product
  store_id      INT,           -- FK → dim_store
  quantity_sold INT,
  revenue       DECIMAL(10, 2)
);

-- Dimension: date (200 distinct years × months × days ≈ 3,650 rows)
CREATE TABLE dim_date (
  date_id    INT PRIMARY KEY,
  full_date  DATE,
  year       INT,
  quarter    INT,
  month_name VARCHAR(20),
  day_of_week VARCHAR(10)
);

-- Dimension: product (10,000 rows)
CREATE TABLE dim_product (
  product_id INT PRIMARY KEY,
  title      VARCHAR(200),
  genre      VARCHAR(50),
  price_band VARCHAR(20)  -- 'budget', 'mid', 'premium'
);
```

Now answer: **"What was total revenue from Crime novels in Q1 2025?"**

```sql
SELECT
  SUM(f.revenue) AS total_revenue
FROM fact_sales   f
JOIN dim_date     d ON f.date_id    = d.date_id
JOIN dim_product  p ON f.product_id = p.product_id
WHERE p.genre    = 'Crime'
  AND d.year     = 2025
  AND d.quarter  = 1;
-- Result: £1,842,390.00
```

With 200 million rows in `fact_sales`, this query touches two tiny dimension tables (3,650 rows and 10,000 rows), filters down to roughly 4 million matching fact rows, then sums one decimal column. A composite index on `fact_sales(date_id, product_id)` brings runtime to under 10 seconds — often under 2 in a columnar warehouse like BigQuery or Redshift.

## In the real world

Amazon runs seller analytics on a star-schema pattern. The central fact table records every order line: product sold, quantity, revenue, fulfilment centre, timestamp. Dimension tables hold seller profiles, the product catalogue, date hierarchies, and geography. When a seller opens their dashboard and asks "Show me my top 10 products by revenue in the last 30 days, broken down by marketplace country," the warehouse executes a star-schema query — fact table joined to four dimensions, grouped and sorted. The denormalised design means Amazon does not drill through twelve normalised tables every time 2 million sellers refresh their dashboards simultaneously.

## Common misconceptions

**People think "star schema" means it is advanced or complicated — actually** the name refers only to the shape: one table in the centre, others radiating outward like star points. It is one of the *simpler* warehouse designs, not one of the harder ones. Beginners often assume it must be hard because it sounds architectural.

**People think every column in the fact table should hold a number — actually** the fact table holds *measurements and foreign keys*. Foreign keys are integers, not descriptions. Descriptions always live in dimension tables. If you find yourself putting `customer_name` or `product_category` directly in `fact_sales`, you have made a design mistake — those columns belong in a dimension.

**People think you should normalise dimension tables to save disk space — actually** splitting `dim_product` into `dim_product + dim_category + dim_subcategory` (a pattern called a **snowflake schema**) saves a small amount of disk space but adds extra joins to every query. In modern analytics warehouses, storage costs pennies; query speed costs seconds of human waiting and dollars of compute. So you keep the dimension flat and accept the redundancy.

## How it relates & differs

| Concept | How it RELATES | How it DIFFERS |
|---|---|---|
| [[normalization-vs-denormalization\|Normalization vs Denormalization]] | Star schema is a deliberate choice to *denormalise* — dimension tables flatten related data into one wide table to avoid joins. | Normalisation removes redundancy to protect write integrity; star schema accepts redundancy to gain read (analytics) speed. They are opposite design goals, each right in its own context. |
| [[slowly-changing-dimensions\|Slowly Changing Dimensions]] | SCDs are the technique for managing *changes inside a dimension table* over time — e.g., a customer moves city. You need SCDs to keep a star schema historically accurate. | Star schema defines the *structure* of your warehouse; SCDs define *how to update the structure* when the real world changes. Structure first, update strategy second. |
| [[tables-keys-sql-basics\|Tables, Keys & SQL Basics]] | Star schema is built from tables, primary keys, and foreign keys — those are the raw ingredients. | Basic SQL tables have no particular design philosophy; star schema is an opinionated *pattern* layered on top, with specific rules about what each table is allowed to contain. |

## Why you'd use it (and when not to)

**Use it** when your goal is analytics: slicing, dicing, aggregating, and visualising business data across millions of rows. Star schemas power nearly every data warehouse (Amazon Redshift, Google BigQuery, Snowflake). They are also easy to explain to non-technical stakeholders because the model maps directly to the questions people already ask: "sales by region and quarter" is literally a join to `dim_store` and `dim_date`.

**Do not use it** for transactional systems — online stores, banking apps, hospital admissions — where you are writing thousands of records per second and need strict data integrity. Those systems use normalised designs to prevent update anomalies (updating one fact in one place rather than in a hundred rows). Also avoid a pure star when your data relationships are genuinely many-to-many and multi-directional; the flat dimension model cannot represent that cleanly without duplicating data excessively.

## Check yourself

**Memory hook:** *"Fact in the middle, descriptions at the points — like a star."*

**Q1. What belongs in a fact table versus a dimension table?**
The fact table holds measurements (numbers you aggregate — revenue, quantity, duration) and foreign key integers pointing to each dimension. Dimension tables hold descriptive text attributes (names, categories, dates, regions) that give context to those measurements.

**Q2. A colleague adds a `genre` column directly to `fact_sales` instead of keeping it in `dim_product`. What problem does this cause?**
`genre` is a description, not a measurement — it belongs in `dim_product`. Storing it in the fact table means every one of the 200 million sale rows carries a redundant text string. If the genre classification system ever changes, you must update 200 million rows instead of the few thousand rows in `dim_product`. It bloats storage and makes maintenance painful.

**Q3. Why does a star schema deliberately avoid splitting dimensions into smaller tables?**
Because analytics queries join the fact table to dimensions on every run. Adding more dimension tables means more joins, and joins across 200 million fact rows are expensive. Denormalising — keeping all product attributes in one `dim_product` table — means one join instead of three or four. Storage saved by splitting is rarely worth the query speed lost.

## Connects to

[[tables-keys-sql-basics|Tables, Keys & SQL Basics]] · [[normalization-vs-denormalization|Normalization vs Denormalization]] · [[slowly-changing-dimensions|Slowly Changing Dimensions]] · [[indexing|Indexing]] · [[batch-vs-streaming|Batch vs Streaming]]