---
persona: vutr
kind: entity
sources:
- raw/dbt-and-dimensional-modeling/i-spent-6-hours-learning-about-slowly.md
last_updated: '2026-07-15'
qc: passed
slug: scd-hybrid-types-5-6-7
topics:
- dbt
---

Vu groups SCD Types 5 through 7 together as hybrid approaches built by combining the basic types, and is upfront that he doesn't think they're widely adopted in real life — he covers them briefly, for completeness, rather than as techniques he recommends.

**Type 5** combines Type 4's mini-dimension (approach A) with Type 1's overwrite. The goal is letting you do historical analysis of a group of attributes *and* get quick access to their current values without an extra join. Kimball's own example, which Vu reuses directly: a `Customer` dimension paired with a `Demographic Mini-Dimension` holding fields like income and age. Under plain Type 4, reaching the current demographic values means joining the fact table to both `Customer` and the mini-dimension. Type 5 avoids that second join for current-value lookups by adding a "Type 1 outrigger" to the base `Customer` table — a column (or small set of columns) that is overwritten every time the mini-dimension gets a new row, always pointing at the mini-dimension's *current* version. So a demographic change triggers two things at once: a new row in the mini-dimension (Type 4 behavior) and an overwrite of the outrigger reference on the `Customer` table (Type 1 behavior).

**Type 6** — its name comes from a coincidence Vu notes with some amusement: both the sum and the product of 1, 2, and 3 equal 6, and Type 6 is indeed a hybrid of Types 1, 2, and 3. It stores the full change history as separate rows (Type 2), while each row also carries columns holding the original value, the current value, and the "as-was" value from when that row was created (Type 3's within-row multi-version trick), letting a single table serve both historical and current analysis. Vu's worked example: an `Employee` dimension where employees change departments. A department change creates a new row (Type 2); the old row is closed with an end date; both the old and new rows carry a Current Department column and a Historical Department column, and the Current Department column is overwritten (Type 1) across *every* historical row for that employee whenever a change happens. The payoff: a query can see both which department an employee was in at a past point in time (via Historical Department) and where they are now (via Current Department), from the same table.

**Type 7** is a variant of Type 6 that splits the single table into two: a history table and a current table. Every row carries both a surrogate key (different for every new version) and a durable key — a stable identifier for the entity itself (e.g. the employee) that never changes across versions, which may be a natural key if the natural key happens to be durable. Type 6's dual-value tracking is still present, but the columns tracking current values are now managed specifically in the separate current table rather than duplicated across every historical row.

*See also: [[scd-type-4-mini-dimension]] · [[scd-type-2]] · [[scd-type-1-and-3]] · [[dimensional-modeling]]*
