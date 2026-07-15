---
persona: vutr
kind: entity
sources:
- raw/data-pipeline-design-framework-additional/i-spent-12-hours-rebuilding-my-junior.md
last_updated: '2026-07-15'
qc: passed
slug: snowflake-copy-into-and-event-driven-orchestration
topics:
- data-pipeline-design-framework
---

The Skytrax rebuild (Minh Pham's guest post on Vu Trinh's publication) chains three Airflow DAGs — `skytrax_crawl` (extract), `skytrax_process` (transform), `skytrax_snowflake` (load) — using **Airflow Datasets** rather than separate schedules: `skytrax_crawl` emits a `skytrax://raw` dataset when it finishes, which triggers `skytrax_process` automatically; that emits `skytrax://processed`, which triggers `skytrax_snowflake`. The load DAG uses dynamic task mapping to spin up one `load_date` task per review date the crawler actually found, so five dates found means five parallel load tasks rather than one task looping over five dates.

The load step itself runs a fixed `COPY INTO` template per date:

```sql
COPY INTO SKYTRAX_REVIEWS_DB.RAW.AIRLINE_REVIEWS
FROM @SKYTRAX_REVIEWS_DB.RAW.SKYTRAX_S3_STAGE/{{ s3_key }}
ON_ERROR = 'CONTINUE'
PURGE    = FALSE;
```

`ON_ERROR = 'CONTINUE'` means a handful of bad rows in a file don't block the rest of that file from loading. `PURGE = FALSE` keeps the source file in S3 after a successful load rather than deleting it, specifically so it's still there if a rerun is ever needed. The property the post highlights as effectively free: Snowflake internally tracks which files have already been loaded into a given stage/table, so running the identical `COPY INTO` a second time over the same file does not create duplicate rows — the mechanism is idempotent by default, without the pipeline author having to build any deduplication logic themselves (compare the [[idempotency|hand-built idempotency techniques]] needed elsewhere, like overwrite-by-partition or MERGE, when the target system doesn't give you this for free).

*See also: [[staging-area-raw-to-processed]] · [[idempotency]] · [[iam-user-vs-role-based-auth-for-pipelines]]*
