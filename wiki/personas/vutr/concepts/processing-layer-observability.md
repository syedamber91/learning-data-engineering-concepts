---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9-4c5.md
last_updated: '2026-07-15'
qc: passed
slug: processing-layer-observability
topics:
- data-pipeline-design-framework
---

Vu Trinh anchors processing-layer observability in four named primitives, each with a distinct job. Logging tells you what happened, and its usefulness is entirely a function of how well the code that emits it was written. Monitoring continuously checks the running system against expectations, so deviations surface before they become incidents. Alerting routes a signal to the right person, through the right channel, with the right urgency. Tracing connects cause to effect across steps — without it you know something broke, but finding the root cause is much harder.

Applied to a real processing layer, he grounds each primitive in specifics. Monitoring: record counts in vs. out at each step, null rates on critical fields, duplicate rates, quarantined-record counts, reconciliation against source counts — this is the runtime enforcement of everything in [[data-quality-rules-and-anomaly-detection|data quality]] — plus infrastructure signals (CPU/memory, disk I/O, network throughput, consumer lag for streaming, task-duration trends, cost per run). He's explicit that validation results should be centralized in one place rather than split between the orchestration layer and CI/CD. Logging, at the processing layer, means task startup/shutdown events and error messages. Alerting needs a severity gradient tied to downstream business impact — a non-critical job failure is a Slack message, but a primary key showing 20% nulls in a production revenue table is a company-wide alert; urgency should scale with how close the affected data sits to an actual business decision. Tracing is where lineage does its work: answering "why is this number wrong" by following data backward through the pipeline, and "what breaks if I change this" by following it forward — the two directions of the same dependency graph.

*See also: [[data-quality-rules-and-anomaly-detection]] · [[dead-letter-queue-and-bad-data-isolation]] · [[pipeline-failure-recovery-and-checkpointing]]*
