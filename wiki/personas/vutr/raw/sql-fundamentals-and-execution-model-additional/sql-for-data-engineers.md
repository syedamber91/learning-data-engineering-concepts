---
title: "SQL For Data Engineers"
channel: vutr
author: "Vu Trinh"
published: 2025-10-07
url: https://vutr.substack.com/p/sql-for-data-engineers
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark"]
tags: [https, auto, table, good, substackcdn, image]
---

# SQL For Data Engineers

*A note on everything a data engineer should know about SQL*

> Source: [Open post](https://vutr.substack.com/p/sql-for-data-engineers)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=168139096)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!2jFx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fab679ab6-229f-4a06-93cb-3ca13e81a632_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!2jFx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fab679ab6-229f-4a06-93cb-3ca13e81a632_2000x1428.png)

---

## Intro

I was wrong in many things, one of them was learning SQL too late. I used to believe that I should put full effort into Python, and I would be fine. The fact is, everybody speaks SQL in the data world!

This article is a reflection on my experience after several years of learning SQL as a data engineer. The goal is to provide you and me with a strong foundation in this query language; from there, learning or working with SQL will be more effective.

## History

Edgar F. Codd. In June 1970, while working at IBM, Codd published his paper, “[A Relational Model of Data for Large Shared Data Banks](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf).” This paper introduced a new model for managing data, now accepted as the dominant approach for Relational Database Management Systems (RDBMS).

[![](https://substackcdn.com/image/fetch/$s_!kL3t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e8b3a15-2846-4145-813a-773d85e2448d_610x458.png)](https://substackcdn.com/image/fetch/$s_!kL3t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e8b3a15-2846-4145-813a-773d85e2448d_610x458.png)

Before Codd’s work, databases were dominated by navigational models, such as the hierarchical and network models. Data was accessed by “navigating” through records using pointers and predefined paths. The programmer must specify the exact step-by-step procedure—the *how*—to retrieve a piece of information.

[![](https://substackcdn.com/image/fetch/$s_!GW--!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc5afbb7-a22d-485c-ba7d-f12da19ffacf_390x230.png)](https://substackcdn.com/image/fetch/$s_!GW--!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc5afbb7-a22d-485c-ba7d-f12da19ffacf_390x230.png)

Codd doesn’t think it's a good idea because only heavily trained technical users can use these systems. His relational model suggested that data be organized into simple tables, called “relations,” composed of rows (”tuples”) and columns (”attributes”).

[![](https://substackcdn.com/image/fetch/$s_!wKBL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faba6fa32-840a-4c95-8fd4-5151828be068_856x266.png)](https://substackcdn.com/image/fetch/$s_!wKBL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faba6fa32-840a-4c95-8fd4-5151828be068_856x266.png)

More importantly, it separated the logical representation of data from its physical storage and access methods. This abstraction enabled the creation of a more declarative language to work with data.

It allows a user to specify *what* data they want, leaving the complex task of *retrieving* it to the database management system. Following the publication of Codd’s model, IBM scientists Donald Chamberlin and Raymond Boyce developed a language to implement it, which they called Structured English Query Language (SEQUEL).

This was later shortened to SQL (often still pronounced “sequel”). The first commercially available implementation of SQL was introduced in 1979 by Relational Software, Inc., the company that would later become Oracle Corporation. The American National Standards Institute (ANSI) standardized SQL in 1986, followed by the International Organization for Standardization (ISO) in 1987.

## Relation algebra

SQL is declarative. It’s cool. However, the database still needs to translate the SQL query into “procedural steps“ (e.g., reading these tables, selecting this field,…). The mathematical framework for this step is **Relational Algebra**. It comprises a set of operators that operate on relations. The fundamental operators of relational algebra are as follows:

* **Selection** (σ): This unary operator filters the tuples (rows) of a relation based on a specified condition or predicate. It corresponds directly to the WHERE clause (surprisingly, it’s not the SELECT). For example, the expression σsalary>500​(Employees) is equivalent to SELECT \* FROM Employees WHERE salary > 500;.

  [![](https://substackcdn.com/image/fetch/$s_!SKu-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3afcaec7-bebf-45e9-a361-e4bd77141076_472x246.png)](https://substackcdn.com/image/fetch/$s_!SKu-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3afcaec7-bebf-45e9-a361-e4bd77141076_472x246.png)
* **Projection** (Π): This unary operator selects a subset of the attributes (columns) of a relation. It corresponds to the SELECT. For example,

  Πname, department​(Employees) is equivalent to SELECT name, department FROM Employees;.

  [![](https://substackcdn.com/image/fetch/$s_!_yGT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11e90bcc-4698-4d34-90ba-24188b9b3ba0_560x264.png)](https://substackcdn.com/image/fetch/$s_!_yGT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11e90bcc-4698-4d34-90ba-24188b9b3ba0_560x264.png)
* **Union** (∪): This binary operator combines two “union-compatible” relations (they must have the same set of columns). The result contains all tuples that appear in either or both relations, with duplicates removed. This maps to the UNION operator in SQL.

  [![](https://substackcdn.com/image/fetch/$s_!9axI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3368e8f5-4781-4c83-8c6a-6eaedfef82f6_418x422.png)](https://substackcdn.com/image/fetch/$s_!9axI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3368e8f5-4781-4c83-8c6a-6eaedfef82f6_418x422.png)
* **Set Difference** (−): This binary operator returns all tuples that are in the first relation but not in the second.
* **Cartesian Product** (×): This binary operator combines every tuple from the first relation with every tuple from the second relation. It is the foundational operation for all SQL JOINs and is explicitly implemented by the CROSS JOIN operator.

  [![](https://substackcdn.com/image/fetch/$s_!vGiN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c3e441c-42b0-4ef8-99d4-f00b3ae63cfd_538x392.png)](https://substackcdn.com/image/fetch/$s_!vGiN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c3e441c-42b0-4ef8-99d4-f00b3ae63cfd_538x392.png)
* **Join** (⨝): This is a binary operator that combines data from two relations based on conditions. It is fundamentally a Cartesian product followed by a selection.

  [![](https://substackcdn.com/image/fetch/$s_!f_cG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9f43308-cf50-460d-abdb-7c353d4135d3_576x316.png)](https://substackcdn.com/image/fetch/$s_!f_cG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9f43308-cf50-460d-abdb-7c353d4135d3_576x316.png)

  + For instance, an equi-join is a Cartesian product followed by a selection that keeps only the rows where the join keys are equal.
  + This concept maps to the entire family of JOIN clauses in SQL (INNER JOIN, OUTER JOIN, etc.).
* Intersection (∩): This binary operator returns all tuples that are common to both relations. It can be derived using the set difference operator (A-B = A∩−(A−B)). Unlike the Join operator, this operator requires the two relations to have the same schema.

  + This maps directly to the INTERSECT operator in SQL. It is rarely seen in SQL implementations; however, it remains part of the ANSI SQL standard (optional)

## Clauses

> *This article only covers the DQL’s clauses; you won’t see DML’s clauses like INSERT, UPDATE, or DELETE here.*

Because you tell the system what you want via SQL, there are clauses, the “verbs“ to describe the action you want with the data. The section will cover most of the 95% (at least to me) SQL queries. These will also be listed based on the order of the physical execution behind the scenes.

[![](https://substackcdn.com/image/fetch/$s_!tnSa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91ff0fe6-7c67-4d78-aa70-25714c51db6e_554x542.png)](https://substackcdn.com/image/fetch/$s_!tnSa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91ff0fe6-7c67-4d78-aa70-25714c51db6e_554x542.png)

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=168139096)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

1. **FROM / JOIN**: The database first identifies the required tables and performs any joins to create the complete dataset.
2. **WHERE**: It then filters this dataset, skipping rows that do not meet the conditions. (e.g., A > 3)
3. **GROUP BY**: The remaining rows are grouped based on the values in one or more columns, preparing them for aggregation (e.g., SUM, COUNT, AVG…)
4. **HAVING**: After the rows are grouped, this clause filters out records that do not meet the aggregate conditions (e.g., SUM(A) > 7)
5. **SELECT**: The engine processes the SELECT list to determine which columns, expressions, and aggregated values to include in the final result. (I used to think the first one would be SELECT.)

   1. **WINDOW FUNCTIONS** are also processed here.
6. **DISTINCT**: If specified, duplicate rows are removed from the result set.
7. **ORDER BY**: The final result set is sorted according to the specified columns or expressions.
8. **LIMIT / OFFSET**: The query limits the output to a specific number of rows.

The difference between WINDOW FUNCTION and GROUP BY also needs to be aware of here:

* **GROUP BY** collapses rows. It takes multiple rows and aggregates them into a single summary row. For example, `SELECT product, SUM(sales) FROM tables GROUP BY product` will return one row for each product, showing the total sales for that product.

  [![](https://substackcdn.com/image/fetch/$s_!KhZI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f4e9286-c7a7-489c-8219-3657ca316e7c_726x266.png)](https://substackcdn.com/image/fetch/$s_!KhZI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f4e9286-c7a7-489c-8219-3657ca316e7c_726x266.png)
* **Window functions** operate on a “window” of rows but do not collapse them. They return a value for each row based on the defined window. For example,

  `SELECT product, SUM(sales) OVER (PARTITION BY product) AS product\_total\_sales FROM tables` will return all the original product rows. However, it adds a new column (product\_total\_sales) to each row, showing the total sales for that product.

  [![](https://substackcdn.com/image/fetch/$s_!xaU_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b01edf8-0140-4068-aa23-bdbd73da8efe_816x360.png)](https://substackcdn.com/image/fetch/$s_!xaU_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b01edf8-0140-4068-aa23-bdbd73da8efe_816x360.png)

## Materialization

From the section above, we know that everything begins with the FROM clause. There must be a “target“ so we can refer to it with the FROM. That target could be a table, a view, or a materialized view.

### Table

A table is the physical container for your data. When we insert, update, or delete data, we are directly manipulating the information stored in structured files on the disk.

[![](https://substackcdn.com/image/fetch/$s_!sdA6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06389c49-d46a-484c-a279-d74127d78a8a_632x206.png)](https://substackcdn.com/image/fetch/$s_!sdA6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06389c49-d46a-484c-a279-d74127d78a8a_632x206.png)

In the file, the database engine manages how this data is organized in pages for efficient access. Then, it exposes the table abstraction for the end user, which contains rows and columns. A table can be created empty at first (and users will write data later) or made from a query result (e.g., CREATE TABLE AS (SELECT…))

### View

There are cases where you don’t want to materialize the data. View can help with that. Essentially, it contains the SQL query; whenever it is referenced, the query will be executed, and the result is retained only during the query execution process. The view’s query is re-executed every single time you access the view.

[![](https://substackcdn.com/image/fetch/$s_!hCYp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc43fc174-c11a-4d49-a56a-dcca04d56c4e_316x260.png)](https://substackcdn.com/image/fetch/$s_!hCYp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc43fc174-c11a-4d49-a56a-dcca04d56c4e_316x260.png)

In my experience, views are helpful when we want to hide and reuse complex queries, especially for end users who wish to query the data but lack a deep understanding of the complexity behind the scenes (e.g., which tables to join?). However, views need to be taken into consideration when they are frequently referred to in the transformation process, and the result of the view is substantial, so materializing it into a table might be a better choice.

[![](https://substackcdn.com/image/fetch/$s_!PseN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F841675b6-ba93-4711-94f6-fbf4f19740f0_698x180.png)](https://substackcdn.com/image/fetch/$s_!PseN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F841675b6-ba93-4711-94f6-fbf4f19740f0_698x180.png)

Views are also implemented for access control. Users can choose to expose restricted rows (by the WHERE clause) or columns (by SELECTing some columns)

### Materialized view

A materialized view (MV) is a hybrid. Like a view, it is defined by a query. But like a table, it physically stores the result set of that query. When you create a materialized view, the database executes the defining query and stores the results on disk, just like a table. When you query the materialized view, the database reads from this pre-computed, stored data.

[![](https://substackcdn.com/image/fetch/$s_!fMvO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1dc06282-1062-45f9-afd2-133933aba1d0_1018x426.png)](https://substackcdn.com/image/fetch/$s_!fMvO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1dc06282-1062-45f9-afd2-133933aba1d0_1018x426.png)

The critical challenge is that the stored data becomes stale as the underlying base tables change. Therefore, materialized views must be refreshed. There are several ways to achieve this: using fixed schedulers (e.g., every hour), full refresh when the source table changes, or incremental refresh when the source table changes.

> ***Note**: Within the scope of this article, we will only examine the high-level aspects of the MV. To delve deeper into it, I think it deserves a whole article.*

### How about Common Table Expression (CTE)

Unlike a table, view, or materialized view, a CTE is only referenced inside a query. Think of it as a temporary, convenient name for a subquery.

[![](https://substackcdn.com/image/fetch/$s_!oWSa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1041f760-f9cc-492d-b469-83194d0508ab_330x308.png)](https://substackcdn.com/image/fetch/$s_!oWSa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1041f760-f9cc-492d-b469-83194d0508ab_330x308.png)

Instead of nesting queries inside other queries, creating what’s often called “spaghetti code,” a CTE allows you to break down a complex problem into a series of logical, readable steps.

## Join

> *In the scope of this article, only the equi-joins (joins with equal editions) are discussed.*

The high-level join is quite simple; the database needs to find records from tables that share the same user-defined condition. When it comes to the physical implementation, the problem boils down to a search problem. Any database primarily implements three main approaches.

### Nested Loop Join (NLJ)

There will be two loops.

The first will loop through every record in the left table. For each record, the database loops through the right table to compare using the join condition. If the condition is met, the combined row is included in the join result. The main advantage of this approach is the simplicity.

[![](https://substackcdn.com/image/fetch/$s_!MiYR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b2c5d37-2cfe-4415-b774-e170523f21ca_954x312.png)](https://substackcdn.com/image/fetch/$s_!MiYR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b2c5d37-2cfe-4415-b774-e170523f21ca_954x312.png)

NLJ can perform quite well when the left table is small, which keeps the number of repeat scans of the right table small. Additionally, if the right table has an index on the join column(s), the second loop can perform an index lookup instead of a full table scan for each row in the left table, thereby drastically improving performance.

### Sort Merge Join (SMJ)

With SMJ, the system must carry out two phases.

[![](https://substackcdn.com/image/fetch/$s_!Rqhb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbccdbc4b-5bad-49ed-aea4-b39491bde00b_1122x354.png)](https://substackcdn.com/image/fetch/$s_!Rqhb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbccdbc4b-5bad-49ed-aea4-b39491bde00b_1122x354.png)

* In the first phase, the system sorts the two tables based on the join columns.
* In the second phase, the system walks through the tables with associated pointers:

  + If the join conditions match, the rows are combined.

    - If duplicates exist in one or both tables for the current join key value, all combinations of matching rows must be generated.
    - This might involve moving the pointer from one table backward while moving the pointer from another forward.
  + If a value in one table is smaller than the value in the other, its pointer moves forward.
  + This process continues until one or both tables are exhausted.

Compared to the NLJ, the system must perform sort operations on both tables. That could be more expensive; however, it amortizes the cost of using two loops in the NLZ. SMJ is particularly efficient when one or both input tables are already sorted on the join columns. It is also convenient if the query output must be sorted by the join key ( `ORDER BY` clause on the join key), as the merge phase naturally produces sorted output.

### Hash Join (NLJ)

Hash join works based on the simple idea that if the rows from two tables match, they have the same join column values, thus having the same result after applying the hash function on these column values.

The classic in-memory Hash Join algorithm consists of two phases:

[![](https://substackcdn.com/image/fetch/$s_!zohg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F314940bb-5ab5-41d4-9763-bd744d8b8e59_672x318.png)](https://substackcdn.com/image/fetch/$s_!zohg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F314940bb-5ab5-41d4-9763-bd744d8b8e59_672x318.png)

1. **Build Phase:** The database system will construct an in-memory hash table using the smaller table. The goal is to fit the entire hash table in memory. Each row’s join column(s) are hashed to determine its bucket.
2. **Probe Phase:** After the hash table is built, the system scans the second table. For each row in this table, its join column(s) are hashed using the same hash function applied during the build phase. This hash value is then used to look up matching rows in the hash table. If a match is found, the corresponding rows are combined and returned.

> *From now on, I will use the 'build table' to refer to the table used to build the hash table, and the 'probe to re’ to refer to the one scanned and used to look up the hash table.*

Hash Join is effective for equi-joins, especially when one of the tables (the build table) is small enough to fit into memory. It won’t require data to be sorted beforehand or a pre-built index to optimize the performance.

However, it requires building an in-memory hash table during runtime. If this hash table exceeds available memory, the performance of the classic Hash Join algorithm degrades significantly, as it may be forced to spill to disk. Imagine the hash table has two parts: part A, which fits in memory, and part B, which spills to the disk.

[![](https://substackcdn.com/image/fetch/$s_!ggQC!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03545740-3bbf-431a-86b8-64aeca5c52f7_1132x372.png)](https://substackcdn.com/image/fetch/$s_!ggQC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03545740-3bbf-431a-86b8-64aeca5c52f7_1132x372.png)

When looping through the probe table, for each row, after checking for matching rows from part A, the system needs to check part B on the disk. This requires loading part B into memory and offloading part A to disk. The loading of data back and forth from disks like this degrades the performance of the hash join.

This is where the [Grace Hash Join](https://youtu.be/MFazkaZKs1s?list=PLSE8ODhjZXjYDBpQnSymaectKjxCy6BYq&t=3323) comes to the rescue. This algorithm can also be referred to as a partitioned hash join. This variant is employed when the hash table does not fit into available memory:

* **Partitioning Phase:** Both tables are scanned, the same hash function is applied to their join columns, and rows are distributed into buckets on disk.

  [![](https://substackcdn.com/image/fetch/$s_!1QSZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74386447-d8d9-451b-97ba-134184e94160_862x336.png)](https://substackcdn.com/image/fetch/$s_!1QSZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74386447-d8d9-451b-97ba-134184e94160_862x336.png)

  + The number of buckets is chosen so that each bucket of the build table is small enough to be processed in memory during the next phase (ideally, the probe table bucket is also fit in the memory).
  + If any partition bucket of the hash table is too large for memory, it can be recursively partitioned using a different hash function until all resulting sub-buckets fit in memory.
* **Probing Phase (Join Phase):** For each pair of corresponding buckets (build bucket i/probe bucket i), the system brings these buckets to memory and creates a hash table from the build bucket i, and a classic in-memory hash-join is executed between this hash table and the associated probe bucket.

  [![](https://substackcdn.com/image/fetch/$s_!70JV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb8156c3-c40e-450d-921c-ca70b1e1e286_596x258.png)](https://substackcdn.com/image/fetch/$s_!70JV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb8156c3-c40e-450d-921c-ca70b1e1e286_596x258.png)

Although this approach requires two rounds of hashing, it limits the number of disk I/Os as each bucket will be brought into memory once to execute the hash join.

## What typically happens behind the scenes

After learning nearly everything we need to write SQL, it’s time to run it. We submit the query to the database, and 38 seconds later, a nicely formatted result table is returned. But do you know what actually happens behind the scenes? Although a data professional rarely implements a query processing engine from scratch, I believe that understanding the query life cycle can bring value in many cases.

Of course, the details of the query execution vary depending on the database implementation; this section only provides the typical process:

[![](https://substackcdn.com/image/fetch/$s_!Wyf1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e77440e-a67b-438b-92da-00dca0f7d8fe_802x386.png)](https://substackcdn.com/image/fetch/$s_!Wyf1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e77440e-a67b-438b-92da-00dca0f7d8fe_802x386.png)

* **Parsing**: First, the DBMS receives the SQL statement as a string of text. It calls the parser to break this string into individual words, or “tokens,” such as clauses (SELECT, FROM), operators (e.g., =, <>), identifiers (e.g., table and column names), and literal values (e.g., ‘product\_A‘, ‘2025-01-01‘).

  + It then checks these tokens against the grammatical rules of the system’s SQL dialect to ensure the statement is syntactically valid. “Syntax errors” are raised here.
  + The parser then takes these tokens and builds an **Abstract Syntax Tree (AST)**, which is a hierarchical tree that represents the query’s grammatical structure.
* **Validation:** After ensuring there are no syntax errors, the DBMS validates the semantics of the query. The database catalog needs to be involved here. It is the database’s internal metadata repository that provides information about the database’s entities (e.g., tables, views, table columns). This step verifies several key points (not comprehensive):

  + Do the tables in the query exist?
  + Do the referenced table’s columns exist, and are their names unambiguous?
  + Does the filtered value have a compatible data type with the column’s type?
  + Permissions checking is also performed here
  + …
* **The Logical Plan**: The validated tree is converted into a logical query plan using the relational algebra. This plan serves only as the high-level blueprint of the data flow and execution. The optimizer could apply some optimizations to the logical plan here, such as filter pushdown.
* **The Physical Plan:** The final logical plan is then converted to the physical plan, which provides concrete instructions for the database engine to retrieve and process the data. The optimizer has a mechanism to choose the best plan here based on:

  + The statistics (e.g., table rows, cardinality, min-max metadata) or any available indexes (e.g., B-Tree,…). The optimizer then generates multiple plans. The chosen plan is the one that satisfies some requirement, such as the one with the lowest total I/O. This approach is called **Cost-Based Optimization**
  + Some predefined rules. This approach is called **Rule-Based Optimization.**
* **Execution:** The final physical plan is then sent to “workers“ for physical execution. The plan is followed from start to end; the final result is then sent back to the client.

  + **Note** that the plan can be dynamically adjusted at runtime, especially with the OLAP system. This helps the systems adapt to new statistics created from the plan's previous steps, which might not be available at the planning phase.

## Outro

In this article, we first learn the history of SQL and its backbone, relational algebra. Then comes the DQL’s clauses and their order of evaluation. Next, we explore the table, view, materialized view, CTE, and how joins are executed under the hood. We then conclude the article with a typical SQL query life cycle.

Thank you for reading this far. See you in my next articles.

---

## Reference

*[1] Andy Pavlo, [Relational Model & Algebra (CMU Intro to Database Systems),](https://www.youtube.com/watch?v=APqWIjtzNGE&list=PLSE8ODhjZXjYDBpQnSymaectKjxCy6BYq&index=2) 2024*

*[2] Andy Pavlo, [Join Algorithms: Hash, Sort-Merge, Nested Loop Joins (CMU Intro to Database Systems)](https://www.youtube.com/watch?v=MFazkaZKs1s&list=PLSE8ODhjZXjYDBpQnSymaectKjxCy6BYq&index=13)*

*[3] Andy Pavlo, [Parallel Hash Join Algorithms (CMU Advanced Database Systems)](https://www.youtube.com/watch?v=S40K8iGa8Ek&list=PLSE8ODhjZXjYa_zX-KeMJui7pcN1rIaIJ&index=10)*
