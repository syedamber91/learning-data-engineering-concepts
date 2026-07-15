---
persona: vutr
kind: entity
sources:
- raw/dbt-and-dimensional-modeling/i-spent-6-hours-learning-about-slowly.md
last_updated: '2026-07-15'
qc: passed
slug: scd-type-4-mini-dimension
topics:
- dbt
---

Vu flags SCD Type 4 as inconsistently defined across sources: what people describe on the internet ("approach B") differs from what he read in *The Data Warehouse Toolkit* itself ("approach A") — so he documents both rather than picking one as canonical.

**Approach A (the book's version)** splits frequently-changing attributes out of the base dimension into a separate **mini-dimension** table, which stores only the *unique combinations* of those column values rather than one row per entity — for example, instead of a row per customer, a row per distinct demographic profile ("Age 25–34, VIP account, Income $50k–$75k"). Kimball's refinement here is to convert continuous values like income or age into predefined bands before storing them, which shrinks the mini-dimension further since many changes land in the same band. The fact table then needs an additional foreign key pointing at the mini-dimension. If a user needs the exact underlying value rather than the band, Kimball's suggestion is to also carry the raw value directly in the fact table.

**Approach B (the version Vu found more common online)** is closer to Type 2 with one twist: the current state and the historical states live in two *separate* tables. When a change happens, the current table is updated in place (overwritten), while the previous version is pushed into a history table. The current table doesn't need `start_date`/`end_date` columns at all, since every row in it is by definition the latest state; the history table does need them, to preserve valid-date ranges. Vu notes this split pays off specifically when most queries only need the latest state (e.g. a user's most recent email or phone number for marketing) — the current table is much smaller than the historical one and gives a real performance benefit, while historical analysis can still reach into the larger history table when needed.

Vu asked for help publicly (Reddit, LinkedIn) trying to resolve which definition was "correct" and found no official explanation for the divergence — only a comment he found persuasive: that these are ultimately just labels, and what matters is picking whatever mechanism actually fits your requirements rather than chasing naming purity. His own conclusion is to present both approaches side by side rather than force a single definition, since he believes each genuinely fits different scenarios.

*See also: [[scd-type-2]] · [[scd-type-1-and-3]] · [[scd-hybrid-types-5-6-7]] · [[surrogate-keys]] · [[dimensional-modeling]]*

## Open questions
- **source gap**: Vu documents that Type 4 has two competing definitions in circulation but says there's "no official reason" for the divergence — which one (if either) actually traces back to Kimball's original intent, or whether they arose independently for different problems, is left unresolved.
