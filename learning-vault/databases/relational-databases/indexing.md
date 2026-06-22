---
title: "Indexing"
area: "Databases"
topic: "Relational Databases"
tags: [index, performance, lookup, query]
---

# Indexing

*Part of [[relational-databases-moc|Relational Databases]] · [[databases-moc|Databases]]*

**In one line:** An index is a pre-sorted shortcut that lets a database find rows without reading the whole table.

**Picture this:** To find "photosynthesis" in a textbook, you don't read all 500 pages — you flip to the index at the back, see "page 212", and jump there. A database index is exactly that: a sorted list of values pointing to where each row lives.

**How it actually works:** Without an index, the database does a *full table scan* — it checks every row one by one (an [[big-o-time-complexity|O(n)]] effort). An index keeps a chosen column sorted in a tree structure, so the database can zero in on matching rows in just a few hops. You add indexes to columns you frequently filter or join on.

**In the real world:** When you search a username on Instagram, an index on the `username` column finds your account among billions almost instantly. Remove that index and the search could take minutes per lookup.

**Why you'd use it (and when not to):** Index columns you search by a lot. But indexes cost storage and slow down writes (every insert must also update the index), so don't index everything — only what your queries actually need.

**Connects to:** [[tables-keys-sql-basics]] · [[big-o-time-complexity]] · [[arrays-hash-maps]]
