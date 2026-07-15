---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/my-framework-to-build-a-data-pipeline.md
- raw/data-pipeline-design-framework-additional/how-to-build-a-data-pipeline-thats.md
last_updated: '2026-07-15'
qc: passed
slug: clarifying-questions-before-tools
topics:
- data-pipeline-design-framework
---

"You cannot simply say, 'I'll use Spark, Kafka, and so on'; you need to ask clarifying questions to gather information for proposing a robust data pipeline." That line is Vu Trinh's explicit thesis for how he approaches pipeline design, in an interview or on the job: the tool choice is downstream of a set of questions, not the starting point. He organizes those questions into three buckets — sink, source, and middle steps — reasoning that separating each component's concerns lets him plan each one better, and he is explicit that the list reflects only his own current experience, not a complete taxonomy.

He restates the same instinct from the opposite direction in his satirical "how to build a pipeline that sucks" piece: the anti-pattern is choosing infrastructure by hype rather than by requirement — provisioning for 20PB when the pipeline runs on 20GB, defaulting to Spark and streaming because a big company might need it, chasing whatever tool just trended on LinkedIn or Twitter, and avoiding mature, battle-tested, well-integrated tools specifically because they would make the pipeline more likely to succeed. His corrective, stated plainly in that post's outro, is to keep the pipeline as simple as possible: use mature tools, keep the tool count minimal (more tools mean more to operate, maintain, and monitor), follow what the team already has (frameworks, guidelines, templates, data modeling), and check for reuse — intermediate tables, functions, processing clusters — before building anything new. Respecting the business requirement and giving the end users' actual needs priority over technical ambition is, in his framing, the discipline that clarifying questions exist to enforce.

*See also: [[sink-first-requirements-gathering]] · [[source-constraints-and-schema-risk]] · [[batch-vs-stream-throughput-and-latency]] · [[business-rules-and-data-modeling-drift]]*
