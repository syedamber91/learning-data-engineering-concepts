---
persona: vutr
kind: concept
sources:
- raw/uber-data-infrastructure-case-studies/i-spent-3-hours-learning-how-uber.md
last_updated: '2026-07-15'
qc: passed
slug: uber-data-quality-standardization
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Before Uber built its data quality platform, it had no standardized data quality measurements across teams, tests were manually authored per dataset, incident management needed improvement, and alerting had no standardized/automated method — all against hundreds of services, ML models, and thousands of datasets where bad data has direct operational consequences. Uber's response was to collect the recurring failure patterns its internal users and past incidents actually surfaced — data arriving late, data missing or duplicated, data discrepancies between data centers, and incorrect data values — and turn each into a formal, computable test category.

**Freshness** measures the delay after which data is 99.9% complete; the assertion passes if `current_timestamp - latest_timestamp_where_data_is_99.9%_complete < freshness SLA`. **Completeness** measures the row-completeness percentage; it passes if `downstream_row_count / upstream_row_count > completeness SLA`. **Duplicates** measures the percentage of rows sharing a duplicate primary key; it passes if `(1 - primary_key_count) / total_row_count < duplicates SLA`. **Cross-datacenter Consistency** measures data loss between a dataset's copy in the current data center and its copy in another, by comparing row counts; it passes if `min(row_count, row_count_other_copy) / row_count > consistency SLA`. **Others** is the escape hatch for anything requiring complicated, business-logic-specific checks, defined as user-defined tests rather than an auto-generated formula.

This test taxonomy is what Uber's [[uber-data-quality-platform-architecture|data quality platform architecture]] actually executes at scale (currently covering 2,000+ datasets and catching ~90% of data quality incidents), and it's also the mechanism behind the write-audit-publish gate Uber layers onto its Hudi ETL pipelines ([[uber-hudi-etl-pipeline-and-impact]]).

*See also: [[uber-data-quality-platform-architecture]] · [[uber-hudi-etl-pipeline-and-impact]]*
