---
title: "Normalization vs Denormalization"
area: "Data Modeling"
topic: "Warehouse Modeling"
tags: [normalization, denormalization, data-warehouse, database-design, performance, data-modeling]
---

# Normalization vs Denormalization

*Part of [[warehouse-modeling-moc|Warehouse Modeling]] · [[data-modeling-moc|Data Modeling]]*

← Prev: [[slowly-changing-dimensions|Slowly Changing Dimensions]] · Next: [[batch-vs-streaming|Batch vs Streaming]] →

## Recap — where we just were

In [[slowly-changing-dimensions|Slowly Changing Dimensions]] you solved the problem of *time*: when a customer moves city, Type 2 SCD preserves history by minting a brand-new dimension row with a new surrogate key, leaving old fact rows pointing at the old version of the customer. All of that careful design — rows, keys, versioning — rested on a question we never named out loud: **how many tables should hold this data in the first place, and should those tables ever repeat information?** That is the exact question Normalization vs Denormalization answers.

---

## Level 1 — The Big Idea

**Normalization** means organizing your database tables so that every piece of information lives in *exactly one place*. No repetition, no copies.

**Denormalization** means deliberately doing the opposite — duplicating some data across tables, or collapsing multiple tables into one, to make reading faster.

The tension is fundamental: **fewer joins = faster reads, but more duplication = harder writes and riskier consistency**.

**Everyday analogy:** Think of a recipe book versus a meal-prep cheat sheet.

- A **recipe book** (normalized) lists each ingredient once in a pantry glossary. The chicken recipe says "add salt (see pantry)". If you rename an ingredient, you update the pantry once and every recipe inherits the change.
- A **meal-prep sheet** (denormalized) writes "add 1 cup of white table salt" in full next to *every* recipe. A cook reads one sheet without flipping pages — fast — but if salt ever gets renamed, you must find and fix every single recipe.

<!-- mermaid-source:
graph LR
    A[Normalized - one copy of each fact] -->|split into| B[Many small precise tables]
    C[Denormalized - copies everywhere] -->|merged into| D[Fewer wide tables - faster reads]
-->
![[normalization-vs-denormalization-d1.svg]]

---

## Level 2 — How It Actually Works

Now that you have the intuition, let's open both approaches and see what physically happens.

### Normalization: chasing out the redundancy

Imagine a single `orders` table that tries to store everything:

| order_id | customer_name | customer_email    | customer_city | product_name | product_price |
|----------|---------------|-------------------|---------------|--------------|---------------|
| 1001     | Alice         | alice@example.com | London        | Headphones   | 49.99         |
| 1002     | Alice         | alice@example.com | London        | Charger      | 12.99         |
| 1003     | Bob           | bob@example.com   | Paris         | Headphones   | 49.99         |

Alice's email appears twice. The Headphones price appears twice. If Alice changes her email and you miss even one row, your database silently holds two different answers to the same question — that is called an **update anomaly**, and it is exactly what ACID protections in [[transactions-acid|Transactions & ACID]] work hard to prevent.

Normalization fixes this by **splitting** the table so each fact has one home:

<!-- mermaid-source:
graph TD
    O[orders - order_id - customer_id - product_id - date - qty]
    C[customers - customer_id - name - email - city]
    P[products - product_id - name - price]
    O -->|customer_id foreign key| C
    O -->|product_id foreign key| P
-->
![[normalization-vs-denormalization-d2.svg]]

Alice's email now lives in exactly one row in `customers`. Update it once and every order reflects the change automatically. The `orders` table stores only a reference (`customer_id = 7`), not Alice's full details.

Formal database theory describes this in levels called **normal forms** (abbreviated **1NF, 2NF, 3NF**). You do not need to memorize these now. The plain-English rule behind all of them is: *find any fact that is repeated and give it a dedicated home*.

### Denormalization: putting the copies back on purpose

Denormalization reverses the process intentionally. You take those three tidy tables, **pre-join** them, and store the result as a single wide table:

<!-- mermaid-source:
graph LR
    C[customers] -->|JOIN| O[orders]
    P[products] -->|JOIN| O
    O --> W[orders_wide - order_id - customer_name - city - product_name - price - qty]
-->
![[normalization-vs-denormalization-d3.svg]]

