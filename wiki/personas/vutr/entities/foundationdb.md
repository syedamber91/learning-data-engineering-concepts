---
persona: vutr
kind: entity
sources:
- raw/snowflake-internals/i-spent-8-hours-diving-deep-into.md
- raw/snowflake-internals/i-spent-another-6-hours-understanding.md
last_updated: '2026-07-15'
qc: passed
slug: foundationdb
topics:
- snowflake-internals
---

FoundationDB is the free, open-source, multi-model distributed NoSQL database that Snowflake uses internally, inside its Cloud Services layer, to manage its data catalog. Earlier coverage of Snowflake's 2016 architecture paper only describes this piece abstractly, as a "global key-value store" that tracks which file additions and removals belong to which version of a table; later coverage names the actual system as FoundationDB. Concretely, it's the metadata store that makes [[snapshot-isolation-and-immutable-file-versioning]] possible: because table data itself lives in immutable object storage and can only change by adding or removing whole files, FoundationDB is what records, for any given table version, exactly which set of files constitutes it — which in turn is what backs time travel, `UNDROP`, and zero-copy cloning.

*See also: [[snapshot-isolation-and-immutable-file-versioning]] · [[snowflake]]*
