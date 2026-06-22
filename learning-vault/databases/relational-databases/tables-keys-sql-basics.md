---
title: "Tables, Keys & SQL Basics"
area: "Databases"
topic: "Relational Databases"
tags: [sql, relational-databases, primary-key, foreign-key, data-modeling, querying]
---

# Tables, Keys & SQL Basics

*Part of [[relational-databases-moc|Relational Databases]] · [[databases-moc|Databases]]*

## In one line

A relational database organises data into tables of rows and columns, uses keys to link those tables together, and lets you ask questions about that data using SQL.

## Picture this

Imagine a school office that keeps two paper binders. The first binder has one page per student — student ID, name, age. The second binder has one page per grade — which student earned which mark in which class. The student ID printed on every grade page is the connection: if you want to know a student's name AND their grade, you match the ID across both binders.

A relational database is exactly that office, but digital and fast. Tables are the binders, rows are the pages, columns are the fields on each page, and keys are the IDs that let you match records across tables.

## How it actually works

**Tables** are the basic storage unit. A table has a fixed set of named columns (the "shape" of the data) and a growing list of rows (the actual data). Every cell in a row holds one value for one column — for example, a `students` table might have columns `student_id`, `name`, and `age`.

**The Primary Key (PK)** is a column (or combination of columns) whose value is unique for every row in that table — no duplicates, no blanks, ever. It is the row's permanent identity. Most databases auto-generate this as an incrementing integer (1, 2, 3 …) so you never have to think about uniqueness yourself.

**The Foreign Key (FK)** is how one table points at another. A `grades` table might have a column called `student_id` that must match a real `student_id` in the `students` table. The database enforces this rule: you cannot insert a grade for student ID 99 if no student with ID 99 exists. This guarantee is called **referential integrity** — the links between tables are never broken.

**SQL** (Structured Query Language) is the language you use to talk to the database. It is *declarative*: you say **what** you want, not **how** to find it. The database figures out the efficient path. The four operations every beginner needs are:

- `SELECT` — read rows
- `INSERT` — add rows
- `UPDATE` — change values in existing rows
- `DELETE` — remove rows

## Worked example

Suppose a school tracks students and their exam scores.

```sql
-- Create the students table
CREATE TABLE students (
    student_id  INT PRIMARY KEY,
    name        VARCHAR(100),
    age         INT
);

-- Create the grades table, with a foreign key back to students
CREATE TABLE grades (
    grade_id    INT PRIMARY KEY,
    student_id  INT REFERENCES students(student_id),
    subject     VARCHAR(50),
    score       INT
);

-- Insert 3 students
INSERT INTO students VALUES (1, 'Aisha',  15);
INSERT INTO students VALUES (2, 'Carlos', 16);
INSERT INTO students VALUES (3, 'Priya',  15);

-- Insert some grades
INSERT INTO grades VALUES (101, 1, 'Maths',   88);
INSERT INTO grades VALUES (102, 1, 'Science', 75);
INSERT INTO grades VALUES (103, 2, 'Maths',   92);

-- Ask: what are Aisha's scores?
SELECT s.name, g.subject, g.score
FROM   students s
JOIN   grades   g ON s.student_id = g.student_id
WHERE  s.name = 'Aisha';
```

Result:

| name  | subject | score |
|-------|---------|-------|
| Aisha | Maths   | 88    |
| Aisha | Science | 75    |

The `JOIN … ON` clause is the key-matching in action: the database finds every grade row where `grades.student_id` equals `students.student_id`, then filters for Aisha. Priya has no grades yet — she simply doesn't appear, which is correct.

Try inserting `INSERT INTO grades VALUES (104, 99, 'Art', 70);` — the database will reject it because student 99 does not exist. That is referential integrity doing its job.

## In the real world

Shopify's order management system is a textbook example. There is a `customers` table (customer_id, name, email), an `orders` table (order_id, customer_id, order_date, total), and an `order_items` table (item_id, order_id, product_id, quantity, price). Every time you click "Buy", Shopify inserts a row into `orders` and one row per product into `order_items`, both pointing back to your `customer_id`. A support agent querying "show me all orders placed by customer 4821 in the last 30 days" runs a `SELECT … JOIN … WHERE` across exactly these tables — and gets the answer in milliseconds across millions of rows.

## Common misconceptions

**People think the primary key should be something meaningful like a name or email — actually it just needs to be unique.** Names clash (two students named "Carlos") and emails change. An auto-incrementing integer (`1, 2, 3 …`) has no real-world meaning, which is a *feature*: it never changes and never collides.

**People think a foreign key copies data from the other table — actually it only stores a reference (the ID).** The `grades` table does not store Aisha's name; it stores `student_id = 1`. The name lives in one place only (`students`). This is the whole point — change Aisha's name once and every grade instantly reflects it, because they all point to the same row.

**People think SQL is a programming language like Python — actually it is a query language.** You declare the *result* you want ("give me students whose score > 80") and the database decides how to find it. There are no loops, no variables in basic SQL. This makes it simpler for data tasks, but it also means you cannot write general programs in it.

## How it relates & differs

| Concept | Relates to Tables & Keys | Differs from Tables & Keys |
|---|---|---|
| [[indexing\|Indexing]] | Primary keys almost always get an index automatically, so lookups by PK are instant. | Indexing is a *performance* layer on top of a table — it does not define structure or relationships, only speeds up searches. |
| [[normalization-vs-denormalization\|Normalization vs Denormalization]] | Splitting data into multiple linked tables (students + grades) *is* normalization. Keys are what make that split reversible. | Normalization is the *design philosophy*; tables and keys are the *mechanics* that implement it. |
| [[transactions-acid\|Transactions & ACID]] | Every `INSERT`, `UPDATE`, or `DELETE` SQL statement runs inside a transaction that guarantees the change is safe, complete, or rolled back. | Transactions & ACID describe *safety guarantees* around changes; tables and keys describe *structure and relationships*. |

## Why you'd use it (and when not to)

Use a relational database when your data has clear relationships, when you need to avoid storing the same fact twice, and when you need reliable, consistent answers to questions that cross-reference multiple entities (orders + customers + products). The trade-off: relational databases demand that you design your schema upfront and enforce strict rules. When your data is unstructured (documents, images), changes shape constantly, or needs to scale to billions of writes per second across hundreds of servers, those strict rules become a bottleneck — and document stores or column-oriented databases become better choices.

## Check yourself

**Memory hook:** "A table is a grid, a key is an ID, SQL is how you ask."

**Q1: What problem does a foreign key solve?**
It ensures that a row in one table can only reference a row that actually exists in another table, preventing "orphan" records — grades with no matching student, orders with no matching customer.

**Q2: You have a `products` table with 1 million rows. What does `SELECT * FROM products WHERE product_id = 42;` return, and why is it fast?**
It returns the single row where `product_id` is 42. It is fast because `product_id` is the primary key, and primary keys automatically get an index — the database jumps straight to that row rather than reading all 1 million.

**Q3: Why is using a person's email address as a primary key risky?**
Emails change. If a user updates their email, you would have to update it everywhere it is referenced as a foreign key across every related table — a cascade of changes that is error-prone and slow. An auto-incremented integer never changes, making updates safe and cheap.

## Connects to

[[indexing|Indexing]] · [[normalization-vs-denormalization|Normalization vs Denormalization]] · [[transactions-acid|Transactions & ACID]] · [[star-schema|Star Schema]] · [[big-o-time-complexity|Big-O / Time Complexity]]