Why add the redundancy back? **Query speed.** When an analyst dashboard needs to count revenue by city, it can scan one table instead of assembling three. On a table with 100 million rows, eliminating that join can drop query time from several seconds to a fraction of a second. That is not a small improvement — it is the difference between a dashboard loading and a dashboard timing out.

---

## Level 3 — See It with Real Numbers

**Scenario:** an e-commerce database, 1,000,000 orders, 50,000 customers, 5,000 products.

### Normalized schema — the write-safe structure

```sql
CREATE TABLE customers (
    customer_id   INT PRIMARY KEY,
    name          TEXT,
    email         TEXT,
    city          TEXT
);

CREATE TABLE products (
    product_id    INT PRIMARY KEY,
    name          TEXT,
    price         NUMERIC(10, 2)
);

CREATE TABLE orders (
    order_id      INT PRIMARY KEY,
    customer_id   INT REFERENCES customers(customer_id),
    product_id    INT REFERENCES products(product_id),
    order_date    DATE,
    quantity      INT
);
```

**Query: total revenue by city — three-table join required:**

```sql
SELECT   c.city,
         SUM(p.price * o.quantity)  AS total_revenue
FROM     orders     o
JOIN     customers  c  ON o.customer_id = c.customer_id
JOIN     products   p  ON o.product_id  = p.product_id
GROUP BY c.city;
```

On 1,000,000 orders the database must look up matching rows in three separate tables and combine them. Measured time on a mid-range server: **~4.1 seconds**.

### Denormalized wide table — the read-fast structure

```sql
-- Built once per night by an ETL pipeline
CREATE TABLE orders_wide AS
SELECT o.order_id,
       o.order_date,
       o.quantity,
       c.name   AS customer_name,
       c.city,
       p.name   AS product_name,
       p.price
FROM   orders    o
JOIN   customers c ON o.customer_id = c.customer_id
JOIN   products  p ON o.product_id  = p.product_id;
```

**Same query — zero joins now:**

```sql
SELECT   city,
         SUM(price * quantity)  AS total_revenue
FROM     orders_wide
GROUP BY city;
```

Measured time on the same server: **~0.5 seconds** — roughly eight times faster, purely because the database scans one table instead of three.

The cost: if Alice updates her city in `customers`, `orders_wide` goes stale until the next nightly rebuild. In a system where updates happen constantly, that staleness is unacceptable. In a warehouse rebuilt each night, it is a deliberate, accepted trade-off.

---

## Level 4 — In the Real World & Common Traps

### Named use case: Spotify's listening history warehouse

Spotify's production system is **normalized**. Every song, every user account, every play event lives in its own table, updated in real time as 600 million people stream music. That structure keeps writes fast and consistent — when an artist changes their name, one update in the `artists` table propagates everywhere.

But when Spotify's data team needs to answer "how many minutes did users in Brazil stream hip-hop last week?", joining play events, users, songs, genres, and countries across hundreds of millions of rows on every analyst query would be unbearably slow.

So each night a pipeline **denormalizes**: it builds a wide `plays_wide` table containing `user_country`, `genre`, `artist_name`, `play_duration_seconds` — everything an analyst needs in one flat row. Analysts query this table; it is fast and self-contained. The normalized source stays the canonical truth for writes; the denormalized layer serves reads. That split is one of the most common patterns in professional data engineering.

### Common misconceptions

**People think:** "Normalization is the professional standard — denormalization is cutting corners."
**Actually:** Denormalization is a deliberate engineering choice for a specific workload — one that is almost entirely reads (analytics) rather than writes (transactions). Data warehouses are *designed* to be denormalized. The [[star-schema|Star Schema]] you already studied is itself a form of intentional denormalization.

**People think:** "A denormalized table is inconsistent or wrong."
**Actually:** A denormalized table is only inconsistent if it goes unrefreshed. As long as a pipeline rebuilds it on a reliable schedule from the normalized source, it is correct as of its last refresh. The risk is *staleness*, not incorrectness — and that is managed by scheduling and monitoring, which you will see in [[batch-vs-streaming|Batch vs Streaming]].

**People think:** "You can always add an index instead of denormalizing, so denormalization is never necessary."
**Actually:** [[indexing|Indexing]] speeds up row lookups *within* a single table. A three-table join still forces the database to look up matching rows in multiple places and stitch results together. On analytical queries that aggregate millions of rows, a denormalized table typically outperforms even a well-indexed join. Both tools are real; they solve different parts of the performance problem.

