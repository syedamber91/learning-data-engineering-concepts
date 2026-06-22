---
title: "Slowly Changing Dimensions"
area: "Data Modeling"
topic: "Warehouse Modeling"
tags: [slowly-changing-dimensions, scd, data-modeling, warehouse-modeling, history-tracking, dimensions]
---

# Slowly Changing Dimensions

*Part of [[warehouse-modeling-moc|Warehouse Modeling]] · [[data-modeling-moc|Data Modeling]]*

## In one line

A Slowly Changing Dimension (SCD) is a strategy for deciding what your data warehouse does when a piece of descriptive information — like a customer's address or job title — changes over time: do you erase the old value, add a new row, or keep one extra "previous" column?

## Picture this

Imagine you keep a paper address book. One day your friend Emma moves to a new city.

- **Type 1 (overwrite):** You erase her old address and write the new one. Simple — but you can never prove she ever lived anywhere else.
- **Type 2 (add a row):** You add a second entry for Emma — "Emma (2022–2024, old city)" and "Emma (2025–present, new city)." The book gets longer, but the full history is there.
- **Type 3 (extra column):** You cross out the old address and write the new one, but you keep a small note in the margin that says "previously: old city." One step of history, and no more.

That is the whole idea of SCDs — three different answers to the question: *what do we do when something quietly changes?*

## How it actually works

In a data warehouse, dimension tables hold the **describing information** about your business objects — think customers, products, employees, or store locations. A dimension record is things like: name, city, loyalty tier, product category, department. These feel stable, but they *do* change — just slowly. (A customer upgrades from Silver to Gold. A product moves to a new category. An employee changes their job title.)

The problem: your fact table (the table of events — sales, logins, orders) links to the dimension by a key. If a customer's tier changes and you silently update the dimension, every historical sale for that customer will now look like it was made by a Gold-tier customer — even the ones from two years ago when they were Silver. Your historical reports become quietly wrong.

**SCD Type 1 — Overwrite**
Just update the row in place. The old value is gone forever. Use this when history genuinely does not matter — fixing a typo in a name, for example. It is the simplest option, but it destroys the past.

**SCD Type 2 — Add a new row**
When a value changes, you close the old row (stamp it with an end date and mark it inactive) and insert a brand-new row with the new value and a fresh start date. The old row stays. The fact table's old events still point to the old dimension row — so historical reports remain correct. This is the most common and most powerful SCD type in real warehouses, but it inflates the size of the dimension table over time.

**SCD Type 3 — Previous-value column**
You add an extra column to the dimension row — something like `previous_city`. When the value changes, you copy the current value into `previous_city` and overwrite the current column. You keep exactly one step of history. This is compact, but it only ever remembers one change. If Emma moves twice, the first city is lost forever.

There are also hybrid types (Type 4, Type 6) that combine these, but Types 1, 2, and 3 are the foundation you need.

## Worked example

Say we have a `dim_customer` table in a warehouse. Emma started as a Silver loyalty member and was upgraded to Gold on 1 March 2025.

**Before any change (baseline row):**

```sql
-- dim_customer
| customer_key | customer_id | name  | loyalty_tier | effective_date | expiry_date  | is_current |
|--------------|-------------|-------|--------------|----------------|--------------|------------|
| 1001         | C-42        | Emma  | Silver       | 2022-01-15     | 9999-12-31   | TRUE       |
```

A `customer_key` of 1001 is what the fact table (`fact_orders`) stores. All of Emma's old orders point to key 1001.

**Type 1 — just overwrite:**

```sql
UPDATE dim_customer
SET loyalty_tier = 'Gold'
WHERE customer_id = 'C-42';
```

Result: the Silver row is gone. Emma's 2022 orders now look like Gold orders. Historical analysis is broken.

**Type 2 — add a new row (the right way for history):**

```sql
-- Step 1: close the old row
UPDATE dim_customer
SET expiry_date = '2025-02-28',
    is_current  = FALSE
WHERE customer_id = 'C-42'
  AND is_current = TRUE;

-- Step 2: insert the new row with a new surrogate key
INSERT INTO dim_customer
  (customer_key, customer_id, name, loyalty_tier, effective_date, expiry_date, is_current)
VALUES
  (1087, 'C-42', 'Emma', 'Gold', '2025-03-01', '9999-12-31', TRUE);
```

Now the table looks like this:

```
| customer_key | customer_id | name  | loyalty_tier | effective_date | expiry_date  | is_current |
|--------------|-------------|-------|--------------|----------------|--------------|------------|
| 1001         | C-42        | Emma  | Silver       | 2022-01-15     | 2025-02-28   | FALSE      |
| 1087         | C-42        | Emma  | Gold         | 2025-03-01     | 9999-12-31   | TRUE       |
```

Emma's old orders still point to key 1001 (Silver). New orders will point to key 1087 (Gold). Historical analysis stays correct.

**Type 3 — previous-value column:**

```sql
ALTER TABLE dim_customer ADD COLUMN previous_loyalty_tier VARCHAR(20);

UPDATE dim_customer
SET previous_loyalty_tier = loyalty_tier,
    loyalty_tier           = 'Gold'
WHERE customer_id = 'C-42';
```

