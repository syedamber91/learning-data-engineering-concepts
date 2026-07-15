---
persona: vutr
kind: entity
sources:
- raw/dbt-and-dimensional-modeling/i-spent-6-hours-learning-about-slowly.md
- raw/dbt-and-dimensional-modeling/deep-dive-into-the-kimball-dimensional.md
last_updated: '2026-07-15'
qc: passed
slug: scd-type-2
topics:
- dbt
---

SCD Type 2 is, in Vu's account, the most-used Slowly Changing Dimension technique, and it works by adding rows rather than overwriting them. When a dimension record changes, the system inserts a new row carrying the change; the new row gets a different surrogate key from the original (see [[surrogate-keys]]), and fact rows can point at whichever version of the dimension record was valid when the fact occurred by referencing the matching foreign key.

Implementing Type 2 requires two additional columns on the dimension record — Vu calls them `start_date`/`end_date` in one post and `effective_date`/`expired_date` in another, describing the identical mechanism both times. When a new version is inserted, the previously current row is marked expired: its end date is set to the day *before* the new row's start date, specifically to avoid leaving a gap between versions, and the new row's end date is set to a sentinel far-future value (9999-12-31) to mark it as open-ended/current. This is also why an `is_current` flag is useful in practice: it lets a query or a pipeline cheaply find "the currently valid version" of a dimension record without comparing dates.

The practical payoff is that historical facts stay historically accurate: if a user bought a product first in Vietnam and later in Singapore, Type 2 reports those two purchases against two different country contexts, because the historical fact row still points at the historical dimension version with its own valid date range — contrast this with [[scd-type-1-and-3|Type 1's]] overwrite, which would silently reassign the earlier purchase's context to the country the user lives in now. Vu implements Type 2 mechanically two different ways in his own dbt project — a hand-written `merge` incremental strategy and dbt's built-in `snapshot` feature — see [[dbt-incremental-strategies-for-scd]] for exactly how each one is wired up, and his own conclusion that snapshot is the better production choice despite its extra setup friction.

*See also: [[star-schema]] · [[grain-declaration]] · [[surrogate-keys]] · [[dbt]] · [[scd-type-1-and-3]] · [[dbt-origin-and-adoption]] · [[dbt-incremental-strategies-for-scd]]*