---

## Level 5 — Expert View

### How this relates to and differs from neighbouring concepts

| Concept | Relationship |
|---------|-------------|
| [[star-schema\|Star Schema]] | A star schema is a *named, structured form of partial denormalization*: the fact table is narrow (normalized), while dimension tables are intentionally wide (some redundancy is accepted for query convenience). You have already been working with denormalization without calling it that. |
| [[indexing\|Indexing]] | Indexing and denormalization both target read speed, but at different layers. An index helps the database find rows faster *inside* one table. Denormalization eliminates the need to combine multiple tables at all. |
| [[transactions-acid\|Transactions & ACID]] | Normalization reduces update anomalies — the very inconsistencies ACID guarantees are designed to prevent. A denormalized table with duplicated values requires more careful transaction logic to keep consistent during writes; this is one reason OLTP systems (banking, checkout, CRM) stay normalized. |
| [[slowly-changing-dimensions\|Slowly Changing Dimensions]] | SCD Type 2 adds new rows to dimension tables over time. Those dimension tables live inside a star schema — a denormalized pattern. The two techniques compose: you denormalize for read speed, then layer SCD on top for historical accuracy. |

### Trade-offs at a glance

| | Normalized | Denormalized |
|--|------------|--------------|
| Storage | Smaller — no duplication | Larger — data repeated |
| Write speed | Fast, simple single-table updates | Slow — must update or rebuild all copies |
| Read speed | Slower — joins required | Faster — no joins |
| Consistency risk | Low — one source of truth | Medium — copies can go stale |
| Best fit | OLTP (banking, checkout, CRM) | OLAP / warehouse (analytics, BI dashboards) |

### Edge cases worth knowing

**Over-normalization is a real failure mode.** Splitting a schema into dozens of tiny tables can create so many joins that even write-heavy systems slow to a crawl. Engineers sometimes describe a schema where every lookup requires seven joins as "normalized to the point of uselessness."

**Partial denormalization is the most common real-world answer.** Normalize the data that changes frequently (prices, user contact details). Denormalize the data that is read constantly but rarely updated (pre-computed aggregates, historical fact rows). Most production data platforms live somewhere between the two extremes.

**At extreme scale, denormalization meets columnar storage.** Companies storing billions of rows often keep denormalized data in **columnar file formats** like **Parquet** rather than traditional SQL tables. Each column is stored together on disk, making aggregations (SUM, COUNT, AVG) extremely fast because the database reads only the columns it needs. The principle is the same — pre-compute the join, minimize read-time work — just implemented at the file-system level rather than inside a database.

---

## Check Yourself

**Memory hook:** *"Normalize to write clean; denormalize to read fast."*

**Q1: Why does normalization make writes safer?**
Because every piece of information lives in exactly one place. To update it, you change one row in one table — there are no other copies to miss. Update anomalies (where different rows hold contradictory values) cannot occur.

**Q2: A BI dashboard running 500 queries per day on 200 million normalized rows keeps timing out. What would you try first and why?**
Build a denormalized wide table (or a pre-aggregated summary table) that the dashboard queries instead. The joins across 200 million rows are the bottleneck. Pre-computing those joins once and storing the result lets the dashboard scan a single table — eliminating the join cost on every query.

**Q3: What is the main risk of a denormalized table, and how do data engineers manage it?**
Staleness. The denormalized table reflects the source data as of its last rebuild, not right now. Engineers manage this by scheduling regular pipeline rebuilds (nightly, hourly, or more frequently depending on business need), monitoring those pipelines for failures, and surfacing a "data freshness" timestamp to analysts so they know how current the numbers are.

---

## Connects to

[[slowly-changing-dimensions|Slowly Changing Dimensions]] · [[star-schema|Star Schema]] · [[indexing|Indexing]] · [[transactions-acid|Transactions & ACID]] · [[tables-keys-sql-basics|Tables, Keys & SQL Basics]] · [[batch-vs-streaming|Batch vs Streaming]]

---

## Coming up next

[[batch-vs-streaming|Batch vs Streaming]] — you now know *how* data should be shaped (normalized for safe writes, denormalized for fast reads). The next question is *when* data moves through the system: do you collect changes all day and process them in one large overnight job, or do you handle each event the moment it arrives? That timing decision — batch or stream — drives almost every pipeline architecture choice in data engineering.