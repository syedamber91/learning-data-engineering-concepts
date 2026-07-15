---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/i-spent-12-hours-rebuilding-my-junior.md
last_updated: '2026-07-15'
qc: passed
slug: staging-area-raw-to-processed
topics:
- data-pipeline-design-framework
---

In Minh Pham's guest post for Vu Trinh's publication, rebuilding a junior-year scraping project into an Insurify-style pipeline, the design choice under the microscope is why data passes through a "raw" and then a "processed" prefix in S3 before it ever reaches Snowflake, instead of loading everything straight into the warehouse and doing all transformation in dbt. He gives seven concrete reasons, drawn from what Insurify itself does in production: early data validation, catching issues before they reach the warehouse; better observability into incoming partner files before they're loaded; support for a partner-delivery workflow, where external partners drop reports directly into the raw directory over SFTP, so validation has to happen before those files ever touch the warehouse; pre-processing outside dbt using Python scripts to clean, standardize, and validate; catching incremental issues sooner — missing columns or schema changes detected at the raw→processed step rather than downstream; faster alerting, since a missing required column can trigger an immediate Slack notification right at that boundary; and cleaner warehouse inputs overall, since only validated, structured data ever gets loaded, which keeps every downstream dbt model more reliable.

The pipeline's actual shape makes this concrete: `scraper.py` writes raw CSVs partitioned by year/month/date, `processing.py` cleans them into a matching processed prefix, and only the processed files get picked up by the Snowflake load step — meaning the raw/processed split is a deliberate quality gate placed before the warehouse boundary, not just a filesystem convention.

*See also: [[data-quality-rules-and-anomaly-detection]] · [[snowflake-copy-into-and-event-driven-orchestration]] · [[iam-user-vs-role-based-auth-for-pipelines]]*
