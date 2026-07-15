---
persona: vutr
kind: concept
sources:
- raw/snowflake-internals/i-spent-8-hours-diving-deep-into.md
- raw/snowflake-internals/i-spent-another-6-hours-understanding.md
last_updated: '2026-07-15'
qc: passed
slug: snapshot-isolation-and-immutable-file-versioning
topics:
- snowflake-internals
---

Snowflake gets its ACID guarantee from Snapshot Isolation (SI): a transaction sees a consistent view of the database as of the moment it started. What makes Snowflake's implementation of SI worth studying isn't the isolation semantics themselves so much as how tightly they're welded to the storage layer underneath. SI is implemented on top of multi-version concurrency control (MVCC), meaning a copy of every change to a table is preserved for a period of time — and that "copy every change" choice isn't optional in Snowflake's case, it's forced by the fact that table data lives in object storage. S3 objects can't be overwritten or appended to, so the *only* way to modify a table is to write a whole new immutable file containing the change. A row update, in other words, cannot be an in-place mutation the way it might be on a local disk-backed database — it can only ever be "add a new file, remove an old one."

That constraint is what produces table versioning almost as a side effect of the storage model rather than as a deliberately engineered feature. Every insert, update, delete, or merge against a table adds and removes whole files relative to the previous version, and each such change yields a newer table version. File additions and removals are tracked in Snowflake's metadata store — the 2016 paper covering this describes it only as a "global key-value store," while later coverage names the actual system: FoundationDB (see [[foundationdb]]). That metadata layer is what lets Snowflake answer, for any table version, exactly which set of files belongs to it.

Because old file versions aren't deleted immediately — they're retained for a configurable duration, up to 90 days by default — the same mechanism that gives Snowflake SI/MVCC also gives it several user-facing features nobody would design SI to provide directly. Time travel lets a user query an earlier version of a table's data via `AT` or `BEFORE` syntax in SQL, using nothing more than the retained file history. `UNDROP` restores a dropped table, schema, or database using that same retained metadata. And cloning (`CLONE`) creates a new table with the same definition and data as a source table by copying only the *metadata* pointing at the source table's files — not the underlying files themselves — so a clone is cheap to create, and the original and the clone can then be modified independently without affecting each other, because subsequent changes to either one simply add/remove files relative to that table's own version history.

The throughline: because persistent storage is immutable object storage, "keep old versions around for MVCC" and "let users read/undo/duplicate old versions" turn out to be nearly the same mechanism wearing different names.

*See also: [[foundationdb]] · [[min-max-pruning-and-dynamic-data-skipping]] · [[snowflake]] · [[isolation-levels-and-mvcc]] · [[acid-in-olap]]*

## Related in the other wiki
- [[Snapshot Isolation and Repeatable Read]] — DDIA's chapter explains the general SI mechanism (a consistent read snapshot fixed at transaction start); Snowflake's version is the same guarantee forced into a specific shape by immutable object-storage files standing in for row versions.
