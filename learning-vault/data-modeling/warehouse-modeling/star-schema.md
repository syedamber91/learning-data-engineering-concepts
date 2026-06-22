---
title: "Star Schema"
area: "Data Modeling"
topic: "Warehouse Modeling"
tags: [star-schema, fact-table, dimension, analytics]
---

# Star Schema

*Part of [[warehouse-modeling-moc|Warehouse Modeling]] · [[data-modeling-moc|Data Modeling]]*

**In one line:** A star schema arranges data as one central "facts" table of measurements, surrounded by "dimension" tables that describe them — shaped for fast reporting.

**Picture this:** Picture a till receipt pinned in the middle of a corkboard. Strings run out to cards labelled *Which store?*, *Which product?*, *Which date?*, *Which customer?*. The receipt is the fact; the cards are the dimensions. Drawn out, it looks like a star.

**How it actually works:** The *fact table* holds the numbers you want to add up — sales amount, quantity — plus keys pointing to each dimension. *Dimension tables* hold the descriptive details: product name, store city, calendar date. To answer "sales by city last December", you join the fact table to the store and date dimensions and sum. The simple shape makes these analytical queries fast and easy to write.

**In the real world:** Retailers like Walmart model their sales warehouse this way so analysts can slice billions of transactions by store, region, week, or product category in seconds for dashboards.

**Why you'd use it (and when not to):** Use a star schema for analytics and reporting, where you read and aggregate a lot. It's a poor fit for an app that does constant small updates — that's the job of a [[normalization-vs-denormalization|normalized]] design.

**Connects to:** [[slowly-changing-dimensions]] · [[normalization-vs-denormalization]]
