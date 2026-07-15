---
persona: vutr
kind: concept
sources:
- raw/meta-data-stack-and-infrastructure/how-meta-solves-data-lineage-at-scale.md
last_updated: '2026-07-15'
qc: passed
slug: data-lineage-signal-collection
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Meta's data lineage problem wasn't tracking data flows in the abstract — it was doing it accurately enough, at high enough confidence, across three structurally different kinds of systems, to power privacy enforcement (the [[policy-zone-manager]]) for something as sensitive as a user's religious views. Manual approaches — diagrams, spreadsheets — had already failed to keep up with the volume and pace of change once Meta's Privacy-Aware Infrastructure (PAI) expanded to all of its apps, which is what forced automated signal collection; the automation itself is genuinely three different techniques stitched to three different substrates.

For web-system activity, Meta combines static and runtime analysis. Static analysis "simulates" code execution across the stacks of function calls (which can cross languages like C++ and Python) to find candidate paths from a data source — a form, an API endpoint — through transformations to a sink such as a database table or log file, without ever running the program. But static analysis alone misses runtime-only behavior like conditional logic driven by user input, so Meta layers real-time signal capture on top: it captures and compares actual payloads at the source and the sink during live request execution, and buckets the evidence into "match sets" (high-confidence flow matches) versus "complete sets" (broader, lower-confidence matches routed to human review). The source is explicit about where confidence breaks down: if a sink payload is an exact echo of the source payload plus incidental fields (their example: a timestamp added), Meta is confident the flow is real; if the sink payload is a "more compacted and abstracted" transformation of the source (a raw religion value collapsing into a `religion_count`), the tool isn't sure, and a human has to review it. Meta doesn't publish the actual rule that sets the confidence threshold between those two cases.

For data-warehousing activity, the technique changes again: Meta combines runtime instrumentation with static analysis of the SQL queries themselves (from Presto and Spark), using contextual runtime information like job IDs to fill in connections the static SQL analysis alone would miss. For AI systems, lineage means tracking relationships between datasets, models, and workflows, built by integrating runtime signals from libraries like PyTorch and from workflow engines like FBLearner Flow into the same kind of lineage graph. The common thread across all three: pure static analysis is never sufficient by itself, and every substrate needs its own runtime instrumentation layered on top to catch what static analysis structurally can't see.

*See also: [[policy-zone-manager]]*

## Related in the other wiki
- [[Privacy and Tracking]] — DDIA's chapter argues that once data is collected as a byproduct of user activity rather than deliberately submitted, the collector's interests and the user's interests can diverge; Meta's lineage effort is the concrete infrastructure a company builds once it decides those flows need to be traced and governed for privacy compliance rather than left opaque, though the two sources disagree in spirit about how much such tracing actually changes the underlying dynamic the DDIA chapter calls "surveillance."
