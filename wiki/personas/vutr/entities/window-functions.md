---
persona: vutr
kind: entity
sources:
- raw/sql-fundamentals-and-execution-model-additional/sql-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: window-functions
topics:
- sql-fundamentals-and-execution-model
---

Window functions operate on a "window" of rows but do not collapse them the way [[group-by]] does — they return a value for every original row, computed over the window that row belongs to. For example, `SELECT product, SUM(sales) OVER (PARTITION BY product) AS product_total_sales FROM tables` still returns every original product row, just with an added column showing that product's total sales attached to each one — contrast with a GROUP BY on the same aggregate, which would collapse the rows down to one per product and lose the original row-level detail.

Physically, window functions are processed as part of the SELECT step in the [[sql-execution-order]] — the same stage where the engine determines which columns, expressions, and aggregated values go into the final result.

*See also: [[group-by]] · [[sql-execution-order]] · [[selection-operator]]*
