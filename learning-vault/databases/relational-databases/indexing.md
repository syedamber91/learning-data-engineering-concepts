---
title: "Indexing"
area: "Databases"
topic: "Relational Databases"
tags: [indexing, sql, relational-databases, performance, data-engineering, databases]
---

# Indexing

*Part of [[relational-databases-moc|Relational Databases]] · [[databases-moc|Databases]]*

← Prev: [[tables-keys-sql-basics|Tables, Keys & SQL Basics]] · Next: [[transactions-acid|Transactions & ACID]] →

## Recap — where we just were

In [[tables-keys-sql-basics|Tables, Keys & SQL Basics]] you built your first mental model of a relational database: rows and columns, a primary key that fingerprints every row, a foreign key that bridges two tables, and the four SQL verbs — SELECT, INSERT, UPDATE, DELETE — that talk to all of it. You can now write `SELECT * FROM orders WHERE customer_id = 1`, but you haven't yet asked *how* the database actually finds those rows. Does it read every single row? Does it jump straight to the answer? That question is exactly what this lesson answers.

---

## Level 1 — The big idea

A **database index** is a separate, sorted data structure the database keeps alongside your table. Its single job: let the engine jump straight to matching rows without reading every row in the table.

**Everyday analogy:** Think of the index at the back of a textbook. When you need every page that mentions "foreign key," you don't re-read the whole book — you flip to the index, find "foreign key" in alphabetical order, and see "pages 14, 47, 203." A database index works identically: it's a sorted shortcut that points to the actual data.

<!-- mermaid-source:
graph LR
    Query[Query - filter on email] --> Index[Email index - sorted]
    Index --> RowPtr[Row pointer - page 7 slot 2]
    RowPtr --> Table[customers table - row fetched]
-->
![[indexing-d1.svg]]

Without an index the database must do a **full table scan** — read every row top to bottom, like re-reading the whole textbook. With an index it leaps to the answer in a handful of steps. That leap is the entire story of indexing.

---

## Level 2 — How it actually works

Now that you have the picture, let's trace the mechanism.

### The B-tree: the engine under the index

Most relational databases (PostgreSQL, MySQL, SQLite) store their default indexes in a structure called a **B-tree** (balanced tree). It arranges your indexed values as a tree where each level cuts the remaining candidates roughly in half — exactly the binary-search halving trick from [[big-o-time-complexity|Big-O / Time Complexity]].

<!-- mermaid-source:
graph TD
    Root[Root - split point M] --> Left[Left branch A through L]
    Root --> Right[Right branch N through Z]
    Left --> LL[alice - bob - carol]
    Left --> LR[dave - eve - frank]
    Right --> RL[nina - omar - peter]
    Right --> RR[quinn - rosa - sue]
    LL --> P1[Row pointers on disk]
    LR --> P2[Row pointers on disk]
    RL --> P3[Row pointers on disk]
    RR --> P4[Row pointers on disk]
-->
![[indexing-d2.svg]]

To find a specific value the database starts at the root, asks "is my target before or after the split value here?", follows the correct branch, and repeats — until it reaches a leaf node holding the exact disk address of the row. This is O(log n): doubling the table size adds only one extra step.

### What an index entry stores

Each entry in the index holds two things:
1. **The indexed value** — e.g., `"alice@example.com"`
2. **A row pointer** — the physical address (page number + slot) of that row on disk

The entries are kept in sorted order by the indexed value. That sort order is what makes the binary-search style navigation possible.

### Step-by-step: a query hitting an index

<!-- mermaid-source:
sequenceDiagram
    participant App as Application
    participant DB as Database Engine
    participant Idx as Index on email
    participant Tbl as customers table

    App->>DB: SELECT WHERE email = alice
    DB->>Idx: Binary search for alice
    Idx-->>DB: Found - row at page 4 slot 2
    DB->>Tbl: Fetch page 4 slot 2
    Tbl-->>DB: Row data
    DB-->>App: Result returned
-->
![[indexing-d3.svg]]

Without the index, steps 2 and 3 are replaced by "scan every row in the table one by one." That's fine with 10 rows; catastrophic with 10,000,000.

---

## Level 3 — See it with real numbers

Your `customers` table has **1,000,000 rows**. You run:

```sql
SELECT name, email
FROM customers
WHERE email = 'alice@example.com';
```

**Without an index on `email`:**
- The database reads all 1,000,000 rows, checking each email value.
- Big-O grade: **O(n)** — linear scan.
- At 10,000 rows checked per second: ~100 seconds. The page times out.

**With an index on `email`:**
- A B-tree 20 levels deep can index over 1,000,000 values (2²⁰ = 1,048,576).
- The database follows at most 20 comparisons to reach the row pointer.
- Big-O grade: **O(log n)** — logarithmic.
- Same hardware: sub-millisecond.

Creating the index and verifying it works:

```sql
-- Step 1: create the index (one-time cost)
CREATE INDEX idx_customers_email ON customers(email);

-- Step 2: run the query as normal — the planner picks up the index automatically
SELECT name, email
FROM customers
WHERE email = 'alice@example.com';

-- Step 3: confirm the index was used with EXPLAIN
EXPLAIN SELECT name, email
FROM customers
WHERE email = 'alice@example.com';

-- Good output — index was used:
--   Index Scan using idx_customers_email on customers
--   (cost=0.42..8.44 rows=1 width=40)

-- Bad output — full scan, no index used:
--   Seq Scan on customers
--   (cost=0.00..18340.00 rows=1 width=40)
```

