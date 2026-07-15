---
persona: vutr
kind: entity
sources:
- raw/linkedin-data-infrastructure/4-trillion-events-daily-at-linkedin.md
last_updated: '2026-07-15'
qc: passed
slug: apache-beam
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Apache Beam is a programming model that defines batch and streaming data-parallel processing as one thing: it lets you specify the desired computation according to the Dataflow model — Google's real-time processing model for both bound (batch) and unbound (streaming) data sets — without committing to the engine that will actually execute it. Beam was released as open source in 2016, with SDK support for Python, Go, and Java, and its explicit goal is to let one multi-language pipeline definition run on whichever runner (execution engine) fits the job.

That runner independence is what made Beam useful to LinkedIn specifically: LinkedIn already had two mature engines — Samza for real-time streaming and Spark for batch — and rather than replace either one, LinkedIn built a Samza runner for Beam in 2018, so an existing pipeline written against the Beam API could execute on Samza for the streaming case or on Spark for the batch case, with the same business logic underneath. By 2019, Beam pipelines were powering several of LinkedIn's critical use cases (see [[unified-batch-stream-pipelines-via-beam]] for the concrete before/after results this unlocked).

The Beam SDK also gives LinkedIn engineers a way to package logic for reuse: pipelines can be built as standard PTransforms — the SDK's unit of composable processing logic — which then act as building blocks other teams can assemble into new pipelines rather than writing from scratch. LinkedIn wrapped this SDK-level reuse into an internal platform, [[managed-beam-platform]], that adds a control plane, operational tooling, and automated scaling on top of raw Beam.

*See also: [[managed-beam-platform]] · [[unified-batch-stream-pipelines-via-beam]] · [[linkedin-data-infrastructure]]*
