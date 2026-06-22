---
title: "Tables, Keys & SQL Basics"
area: "Databases"
topic: "Relational Databases"
tags: [sql, tables, primary-key, foreign-key]
---

# Tables, Keys & SQL Basics

*Part of [[relational-databases-moc|Relational Databases]] · [[databases-moc|Databases]]*

**In one line:** A relational database stores data in tables (rows and columns), links tables with keys, and answers questions written in a language called SQL.

**Picture this:** Think of a school spreadsheet. One sheet lists *Students*, another lists *Classes*. Each student row has a Student ID; each class row records which Student IDs attend. The ID is the thread that ties the two sheets together.

**How it actually works:** Each table holds one kind of thing (students, orders). A *primary key* is a column that uniquely names each row (like Student ID). A *foreign key* in another table points back to it, creating relationships. You ask questions with SQL: `SELECT` reads, `INSERT` adds, `UPDATE` changes, `DELETE` removes. For example, `SELECT name FROM students WHERE grade = 10`.

**In the real world:** Your bank stores accounts and transactions in relational tables. When you check your balance, an SQL query joins your account row to its transaction rows and adds them up. Airlines, hospitals, and online shops all run on this model.

**Why you'd use it (and when not to):** Use relational databases when data is structured and relationships matter (customers ↔ orders). They're less ideal for huge piles of loosely-structured data like raw logs, where other stores fit better.

**Connects to:** [[indexing]] · [[transactions-acid]] · [[normalization-vs-denormalization]]
