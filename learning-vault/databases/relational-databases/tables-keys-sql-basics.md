---
title: "Tables, Keys & SQL Basics"
area: "Databases"
topic: "Relational Databases"
tags: [sql, relational-databases, primary-key, foreign-key, data-engineering, databases]
---

# Tables, Keys & SQL Basics

*Part of [[relational-databases-moc|Relational Databases]] · [[databases-moc|Databases]]*

← Prev: [[big-o-time-complexity|Big-O / Time Complexity]] · Next: [[indexing|Indexing]] →

## Recap — where we just were

In [[big-o-time-complexity|Big-O / Time Complexity]] you learned to read the efficiency grade on any algorithm — O(1) for instant lookups, O(n) for linear scans, and the logarithmic O(log n) trick that powers binary search. You even spotted that database indexes use exactly that halving trick under the hood. Now we step inside the database itself to understand what is actually *being* indexed: **tables**, the rows and columns inside them, and **SQL**, the language you use to ask questions of the data.

---

## Level 1 — The big idea

A **relational database** is a system that stores data in **tables** — grids of rows and columns, like a very strict spreadsheet — and lets you link those tables together using shared keys. **SQL** (Structured Query Language) is the plain-English-ish language you use to read, add, change, or remove that data.

**Everyday analogy:** Imagine a school's filing cabinet. One drawer holds one index card per student (name, student ID, year). A second drawer holds one card per class enrolment, with the student ID written on it so you know who enrolled. The student ID is the link between the two drawers. A relational database is that filing cabinet, turbocharged to handle millions of cards and answer queries in milliseconds.

<!-- mermaid-source:
graph TD
    DB[Relational Database] --> T1[customers table]
    DB --> T2[orders table]
    T1 --> R1[id=1 Alice]
    T1 --> R2[id=2 Bob]
    T2 --> O1[order 101 belongs to customer 1]
    T2 --> O2[order 102 belongs to customer 2]
-->
![[tables-keys-sql-basics-d1.svg]]

The key insight: instead of one giant blob of data, you split information into focused tables and connect them with shared values. That discipline is exactly what the word *relational* means.

---

## Level 2 — How it actually works

Now that you have the picture, let's trace three core building blocks: **columns and rows**, **primary keys**, and **foreign keys**.

### Columns and rows

Every table has a fixed set of **columns** (the headings — what kind of thing is stored) and a growing set of **rows** (one record per real-world entity). Columns have a **data type** such as `INTEGER`, `TEXT`, or `DECIMAL`. The database enforces those types, so a phone-number column can never accidentally store a date.

<!-- mermaid-source:
graph TD
    T[customers table] --> COLS[Columns define the shape]
    T --> ROWS[Rows hold the data]
    COLS --> C1[customer_id INTEGER]
    COLS --> C2[name TEXT]
    COLS --> C3[email TEXT]
    ROWS --> R1[Row 1 - id 1 Alice alice@ex.com]
    ROWS --> R2[Row 2 - id 2 Bob bob@ex.com]
-->
![[tables-keys-sql-basics-d2.svg]]

### Primary key — the row's fingerprint

A **primary key** (PK) is a column whose value is **unique for every row** and **never null**. It is the row's fingerprint — no two rows may share it.

Why does uniqueness matter? Because every other table that wants to *reference* a customer needs a reliable, unambiguous way to say "I mean *this exact* customer, and no other." If two customers could share the same ID, that reference would be ambiguous and the whole system would break down.

Most databases let you declare `PRIMARY KEY` on a column and then automatically reject any duplicate insert attempt.

### Foreign key — the bridge between tables

A **foreign key** (FK) is a column in one table whose values must match the primary key of *another* table. It is the bridge that makes databases *relational*.

<!-- mermaid-source:
graph LR
    customers -->|customer_id is PK| PK_label[unique identifier per customer]
    orders -->|order_id is PK| PK2_label[unique identifier per order]
    orders -->|customer_id is FK - points to| customers
-->
![[tables-keys-sql-basics-d3.svg]]

The database enforces **referential integrity** — a guarantee that your references are always valid: you cannot insert an order with `customer_id = 99` if no customer with ID 99 exists. This prevents *orphan records*, which are rows that reference something that no longer exists.

### SQL: the four core commands

SQL lets you do four things to data, often remembered as **CRUD**:

| SQL keyword | What it does | Human translation |
|---|---|---|
| `SELECT` | Read rows | "Give me data" |
| `INSERT` | Add a new row | "Store this" |
| `UPDATE` | Change existing rows | "Fix this" |
| `DELETE` | Remove rows | "Forget this" |

<!-- mermaid-source:
graph LR
    SQL[SQL] --> S[SELECT - read data]
    SQL --> I[INSERT - add a row]
    SQL --> U[UPDATE - modify rows]
    SQL --> D[DELETE - remove rows]
-->
![[tables-keys-sql-basics-d4.svg]]

Every data engineering pipeline you will ever build uses these four verbs. They are the vocabulary of every database conversation.

---

## Level 3 — See it with real numbers

Imagine a tiny e-commerce store. It has two tables.

**customers** — 3 rows:

| customer_id | name  | email             |
|-------------|-------|-------------------|
| 1           | Alice | alice@example.com |
| 2           | Bob   | bob@example.com   |
| 3           | Carla | carla@example.com |

**orders** — 5 rows:

| order_id | customer_id | total  |
|----------|-------------|--------|
| 101      | 1           | 49.99  |
| 102      | 2           | 19.50  |
| 103      | 1           | 89.00  |
| 104      | 3           | 5.00   |
| 105      | 1           | 120.00 |

`customer_id` in `orders` is a foreign key — it points to `customer_id` in `customers`. Notice that Alice (id 1) has three orders, Bob one, and Carla one. Now let's run all four SQL commands against this data:

```sql
-- SELECT: find all orders placed by Alice (customer_id = 1)
SELECT order_id, total
FROM orders
WHERE customer_id = 1;
-- Result: rows 101 ($49.99), 103 ($89.00), 105 ($120.00)

-- INSERT: add a new customer
INSERT INTO customers (customer_id, name, email)
VALUES (4, 'David', 'david@example.com');
-- customers now has 4 rows

-- UPDATE: Alice changed her email address
UPDATE customers
SET email = 'alice@newdomain.com'
WHERE customer_id = 1;
-- Only Alice's row changes; Bob and Carla are untouched

-- DELETE: remove a cancelled order
DELETE FROM orders
WHERE order_id = 104;
-- orders now has 4 rows; Carla's $5.00 order is gone
```

**JOIN — the relational superpower.** The real power shows up when you read from *two tables at once* using a `JOIN`:

```sql
-- Show customer names alongside their orders
SELECT customers.name, orders.order_id, orders.total
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id;
```

Result:

| name  | order_id | total  |
|-------|----------|--------|
| Alice | 101      | 49.99  |
| Bob   | 102      | 19.50  |
| Alice | 103      | 89.00  |
| Alice | 105      | 120.00 |

The database matched every row in `orders` to the `customers` row with the same `customer_id`. That matching step is exactly where [[indexing|Indexing]] becomes critical — without an index, the database has to scan every customer row for every single order row, an O(n²) operation you now know is catastrophic at scale.

---

## Level 4 — In the real world & common traps

### Named real-world use case

Think of **Shopify's order management system**. Every merchant store has a `customers` table (millions of rows), an `orders` table (tens of millions of rows), a `products` table, and a `line_items` table connecting orders to the specific products purchased. When a customer checks out, one `INSERT` lands in `orders` and one `INSERT` per product lands in `line_items`. When the merchant opens their dashboard, a `SELECT ... JOIN` assembles the full order summary in milliseconds. Foreign keys ensure no order can reference a deleted product, and primary keys ensure no two orders ever collide — even when thousands of customers are checking out simultaneously.

### Common misconceptions

**People think:** "A spreadsheet and a database table are basically the same thing."
**Actually:** A spreadsheet lets any cell hold any value at any time, and it breaks under concurrent edits. A database table enforces column types, primary key uniqueness, foreign key constraints, and handles thousands of simultaneous users without data corruption. The discipline is the point — the restrictions are features, not limitations.

**People think:** "SQL is just for reading data — SELECT is the important one."
**Actually:** `INSERT`, `UPDATE`, and `DELETE` are equally critical. Every pipeline that *loads* data into a warehouse uses `INSERT`; every system that keeps records current uses `UPDATE`; and `DELETE` (or soft-delete patterns) prevents tables from growing without bound. `SELECT` is the window you look through; the other three are the machinery that keeps the warehouse stocked.

