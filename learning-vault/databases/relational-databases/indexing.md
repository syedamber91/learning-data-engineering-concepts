---
title: "Indexing"
area: "Databases"
topic: "Relational Databases"
tags: [indexing, sql, performance, databases, query-optimization, relational-databases]
---

# Indexing

*Part of [[relational-databases-moc|Relational Databases]] · [[databases-moc|Databases]]*

## In one line

An index is a separate, sorted lookup structure the database builds on one or more columns so it can find matching rows in milliseconds instead of reading every single row in the table.

## Picture this

Imagine you are holding a 1,000-page chemistry textbook and someone asks you to find every mention of "sodium." Without an index, you flip through every page — that is a **full table scan**. With the index at the back of the book, you look up "sodium," see "pages 47, 312, 789," and jump straight there. You read three pages instead of one thousand.

A database index works exactly like that back-of-book index: it is a sorted list of values from one column, each entry pointing to the physical location of the matching row. The database uses that list to skip directly to what you need.

## How it actually works

When you create an index on a column, the database engine builds a separate data structure — almost always a **B-tree** (a self-balancing sorted tree, think of it as a very efficient sorted list you can search in logarithmic time) — that stores the indexed column's values in sorted order, each paired with a pointer to the full row on disk.

**The read path (fast):** You run `SELECT * FROM orders WHERE customer_id = 42`. Without an index the engine reads every row in `orders` to check `customer_id`. With an index on `customer_id`, the engine walks the B-tree — start at the root, go left or right based on whether 42 is smaller or larger than the current node's value, repeat — and reaches the matching entries in roughly log₂(n) comparisons. For a million-row table that is around 20 comparisons instead of 1,000,000. It then follows the pointers to fetch only those rows.

**The write path (slower):** Every `INSERT`, `UPDATE`, or `DELETE` now has two jobs: change the data in the main table *and* update every index that covers the changed columns. If you add an order for customer 42, the engine inserts the row in the table *and* inserts an entry into the `customer_id` index, re-balancing the B-tree if needed. More indexes = more maintenance work on every write.

**Selectivity matters:** An index on a column with only two values (`gender = 'M'` or `'F'`) saves almost nothing — the engine still has to read half the table. An index on `email` (nearly unique for every row) is extremely useful. High selectivity (many distinct values) = valuable index.

**Composite indexes:** You can index multiple columns together, e.g., `(customer_id, order_date)`. The database can use this index for queries that filter on `customer_id` alone, or on `customer_id` AND `order_date` together — but NOT on `order_date` alone (it is like an index sorted first by last name, then by first name: "Smith, Alice" is easy to find; finding everyone named "Alice" still requires reading the whole index).

## Worked example

Suppose we have an `orders` table with 1,000,000 rows:

```sql
CREATE TABLE orders (
    order_id    BIGINT PRIMARY KEY,
    customer_id INT,
    order_date  DATE,
    total       DECIMAL(10,2)
);
```

**Without an index — slow:**

```sql
SELECT * FROM orders WHERE customer_id = 42;
```

The engine performs a full table scan: it reads all 1,000,000 rows, checks each `customer_id`, and returns the ~200 rows that match. On a typical disk, that might take 2–5 seconds.

**Adding the index:**

```sql
CREATE INDEX idx_orders_customer ON orders (customer_id);
```

The engine builds a B-tree on `customer_id`. The tree has roughly log₂(1,000,000) ≈ 20 levels. Now the same `SELECT` walks 20 nodes, finds 200 matching pointers, and fetches those 200 rows. Time drops to under 10 milliseconds — a 200–500x speedup.

**The write cost in action:**

```sql
INSERT INTO orders (order_id, customer_id, order_date, total)
VALUES (1000001, 99, '2026-06-22', 149.99);
```

Now the engine must (1) write the new row to the main table and (2) insert `customer_id = 99` into `idx_orders_customer` and rebalance the B-tree. With one index the overhead is small. With ten indexes on the same table, every insert touches eleven data structures.

## In the real world

