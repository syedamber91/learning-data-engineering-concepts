---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/my-framework-to-build-a-data-pipeline.md
last_updated: '2026-07-15'
qc: passed
slug: sink-first-requirements-gathering
topics:
- data-pipeline-design-framework
---

Vu Trinh's rule for where a pipeline design starts: "when building a pipeline, we should begin from the sink. More accurately, we should start from the end users." Before anything else, he asks whether the pipeline serves any real business purpose at all — his observation is that plenty of pipelines get built and are forgotten a week later because they never supported an actual business process, so this single question can save the work of building something useless.

From there the sink questions cascade in a specific order. Does the company have a data model? If yes, follow it for dims/facts/derived metrics; if a new business flow shows up, model it with a business user. If no data model exists, he doesn't wait for one — he models just the entities the pipeline needs, incrementally, so the pipeline still ships while leaving the door open for broader modeling later. Once modeling is settled, the expected output fields and how the output will be served (table, dashboard, CSV, API, web-app, ML training set) follow directly, and each serving mode implies its own infrastructure prep (build APIs? pick a CSV store? expose tables how?).

Staleness tolerance is the question that drives infrastructure choice hardest: it sets how often the source needs to be touched, and it determines whether he needs a low-latency serving option that reads from memory (a dedicated store like Pinot or Druid, or a warehouse sub-feature like BigQuery's BI Engine). Usage pattern — how users filter and join the output — decides partitioning and clustering choices, with the explicit trade-off that these optimizations always cost more on the write side, since data must be organized as it's written; naive writes are always faster than writes into a predefined layout. Retention follows the line "data is a product, a product with an expiration date," and drives lifecycle rules like archiving after two weeks or deleting after a year. Finally, atomicity — can the sink guarantee all-or-nothing writes? — determines retry safety; he illustrates the risk with local-filesystem downloads that aren't atomic even though the final object-storage upload is, which is how corrupted partial files leak into a sink that looks atomic but isn't. Sink firewalls (credentials, service accounts, private-network approvals) close out the list, since delays there can cost weeks.

*See also: [[source-constraints-and-schema-risk]] · [[data-grain-and-serving-storage-shape]] · [[physical-layout-partitioning-clustering-and-compaction]] · [[clarifying-questions-before-tools]]*
