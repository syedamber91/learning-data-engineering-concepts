---
title: "Normalization vs Denormalization"
area: "Data Modeling"
topic: "Warehouse Modeling"
tags: [normalization, denormalization, warehouse-modeling, sql, data-modeling, performance]
---

# Normalization vs Denormalization

*Part of [[warehouse-modeling-moc|Warehouse Modeling]] · [[data-modeling-moc|Data Modeling]]*

## In one line

Normalization stores each fact exactly once across multiple tables to keep data clean; denormalization deliberately copies facts into fewer, wider tables so that reading that data is faster.

## Picture this

Imagine a school office that keeps student records. The normalized version has three separate binders: one for students (name, grade level), one for classes (class name, teacher), and one for enrollments (which student is in which class). If a teacher's name changes, you update it in exactly one place — the classes binder — and every enrollment instantly reflects that.

Now imagine the lazy-but-fast version: one giant spreadsheet with every enrollment as a row, and each row repeats the student's name, grade level, class name, and teacher name. Finding all of Sarah's classes is instant — just filter her rows. But if Ms. Johnson changes her name, you have to find and fix every single row that mentions her. That giant spreadsheet is the denormalized version.

The school office metaphor captures the core tension: **separate binders = safe and consistent; one giant spreadsheet = fast to read, risky to update.**

## How it actually works

**Normalization** is a set of rules (called "normal forms," usually 1NF through 3NF) for splitting a table into smaller, more focused tables so that every piece of information lives in exactly one place. The mechanism is **foreign keys**: instead of copying a customer's name into every order row, you store a `customer_id` number. When you need the name, the database follows that ID to the `customers` table — a process called a **JOIN** (combining rows from two tables based on a matching column).

Why does this matter? Because if a customer changes their name, you update one row in `customers` and every order automatically reflects the new name. Without normalization you'd have an **update anomaly**: one piece of reality stored in a thousand places that can get out of sync.

**Denormalization** reverses this deliberately. You take the joined result — customer name sitting right next to the order — and store it that way permanently. When an analyst queries "show me all orders with the customer name," the database does not need to consult two tables; it reads one. For data warehouses that run thousands of complex analytical queries per hour, cutting out joins can shave seconds off query time.

The key insight is that the two goals — **safe writes** and **fast reads** — pull in opposite directions. Operational databases (the ones your app writes to constantly) favour normalization because correctness matters more than query speed. Data warehouses (the ones analysts read from) favour denormalization because no one is updating those historical rows anyway.

## Worked example

Suppose you run an online bookshop with 1,000,000 orders and 50,000 customers.

**Normalized schema (two tables):**

```sql
-- customers table: 50,000 rows, one per customer
CREATE TABLE customers (
    customer_id   INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email         VARCHAR(150)
);

-- orders table: 1,000,000 rows, references customers by ID
CREATE TABLE orders (
    order_id    INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    book_title  VARCHAR(200),
    total_amount DECIMAL(8,2),
    order_date  DATE
);
```

To get orders with customer names you must JOIN:

```sql
SELECT o.order_id, c.customer_name, o.book_title, o.total_amount
FROM   orders o
JOIN   customers c ON o.customer_id = c.customer_id
WHERE  o.order_date = '2025-12-01';
```

The database reads both tables and matches rows on `customer_id`. With 1,000,000 order rows and 50,000 customer rows, a full JOIN touches up to 1,050,000 rows even before filtering.

**Denormalized schema (one wide table):**

```sql
-- orders_wide: 1,000,000 rows, customer name copied in
CREATE TABLE orders_wide (
    order_id      INT PRIMARY KEY,
    customer_name VARCHAR(100),   -- duplicated from customers
    email         VARCHAR(150),   -- duplicated from customers
    book_title    VARCHAR(200),
    total_amount  DECIMAL(8,2),
    order_date    DATE
);
```

```sql
SELECT order_id, customer_name, book_title, total_amount
FROM   orders_wide
WHERE  order_date = '2025-12-01';
```

No JOIN. The database scans one table. The cost: `customer_name` (≈ 20 bytes) + `email` (≈ 30 bytes) copied into every order row = 50 bytes × 1,000,000 rows = **50 MB of extra storage** — a small price in a modern warehouse but a real one.