**People think:** "If I put all my data in one big table I won't need to deal with foreign keys or JOINs."
**Actually:** This is called **denormalization** — sometimes an intentional, useful choice (you will study the trade-off in [[normalization-vs-denormalization|Normalization vs Denormalization]]) but more often a slow-motion disaster. Alice's name would be repeated on every one of her 1,000 orders. Change her email once and you have to update 1,000 rows instead of one — and if you miss even one row, your data is now inconsistent. Splitting into related tables is not bureaucracy; it is how you keep data trustworthy.

---

## Level 5 — Expert view

### How this relates to — and differs from — neighbouring concepts

| Concept | What it shares with Tables & SQL | Key difference |
|---|---|---|
| [[arrays-hash-maps|Arrays & Hash Maps]] | Both store collections of items you can query | Arrays live in program memory and vanish when the program ends; tables persist to disk, survive restarts, and are shared across many programs and users simultaneously |
| [[big-o-time-complexity|Big-O / Time Complexity]] | A JOIN without an index is an O(n²) nested-loop scan | Big-O grades the algorithm; the table structure determines *which* algorithm the database is forced to use |
| [[indexing|Indexing]] | Both are core database mechanics | Tables define *what* data exists; indexes define *how fast* the database can find it — an index on `customer_id` turns the JOIN above from O(n²) to O(log n) |
| [[transactions-acid|Transactions & ACID]] | Both operate on the same tables | ACID wraps SQL commands in a safety guarantee: either all of them succeed or none of them do — table rules alone cannot protect you if power cuts out mid-INSERT |

### Trade-offs and edge cases

**When relational tables shine:**
Data has clear relationships (customers → orders → products), you need to enforce integrity (no orphan records, no duplicate IDs), and queries are ad hoc — SQL is flexible enough to answer questions you have not thought of yet.

**When to be careful:**
- Deeply nested JOINs across many large tables hit O(n²) performance without careful indexing. The database can only be as fast as the algorithm it can choose, and no amount of hardware fixes a missing index.
- Very wide tables — hundreds of columns — become difficult to maintain. Adding a column to a billion-row table can lock the entire table for minutes.
- If every query always reads the same pre-joined shape, a [[star-schema|Star Schema]] or a pre-aggregated model may be far faster than rerunning the same JOIN millions of times per day.

**The NULL trap — an expert-level gotcha:** SQL uses three-valued logic: TRUE, FALSE, and NULL (meaning "unknown"). `WHERE email = NULL` never returns any rows, because NULL is not equal to anything — not even to itself. You must write `WHERE email IS NULL`. This surprises almost every beginner and is responsible for a disproportionate share of subtle data bugs in production systems.

---

## Check yourself

**Memory hook:** "Tables store the facts, keys make the connections, SQL asks the questions."

**Q1: What is the purpose of a primary key, and what two rules must it always obey?**
A: A primary key uniquely identifies each row in a table. It must be unique (no two rows share the same value) and never null. It is the row's unambiguous fingerprint.

**Q2: Alice's `customer_id` is 1 in the `customers` table, and the `orders` table has a `customer_id` column pointing back to her. What is that column in `orders` called, and what does the database refuse to let you do because of it?**
A: It is a **foreign key**. The database refuses to insert any order with a `customer_id` that does not exist in the `customers` table, preventing orphan records that reference nothing real.

**Q3: You run `DELETE FROM orders WHERE customer_id = 2` against the Level 3 data. How many rows are deleted, and which ones survive?**
A: Exactly one row is deleted — order 102 (Bob's only order, $19.50). All four of Alice's remaining orders and Carla's order survive untouched because their `customer_id` values are not 2.

---

## Connects to

[[arrays-hash-maps|Arrays & Hash Maps]] · [[big-o-time-complexity|Big-O / Time Complexity]] · [[indexing|Indexing]] · [[transactions-acid|Transactions & ACID]] · [[normalization-vs-denormalization|Normalization vs Denormalization]] · [[star-schema|Star Schema]]

---

## Coming up next

**[[indexing|Indexing]]** — Now that you know what a table is and how a JOIN works, you will discover why matching rows across two million-row tables without the right structure can grind a server to a halt, and how a **B-tree** index slices that cost from O(n²) down to O(log n) — exactly the halving trick that Big-O promised was coming.