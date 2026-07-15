---
persona: vutr
kind: concept
sources:
- raw/airbnb-data-infrastructure/how-did-airbnb-build-their-semantic.md
last_updated: '2026-07-15'
qc: passed
slug: minerva-data-versioning
topics:
- airbnb-data-infrastructure
---

Minerva's "Consistent" design principle rests on one mechanism: the data version. Internal users at Airbnb frequently changed Minerva's metric and dimension definitions, and Airbnb needed a way to guarantee that a dataset always reflected its current definition rather than silently drifting from it. The data version is a hash of all the essential fields specified in a definition — for example, the data source. Whenever a user changes any field that feeds that hash, the data version updates automatically, and each dataset carries its own data version.

The consequence is what makes this more than bookkeeping: because the data version changes automatically the moment a defining field changes, Minerva can automatically create and backfill a new dataset whenever that happens. This propagates upstream changes to every downstream dataset without a human having to notice a change and manually trigger a rebuild — and it's the mechanism that ensures no Minerva dataset diverges from the source of truth. Where Airbnb's pre-Minerva core_data problem was that nobody could tell whether two tables answering the same question were still in sync, data versioning makes staleness a structural impossibility rather than a debugging exercise: if the version doesn't match, a backfill is already underway.

*See also: [[minerva]] · [[minerva-backfill-and-staging-environment]]*
