---
title: "Normalization vs Denormalization"
area: "Data Modeling"
topic: "Warehouse Modeling"
tags: [normalization, denormalization, duplication, trade-off]
---

# Normalization vs Denormalization

*Part of [[warehouse-modeling-moc|Warehouse Modeling]] · [[data-modeling-moc|Data Modeling]]*

**In one line:** Normalization splits data apart so nothing is duplicated; denormalization deliberately duplicates data so reads are faster.

**Picture this:** Normalization is keeping one master contact card for a friend and writing "see card #12" everywhere else — change it once, fixed everywhere. Denormalization is writing their full address on every envelope — slower to update, but each envelope is ready to post on its own.

**How it actually works:** A *normalized* design stores each fact in exactly one place and links to it with keys (see [[tables-keys-sql-basics]]). This keeps writes clean: update a product price once. The cost is that reading often needs many joins. A *denormalized* design copies values into one wide table so a read needs no joins — fast, but if a copied value changes you must update many rows.

**In the real world:** App databases that take orders are normalized (a price lives in one place). The analytics warehouse those orders flow into is denormalized into a [[star-schema|star schema]], so dashboards read fast without expensive joins.

**Why you'd use it (and when not to):** Normalize when writes and correctness dominate (live apps). Denormalize when reads dominate and data changes rarely (reporting). Picking the wrong one means either slow dashboards or messy, error-prone updates.

**Connects to:** [[tables-keys-sql-basics]] · [[star-schema]]
