---
title: "Slowly Changing Dimensions"
area: "Data Modeling"
topic: "Warehouse Modeling"
tags: [slowly-changing-dimensions, scd, data-warehouse, dimension-tables, data-modeling, history]
---

# Slowly Changing Dimensions

*Part of [[warehouse-modeling-moc|Warehouse Modeling]] · [[data-modeling-moc|Data Modeling]]*

← Prev: [[star-schema|Star Schema]] · Next: [[normalization-vs-denormalization|Normalization vs Denormalization]] →

## Recap — where we just were

In [[star-schema|Star Schema]] you learned how a data warehouse splits tables into a central fact table (the numbers) surrounded by dimension tables (the descriptions). That design assumes dimensions are stable: a product's name, a customer's city, a store's region. But the real world changes — customers move, products get re-categorised, employees change job titles. The moment a dimension attribute changes, you face a choice the star schema blueprint does not answer for you: do you erase the old value, keep it alongside the new one, or do something in between? That is exactly the problem Slowly Changing Dimensions solve.

---

## Level 1 — The Big Idea

A **Slowly Changing Dimension (SCD)** is a dimension whose attributes change occasionally — not every millisecond, not never, but slowly over time. The word "slowly" matters: we are not talking about a stock price that changes thousands of times a day; we are talking about a customer who moves house once every few years.

The core design challenge is: **when an attribute changes, should the old value survive or disappear?**

Three numbered techniques answer this differently:

- **Type 1** — overwrite the old value. Simple. No history.
- **Type 2** — add a new row. Full history, more complexity.
- **Type 3** — add a new column for the previous value. Limited history, minimal complexity.

**Everyday analogy:** Imagine your school yearbook caption changes when a classmate gets a new preferred name. The school has three choices: **reprint** the old caption (Type 1 — new name only, old name gone); **add a new page** with the new name and a date, leaving the old page intact (Type 2 — both versions exist); or **stick a sticker** over the old name with the new one, writing the old name in small print underneath (Type 3 — current name plus one prior name, side by side).

<!-- mermaid-source:
graph TD
    C[Dimension attribute changes]
    C --> T1[Type 1 - Overwrite - no history kept]
    C --> T2[Type 2 - New row added - full history kept]
    C --> T3[Type 3 - New column added - one prior value kept]
-->
![[slowly-changing-dimensions-d1.svg]]

---

## Level 2 — How It Actually Works

Now that you have the three strategies, let's open each one and see what physically happens to the database table.

### Type 1 — Overwrite

You run a plain `UPDATE`. The old value is **destroyed**.

<!-- mermaid-source:
graph LR
    B[Before: city = London] --> U[UPDATE SET city = Paris]
    U --> A[After: city = Paris - London is gone forever]
-->
![[slowly-changing-dimensions-d2.svg]]

Every historical fact row that ever joined to this dimension row will now *retroactively* read "Paris" — even the orders placed years ago when the customer lived in London. History is silently rewritten.