An e-commerce company like Shopify processes millions of orders. Their support dashboard lets agents search orders by `customer_id`, `status`, and `created_at`. Without indexes on those columns, every search would scan hundreds of millions of rows — pages would time out. With carefully chosen indexes, each lookup returns in under 50 ms. The trade-off: the warehouse team runs millions of `INSERT`s per day, so the team audits indexes quarterly and drops ones that are no longer used by any query, because each dead index still slows down every write for free.

## Common misconceptions

**People think: "More indexes = faster database." — Actually:** Every index you add speeds up reads but slows down every write (`INSERT`/`UPDATE`/`DELETE`) on that table. A table with 15 indexes on a write-heavy workload can be *slower overall* than the same table with 3 well-chosen indexes. Index every column that genuinely needs it, not every column that exists.

**People think: "A composite index on (A, B) works the same as two separate indexes on A and B." — Actually:** A composite index `(A, B)` is most efficient for queries that filter on A first (or A and B together). A query filtering only on B cannot use the leading column, so it may not use the composite index at all. Two separate indexes let each query use the most relevant one, but each has its own write overhead. They are different tools.

**People think: "The database always uses an index if one exists." — Actually:** The query optimizer decides whether using the index is actually faster than a full table scan. If your query matches 80% of the rows, the optimizer knows it is cheaper to scan the table sequentially than to chase 800,000 individual pointers across disk. Indexes help most when queries are *selective* — returning a small fraction of rows.

## How it relates & differs

| Concept | Relates to Indexing | Differs from Indexing |
|---|---|---|
| [[tables-keys-sql-basics\|Tables, Keys & SQL Basics]] | A **primary key** is automatically indexed in most databases; indexes are built on top of the table structure you learn there | Keys define *identity and relationships*; indexes are a *performance tool* layered on top — you can index any column, not just keys |
| [[transactions-acid\|Transactions & ACID]] | Write transactions must update indexes atomically alongside the table to maintain consistency | Transactions govern correctness and durability; indexes govern *speed of access* — they are separate concerns, though both live inside the database engine |
| [[normalization-vs-denormalization\|Normalization vs Denormalization]] | A normalized schema with many tables often needs more indexes to make cross-table joins fast; denormalization reduces joins and may reduce index needs | Normalization is about *how you organize data*; indexing is about *how fast you find it* — you apply indexes to whatever schema you chose, normalized or not |

## Why you'd use it (and when not to)

Use indexes on columns you frequently filter (`WHERE`), join (`JOIN ... ON`), or sort (`ORDER BY`) — especially when those columns have high selectivity and the table is large (thousands of rows or more). Avoid indexes on small tables (a full scan of 500 rows is instantaneous), on columns with very few distinct values (low selectivity), or on columns that are written to constantly but rarely queried. Every index has a storage cost and a write-amplification cost; the payoff only appears when reads actually use it. Audit index usage with your database's built-in tools (`pg_stat_user_indexes` in PostgreSQL, `sys.dm_db_index_usage_stats` in SQL Server) and drop indexes that are never hit.

## Check yourself

**Memory hook:** *"Index = book index: fast to look up, extra work every time the book is revised."*

**Q1: If you add five indexes to a table, what happens to INSERT performance?**
It gets slower. Every insert must update all five index data structures in addition to writing the main row. The more indexes, the more maintenance work per write.

**Q2: You have a column `country` with only 3 distinct values in a 5-million-row table. Should you index it?**
Almost certainly not. With only 3 values each query matches roughly 1.7 million rows — the optimizer will likely prefer a full table scan over chasing that many index pointers. Low-selectivity columns rarely benefit from indexing.

**Q3: A composite index exists on `(last_name, first_name)`. Can a query `WHERE first_name = 'Alice'` use it efficiently?**
No. The index is sorted by `last_name` first; entries for every "Alice" are scattered across the entire index. The database cannot narrow down using `first_name` alone without scanning the whole index — it needs a separate index on `first_name` for that query.

## Connects to

[[tables-keys-sql-basics|Tables, Keys & SQL Basics]] · [[transactions-acid|Transactions & ACID]] · [[normalization-vs-denormalization|Normalization vs Denormalization]] · [[big-o-time-complexity|Big-O / Time Complexity]] · [[data-quality-validation|Data Quality & Validation]]