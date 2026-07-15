---
persona: vutr
kind: concept
sources:
- raw/netflix-data-infrastructure/netflix-data-engineer-stack.md
last_updated: '2026-07-15'
qc: passed
slug: write-audit-publish-pattern
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Netflix's data-quality step in its batch pipeline (see [[netflix-batch-pipeline-four-steps]]) leans on the Write-Audit-Publish (WAP) pattern. The mechanism: Netflix first writes new data to a hidden Iceberg snapshot — invisible to normal readers — and then runs it through an internal data auditor tool. Only if the audit passes is that snapshot exposed to users.

The reason this pattern needs Iceberg specifically (rather than any table format) is that Iceberg's snapshot/branching model lets Netflix avoid copying data during the audit step.

WAP sits alongside more conventional testing in Netflix's quality step: native unit test libraries (PyTest or ScalaTest) plus a Spark-specific unit test library for pipeline logic, and a tool called Dataflow Mock Generation that generates mock data based on what's actually in the warehouse — so tests run against realistic data shapes rather than hand-crafted fixtures.

*See also: [[netflix-batch-pipeline-four-steps]] · [[maestro-workflow-orchestrator]]*