If a customer corrects a typo in their email, the normalized version fixes 1 row. The denormalized version must update every one of their order rows — potentially hundreds of writes instead of one.

## In the real world

Spotify's data warehouse tracks hundreds of millions of song plays per day. When a data analyst asks "how many times was each artist's music played in Brazil last month, broken down by subscription tier?", that query joins play events, users, artists, and subscription records. Running this query against a fully normalized schema at that scale would require joining four tables with hundreds of millions of rows — queries that could take minutes.

Instead, Spotify's warehouse team builds a denormalized **fact table** for plays: each row contains `user_country`, `subscription_tier`, `artist_name`, and `play_count` already baked in. Analysts get answers in seconds. The trade-off is accepted because nobody is updating historical play records — they are facts locked in the past.

This pattern — denormalized fact tables — is the foundation of the [[star-schema|Star Schema]], which is the most common design in modern data warehouses.

## Common misconceptions

**People think denormalization is sloppy or wrong — actually it is a deliberate engineering decision.** Denormalization has a bad reputation because redundancy causes bugs in application databases. In a data warehouse, where rows are written once and never updated, the risk of update anomalies disappears entirely, and the read-speed benefit is real.

**People think normalization is mainly about saving disk space — actually its primary goal is preventing inconsistent data.** Storage is a side benefit. The real reason to normalize is so that one fact (a customer's email address) can never be "true" in one row and "false" in another because someone forgot to update all the copies.

**People think you must choose one or the other for an entire system — actually most production systems mix both.** A company typically uses a normalized operational database (so the app writes safely) and a separate denormalized warehouse (so analysts read fast). The data moves from one to the other through a pipeline — that hand-off is what data engineering is largely about.

## How it relates & differs

| Concept | Relates to | Differs from |
|---|---|---|
| [[star-schema\|Star Schema]] | Star schemas are the most common warehouse denormalization pattern — fact tables are denormalized, dimension tables are semi-normalized | A star schema is a specific *blueprint*; normalization/denormalization is the underlying *principle* that blueprint applies |
| [[tables-keys-sql-basics\|Tables, Keys & SQL Basics]] | Normalization is built on primary keys and foreign keys — it cannot exist without them | Keys are the mechanism; normalization is the design strategy that uses them |
| [[indexing\|Indexing]] | Both indexing and denormalization aim to speed up reads | An index adds a separate lookup structure to an existing table; denormalization changes the table's shape so fewer tables need to be touched at all |

## Why you'd use it (and when not to)

Use normalization in any system where the same data will be **written and updated frequently** — your app's database, a CRM, an inventory system. The guarantee that every fact lives in one place is worth the cost of joins, because correctness is non-negotiable.

Use denormalization when **reads vastly outnumber writes** and the data is largely historical or append-only — reporting databases, analytics warehouses, dashboards. Denormalize only the data that actually needs to be fast; not everything needs to be flattened. Avoid denormalizing an operational database: the moment two copies of the same fact get out of sync, you have a data quality incident.

## Check yourself

**Memory hook:** *Normalize to protect your writes; denormalize to speed your reads.*

**Q1 — What problem does normalization solve?**
It ensures that every fact is stored exactly once, so updates and deletes cannot leave the database in a contradictory state (where the same customer has two different email addresses in different rows).

**Q2 — Why would a data warehouse choose denormalization even though it creates redundancy?**
Because warehouse tables are written once (historical records) and read many times by analysts. Redundancy risk is low; the performance gain from eliminating joins on hundreds of millions of rows is high.

**Q3 — If a customer changes their email address in a denormalized orders table with 500 rows for that customer, how many rows must be updated? What about in a normalized schema?**
In the denormalized table: all 500 rows. In the normalized schema: exactly 1 row (in the `customers` table), and every order instantly reflects the change via the foreign key.

## Connects to

[[tables-keys-sql-basics|Tables, Keys & SQL Basics]] · [[star-schema|Star Schema]] · [[slowly-changing-dimensions|Slowly Changing Dimensions]] · [[indexing|Indexing]] · [[transactions-acid|Transactions & ACID]] · [[data-quality-validation|Data Quality & Validation]]