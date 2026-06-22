---
title: "Slowly Changing Dimensions"
area: "Data Modeling"
topic: "Warehouse Modeling"
tags: [scd, history, dimension, type-2]
---

# Slowly Changing Dimensions

*Part of [[warehouse-modeling-moc|Warehouse Modeling]] · [[data-modeling-moc|Data Modeling]]*

**In one line:** Slowly Changing Dimensions (SCD) are the rules for what to do when a descriptive detail — like a customer's city — changes over time.

**Picture this:** A customer moves from Lahore to Dubai. Do you erase "Lahore" and write "Dubai"? Or keep both, so last year's sales still say Lahore? That choice is what SCD is about.

**How it actually works:** There are three common approaches. **Type 1**: overwrite the old value — simple, but history is lost (the past now looks like it always said Dubai). **Type 2**: add a *new row* for the customer with the new city and date ranges, keeping the old row — full history preserved. **Type 3**: keep a "previous value" column alongside the current one — only the last change is remembered.

**In the real world:** A subscription business like Netflix uses Type 2 to track which plan a member was on each month. When revenue is reported, old months correctly reflect the old plan, not today's plan — vital for accurate financials.

**Why you'd use it (and when not to):** Use Type 2 when history matters (analytics, audits). Use Type 1 when only the latest value matters and the past is irrelevant, since keeping history costs extra rows and complexity.

**Connects to:** [[star-schema]] · [[normalization-vs-denormalization]]