**Use it when:** the change is a correction (a typo in a product name) or when history is genuinely irrelevant (a customer's latest contact email address — you only care about the current one).

---

### Type 2 — Add a new row

When a value changes, you perform a two-step operation:

1. **Expire** the current row — set `is_current = false` and record an `expiry_date`.
2. **Insert** a brand-new row with a **new surrogate key**, the new attribute value, `effective_date = today`, and `is_current = true`.

Old fact rows still point to the old surrogate key (e.g., `customer_key = 10`, city = London). New fact rows point to the new surrogate key (e.g., `customer_key = 15`, city = Paris). The fact table never changes; history is perfectly preserved.

<!-- mermaid-source:
graph TD
    D1[dim_customer - key=10 - London - is_current: false]
    D2[dim_customer - key=15 - Paris - is_current: true]
    F1[Old fact rows - joined to key=10 - London]
    F2[New fact rows - joined to key=15 - Paris]
    F1 --> D1
    F2 --> D2
-->
![[slowly-changing-dimensions-d3.svg]]

**Use it when:** historical accuracy matters — e.g., you must know which region a customer was in *at the time of purchase*, not today.

---

### Type 3 — Previous value column

You add one extra column — `prev_city` — beside the existing `city` column. When a change arrives, the current value moves to `prev_city` and the new value fills `city`.

<!-- mermaid-source:
graph LR
    B[Before: city=London - prev_city=null] --> U[Alice moves to Paris]
    U --> A[After: city=Paris - prev_city=London]
-->
![[slowly-changing-dimensions-d4.svg]]

**Use it when:** you need a simple before/after comparison for exactly one change cycle, and you know only one level of history is ever needed.

**The hard limit:** if Alice moves again — say, from Paris to Berlin — London is overwritten in `prev_city` and is permanently lost. Type 3 cannot track a full history.

---

## Level 3 — See It with Real Numbers

**Scenario:** `dim_customer` has one row for Alice. She lives in London. On 2025-03-01 she moves to Paris. Watch what each type does.

**Starting table (all three types start here):**

| customer_key | name  | city   |
|---|---|---|
| 10           | Alice | London |

---

**Type 1 — after the move:**

```sql
UPDATE dim_customer
SET    city = 'Paris'
WHERE  customer_key = 10;
```

| customer_key | name  | city  |
|---|---|---|
| 10           | Alice | Paris |

London is gone. Every historical sales row that joined to `customer_key = 10` now reads Paris — even orders placed in 2022.

---

**Type 2 — after the move:**

```sql
-- Step 1: expire the old row
UPDATE dim_customer
SET    is_current  = false,
       expiry_date = '2025-02-28'
WHERE  customer_key = 10;

-- Step 2: insert the current row with a new key
INSERT INTO dim_customer
       (customer_key, name, city, effective_date, expiry_date, is_current)
VALUES (15, 'Alice', 'Paris', '2025-03-01', '9999-12-31', true);
```

| customer_key | name  | city   | effective_date | expiry_date | is_current |
|---|---|---|---|---|---|
| 10           | Alice | London | 2024-01-01     | 2025-02-28  | false      |
| 15           | Alice | Paris  | 2025-03-01     | 9999-12-31  | true       |

Old fact rows still point to key 10 (London). New fact rows point to key 15 (Paris). No historical value is lost.

---

**Type 3 — after the move:**

```sql
UPDATE dim_customer
SET    prev_city = city,
       city      = 'Paris'
WHERE  customer_key = 10;
```

| customer_key | name  | city  | prev_city |
|---|---|---|---|
| 10           | Alice | Paris | London    |

One prior value is visible. A second move would erase London.

---

## Level 4 — In the Real World & Common Traps

**Real-world use case:** A global e-commerce company needs to answer "What were sales by shipping region, per quarter, for the last three years?" Customers occasionally move between countries. Using **Type 2** means that orders placed when Alice lived in the UK are permanently attributed to the UK, while her orders after moving to France are attributed to France — giving the finance team a historically accurate regional breakdown for any quarter. Using Type 1 would silently re-attribute all of Alice's past UK orders to France the moment she moved, corrupting every historical report without a single error message.

---

**Misconceptions:**

**People think: "Type 2 is always the right answer."**
Actually: Type 2 is the most powerful option, but it carries real costs. Every query for "current" customers must filter `WHERE is_current = true`, or you will double-count every customer who has ever moved. The dimension table also grows a new row for every change — a customer who moves 10 times has 11 rows. Choose Type 2 only when historical accuracy on that specific attribute genuinely matters.

**People think: "You can upgrade a Type 1 dimension to Type 2 later if you need history."**
Actually: Once you have been overwriting values for months, the historical record is destroyed. You cannot reconstruct what city Alice was in on 2023-07-15 if you never stored it. Switching to Type 2 only captures history *from that point forward*. This is one of the most expensive mistakes in warehouse design — the SCD strategy must be chosen correctly at the start.

**People think: "Type 3 gives you a full audit trail."**
Actually: Type 3 only remembers *one* prior value per attribute. It is not an audit trail. If you need every change with a timestamp — a genuine audit log — Type 2 is the only option among the three classic types.

---

## Level 5 — Expert View

### How the types relate and differ

| Feature | Type 1 | Type 2 | Type 3 |
|---|---|---|---|
| History kept | None | Full | One prior value |
| Table row count grows? | No | Yes — one row per change | No |
| Query complexity | Lowest | Highest | Medium |
| Storage cost | Lowest | Highest | Low |
| Retroactive impact on old facts | Yes | No | Partial |
| Best for | Error corrections | Accurate historical reporting | Simple before/after |

### Trade-offs and edge cases

**When Type 2 becomes expensive:** A dimension attribute that changes very frequently — like a user's "last active" timestamp or a product's real-time stock level — should *never* be Type 2. The table would grow by millions of rows per day. Reserve Type 2 for attributes that change rarely but whose history is business-critical: shipping country, job title, product category.

**Surrogate keys are non-negotiable for Type 2.** You saw in [[star-schema|Star Schema]] that dimensions use a surrogate key (a plain integer) rather than a business key (like a customer's email). Type 2 is the sharpest reason why: Alice gets *two surrogate keys* (10 and 15), each representing a version of herself in time. If the primary key were her email address, you would be forced to store the same email twice and join on a string — fragile, slow, and incorrect.

**Mixed SCDs in practice.** Real warehouses often combine types on a single dimension: most attributes are Type 1 (fix typos silently), while one or two critical attributes — `region`, `pricing_tier` — are Type 2. This keeps table growth manageable while preserving history exactly where it matters.

**Type 2 and indexing:** As a Type 2 dimension grows (a five-year warehouse might have 10× as many rows as active entities), queries that need only current rows suffer unless a **partial index** on `is_current = true` is maintained. Without it, the database scans all expired rows too — turning a fast O(log n) lookup into a slow full scan. This directly applies what you learned in [[indexing|Indexing]].

**Type 2 and atomicity:** The two-step Type 2 operation — expire the old row, insert the new row — must be wrapped in a single transaction. If the INSERT succeeds but the UPDATE to set `is_current = false` fails, you end up with two active rows for the same customer. Every report silently double-counts her. This is a classic [[transactions-acid|Transactions & ACID]] requirement: both steps commit together or neither does.

---

## Check yourself

**Memory hook:** SCDs are a time-machine dial — Type 1 has no dial (overwrite and forget), Type 2 lets you travel back to any point in history, Type 3 only shows you one stop back.

**Q1: A product's SKU was entered with a typo. You fix it. Which SCD type is correct, and why?**
A: Type 1. A typo is an error, not a meaningful historical state. There is no business reason to preserve the misspelled SKU — overwriting it is the right call.

**Q2: Your dimension uses Type 1. An analyst asks: "How many customers were based in Germany when they placed their order in 2023?" Can you answer this accurately?**
A: No. If any of those customers have since moved, their city has been overwritten. The 2023 location no longer exists in the database, so the question cannot be answered accurately.

**Q3: In a Type 2 dimension, Alice has two rows (customer_key 10 — London, expired; customer_key 15 — Paris, current). A new order arrives today. Which surrogate key does the ETL pipeline use when writing the fact row?**
A: customer_key 15 — the row where `is_current = true`. The pipeline must always resolve to the *current* surrogate key at load time, so that the new fact row correctly reflects Alice's present dimension record.

---

## Connects to

[[star-schema|Star Schema]] · [[tables-keys-sql-basics|Tables, Keys & SQL Basics]] · [[indexing|Indexing]] · [[transactions-acid|Transactions & ACID]] · [[normalization-vs-denormalization|Normalization vs Denormalization]]

---

## Coming up next

[[normalization-vs-denormalization|Normalization vs Denormalization]] — you have now seen that a star schema deliberately *copies* attribute values directly into dimension rows (denormalization) instead of splitting them into extra tables. The next lesson digs into the theory behind that trade-off: what normalization is, why it was invented, and precisely when storing redundant data is the *right* engineering choice rather than a mistake.