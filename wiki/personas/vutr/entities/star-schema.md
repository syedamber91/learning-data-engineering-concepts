---
persona: vutr
kind: entity
sources:
- raw/dbt-and-dimensional-modeling/dimensional-modeling-overview.md
- raw/dbt-and-dimensional-modeling/deep-dive-into-the-kimball-dimensional.md
- raw/dbt-and-dimensional-modeling/i-spent-6-hours-learning-about-slowly.md
last_updated: '2026-07-15'
qc: passed
slug: star-schema
topics:
- dbt
---

The star schema — named for its visual resemblance to a star — puts a single fact table at the center, surrounded by dimension tables radiating outward. Vu presents it as Kimball's answer to a problem third normal form (3NF) modeling creates for analytics: 3NF removes redundancy by splitting data across many separate relational entities, which is right for operational systems prioritizing data integrity, but becomes overwhelming for analysis — trying to compute January revenue for users in India by navigating an ERD with hundreds of entities is, in his words, too complicated. The star schema deliberately accepts some denormalization to keep queries and mental models simple for business users.

The fact table holds the performance measurements from a business process's events — one row per measurement, at a single, consistent grain (see [[grain-declaration]]) — with foreign keys out to the surrounding dimension tables and numeric measures (revenue, quantity, profit). Kimball's guidance, which Vu repeats consistently, is to store the *low-level* measurement rather than a pre-aggregate, because low granularity preserves flexibility for future questions the current design didn't anticipate. When every foreign key in the fact table correctly matches a primary key in its dimension table, the schema has referential integrity — the property that actually makes fact-to-dimension joins produce meaningful answers, like computing a user's European revenue by joining the sales fact table to the country dimension on a foreign key.

Dimension tables are the "who, what, where, when, how, and why" around each fact — Vu's example: a skyrocketing revenue number alone tells you nothing until a product or territory dimension lets you ask why. In his own hands-on project he builds two: `dim_product` (joined from staging tables for products, subcategories, and categories) and `dim_territories`, both carrying a surrogate key generated to support SCD Type 2 history tracking (see [[surrogate-keys]] and [[scd-type-2]]), and both referenced by his single `fact_sale` table at the order grain.

*See also: [[grain-declaration]] · [[surrogate-keys]] · [[dbt]] · [[scd-type-2]] · [[scd-type-1-and-3]] · [[dbt-origin-and-adoption]] · [[dimensional-modeling]] · [[one-big-table]]*

## Related in the other wiki
- [[Stars and Snowflakes - Schemas for Analytics]] — DDIA names the same trade-off in the opposite direction: the normalized "snowflake" variant of this schema avoids redundancy but multiplies joins and analyst confusion, which is exactly the 3NF failure mode Vu contrasts the star schema against.
