---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/my-framework-to-build-a-data-pipeline.md
last_updated: '2026-07-15'
qc: passed
slug: source-constraints-and-schema-risk
topics:
- data-pipeline-design-framework
---

Vu Trinh's source-side questions come after the sink questions are settled, because by then he already knows how the output must look and how fresh it must be — the source questions exist to check whether the world actually supplies what the sink needs. First: what type of source is it — an API, a database, or something that pushes data to you? The answer sets the retrieval infrastructure directly: periodic file exports or change data capture for a database, a defined calling pattern for an API, a consumption mechanism for a stream.

How often the source must be touched is the mirror image of the sink's staleness question: daily/weekly needs can run on a cron job, while low-latency needs mean data must flow continuously, potentially requiring a CDC pipeline to be built just to make the stream available. Touching the source has a cost, though — his next question is how source performance will be impacted: does a database export affect read/write performance enough to need a read replica coordinated with the backend team, or does an API rate-limit impose a ceiling on call frequency?

Source retention sets a hard boundary: if the pipeline needs a week of history but the source only keeps two days, no amount of clever engineering fixes that — the choice is renegotiating the required range with end users or finding another source, and this same constraint is what determines whether a [[backfilling-data-pipelines|backfill]] is even possible later. Schema sufficiency (does the source have the fields the sink needs?) and schema-change notification (how will you know if columns get renamed, dropped, or added?) are treated as two separate risks — knowing the schema today says nothing about whether it will still be true tomorrow, and a pipeline that assumes a fixed schema will break the moment it changes without warning. Source firewalls close the list, for the same credential-and-access reasons as the sink side.

*See also: [[sink-first-requirements-gathering]] · [[backfilling-data-pipelines]] · [[clarifying-questions-before-tools]]*
