---
persona: vutr
kind: entity
sources:
- raw/netflix-data-infrastructure/netflix-data-engineer-stack.md
last_updated: '2026-07-15'
qc: passed
slug: maestro-workflow-orchestrator
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Maestro is Netflix's workflow scheduler, the "scheduling" step of its four-step batch pipeline (see [[netflix-batch-pipeline-four-steps]]). It handles an impressive 70,000 workflows and 500,000 job steps every day. Users set job frequencies with either event-based triggers or a time-based scheduler, and define workflows in YAML or Python.

Maestro ships many standard steps analogous to Airflow Operators — Spark Jobs, Data Audits, and Email Sending among them. For anything not covered by a standard step, Netflix provides a wrapper API that gives access to various underlying engines through a single interface, so users can build custom steps without having to learn each engine's low-level API and its particular semantics.

*See also: [[netflix-batch-pipeline-four-steps]] · [[write-audit-publish-pattern]] · [[keystone-real-time-platform]]*