Result: one row with `loyalty_tier = 'Gold'` and `previous_loyalty_tier = 'Silver'`. Compact — but if Emma later becomes Platinum, the Silver history vanishes.

## In the real world

E-commerce companies use SCD Type 2 constantly for their customer dimension. Suppose an online retailer wants to answer: "How much did customers spend *before* and *after* upgrading to Gold tier?" Without Type 2, that question is unanswerable — the old tier is gone. With Type 2, the analyst filters `fact_orders` on the date range and joins to the correct historical dimension row using the surrogate key. The correct tier-at-time-of-purchase is preserved.

A concrete example: a major retail analytics team might have a `dim_product` table where a product's department changes (e.g., a blender moves from "Appliances" to "Kitchen"). With Type 2, they can correctly attribute historical sales to the *original* department for year-over-year comparisons, rather than silently re-categorising the past.

## Common misconceptions

**People think "slowly" means the change happens rarely — actually** it just means the change is gradual and not in every transaction. A customer's city might change once in ten years; a product price might change weekly. "Slowly" is relative to fact-table events (which happen by the millions). Both can be SCDs.

**People think you should always use Type 2 — actually** Type 1 is correct when history genuinely does not matter. Fixing a misspelled name, correcting a wrong phone number — these are data-quality fixes, not business events. Using Type 2 for typo corrections bloats the table and confuses analysts with "two Emmas."

**People think the `customer_id` is the key you join on in the fact table — actually** in a Type 2 dimension you must join on the **surrogate key** (`customer_key`), not the natural business ID. If you join on `customer_id`, you will get multiple rows back (one per version) and produce duplicated or incorrect aggregations. This is one of the most common query bugs in warehouses.

## How it relates & differs

| Concept | How it RELATES | How it DIFFERS |
|---|---|---|
| [[star-schema\|Star Schema]] | SCDs live inside the dimension tables of a star schema. Type 2 is the standard way a star schema handles change over time. | The star schema is the *structure* (fact + dimension tables); SCD is the *strategy* for what happens when dimension data changes. |
| [[normalization-vs-denormalization\|Normalization vs Denormalization]] | Type 2 dimensions are intentionally denormalised — you duplicate rows instead of pointing to a separate history table. | Normalisation avoids redundancy; Type 2 *embraces* controlled redundancy to make historical queries fast and simple. |
| [[tables-keys-sql-basics\|Tables, Keys & SQL Basics]] | SCD Type 2 depends on surrogate keys (system-generated integers) to uniquely identify each version of a row, separate from the natural business ID. | The SQL basics concept teaches keys as identifiers; SCDs extend that by making you think about *which* key the fact table should store — the surrogate, not the natural key. |

## Why you'd use it (and when not to)

**Use Type 2** when historical accuracy of dimension attributes is business-critical — loyalty tiers, pricing bands, sales territories, job titles. Any report that asks "what was the value at the time of the event?" needs Type 2. The trade-off is a larger dimension table and more complex ETL logic to open and close rows correctly.

**Use Type 1** when the attribute change is a correction, not a real-world event, or when no downstream report ever needs the old value. This is simpler and keeps the table small.

**Use Type 3** sparingly — only when you need exactly one previous value and you are sure you will never need more than one step of history. It is a compromise that satisfies almost nobody in practice.

Avoid Type 2 if your dimension changes extremely frequently (e.g., a product price updated hourly) — at that point the dimension has effectively become a fact and should be modelled differently, perhaps as a **Type 4** history table or a time-series fact.

## Check yourself

**Memory hook:** *"Type 1 forgets, Type 2 remembers everything, Type 3 only remembers yesterday."*

**Q1. A customer's email address was entered incorrectly. You fix the typo. Which SCD type should you use, and why?**
Type 1. This is a data-quality correction, not a real business event. The old misspelled email never represented a true state you need to analyse historically. Overwriting is correct.

**Q2. A warehouse uses Type 2 for `dim_customer`. Emma (customer_id = C-42) now has two rows with surrogate keys 1001 and 1087. An analyst runs `SELECT SUM(amount) FROM fact_orders WHERE customer_id = 'C-42'` by joining `dim_customer` on `customer_id`. What goes wrong?**
The join matches both dimension rows for Emma, so every fact row for Emma is duplicated in the result set. The `SUM` comes out roughly double the correct answer. The analyst must join on the surrogate key (`customer_key`) instead — each fact row stores exactly one surrogate key, so no duplication occurs.

**Q3. What are the three pieces of metadata you typically add to a dimension row to implement Type 2?**
`effective_date` (when this version became active), `expiry_date` (when it was superseded — often set to a far-future sentinel like `9999-12-31` for the current row), and `is_current` (a boolean flag making it easy to filter to the latest version without comparing dates).

## Connects to

[[star-schema|Star Schema]] · [[normalization-vs-denormalization|Normalization vs Denormalization]] · [[tables-keys-sql-basics|Tables, Keys & SQL Basics]] · [[batch-vs-streaming|Batch vs Streaming]] · [[idempotency|Idempotency]]