`EXPLAIN` shows the database's execution plan before it runs the query. `Index Scan` means the shortcut was taken. `Seq Scan` (sequential scan) means every row was read — your cue that an index is missing or the planner chose not to use it.

---

## Level 4 — In the real world & common traps

### Real-world use case: customer support at an e-commerce company

Imagine a shop like Amazon with 50 million orders. A customer-service agent types a customer's email address to pull up their order history. Without an index on `orders.customer_email`, the database reads all 50 million rows — the screen shows a spinner for 30 seconds and the agent's call queue grows. With an index, the same query returns in under 10 milliseconds. Indexes are almost always the first thing a data engineer or database administrator checks when a query is reported as slow. The rule of thumb used on real teams: **index columns you frequently filter on (`WHERE`), join on (`JOIN ON`), or sort on (`ORDER BY`).**

### Common misconceptions

**People think: "More indexes = a faster database."**
Actually: every index you add speeds up *reads* but slows down *writes*. On `INSERT`, `UPDATE`, and `DELETE`, the database must update every index covering that row. A write-heavy table with 10 indexes can be slower overall than the same table with 2. Choose indexes surgically, not generously.

**People think: "The database always uses my index."**
Actually: the database's **query planner** — the internal component that decides how to execute a query — estimates whether the index is worth using at all. If a query touches more than roughly 5–10 % of the table anyway (e.g., `WHERE country = 'US'` when 80 % of your users are American), the planner may prefer a full table scan, because jumping to scattered disk locations via the index becomes slower than reading pages in order.

**People think: "An index on column A helps with filtering on column B."**
Actually: an index only accelerates queries that filter, join, or sort on the *exact column(s) indexed*. An index on `email` does nothing for `WHERE name = 'Alice'`. You need a separate index on `name`, or a **composite index** listing both columns — in the right order, which matters.

---

## Level 5 — Expert view

### How indexing relates to and differs from neighbours

| Concept | What it is | Relationship to indexing |
|---|---|---|
| **Full table scan** | Reading every row in order | What indexing replaces for selective queries |
| **B-tree** | The balanced-tree data structure under most indexes | The mechanism giving indexes O(log n) lookup |
| **Hash index** | Alternative index using a hash map | O(1) equality lookup, but cannot handle range queries (`BETWEEN`, `>`, `<`) — no sorted order |
| [[arrays-hash-maps\|Arrays & Hash Maps]] | In-memory data structures | A hash index is the disk-resident cousin of a hash map; same O(1) idea, same range-query blind spot |
| [[big-o-time-complexity\|Big-O / Time Complexity]] | Efficiency grades | Full scan = O(n); index scan = O(log n) — the same contrast you already know, now applied to disk |

### When to add an index

- The column appears frequently in `WHERE`, `JOIN ON`, or `ORDER BY`.
- The column has high **cardinality** — many distinct values (e.g., email address, user ID, order number). An index on a column with only two possible values is nearly useless because the planner will prefer a full scan anyway.
- The table is large. Indexes rarely pay off on tables under a few thousand rows.

### When NOT to add an index

- The table is written to far more often than it is read (e.g., a high-frequency event log). Write overhead may outweigh the read benefit.
- The column has very low cardinality (e.g., `status` with values `'active'` / `'inactive'`).

### Composite indexes and the leftmost-prefix rule

A **composite index** on `(last_name, first_name)` helps a query filtering on `last_name` alone, or on both columns together — but does *not* help a query filtering only on `first_name`. The leftmost column in the index definition must be present in the filter. This "leftmost-prefix rule" is one of the most common index mistakes in production systems.

### Index maintenance

Over time, as rows are inserted and deleted, a B-tree index can become fragmented — like a filing cabinet where folders are scattered across many drawers. Most databases provide an `ANALYZE` or `REINDEX` command to rebuild the index and refresh the planner's statistics about it.

---

## Check yourself

**Memory hook:** *An index is the back-of-book index — flip, find, fetch. Without it, read every page.*

**Q1: Why does adding an index speed up `SELECT` but slow down `INSERT`?**
A1: `SELECT` benefits because the index lets the planner jump to matching rows instead of scanning all of them. `INSERT` is slower because the database must update every index that covers the table — in addition to writing the new row itself.

**Q2: Your `products` table has 2,000,000 rows. A query with `WHERE category = 'Electronics'` returns 800,000 rows (40 % of the table). Would an index on `category` help?**
A2: Probably not. The query planner estimates that fetching 40 % of rows via random index lookups would be slower than reading pages in order with a full table scan. Indexes pay off most when the result set is a tiny fraction of the table.

**Q3: What two output terms from `EXPLAIN` tell you whether an index was used?**
A3: `Index Scan` (or `Index Only Scan`) means the index was used. `Seq Scan` means the engine read the table row by row with no index.

---

## Connects to

[[big-o-time-complexity|Big-O / Time Complexity]] · [[tables-keys-sql-basics|Tables, Keys & SQL Basics]] · [[arrays-hash-maps|Arrays & Hash Maps]] · [[normalization-vs-denormalization|Normalization vs Denormalization]] · [[star-schema|Star Schema]]

---

## Coming up next

[[transactions-acid|Transactions & ACID]] — now that you can find rows fast with indexes, the next question is: what happens when two people try to change the same row at the same moment, or a system crashes halfway through a bank transfer? Transactions and ACID guarantees are the database's answer to that problem.