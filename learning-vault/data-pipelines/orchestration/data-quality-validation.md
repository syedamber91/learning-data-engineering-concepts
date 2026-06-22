---
title: "Data Quality & Validation"
area: "Data Pipelines"
topic: "Orchestration"
tags: [data-quality, validation, freshness, checks]
---

# Data Quality & Validation

*Part of [[orchestration-moc|Orchestration]] · [[data-pipelines-moc|Data Pipelines]]*

**In one line:** Data quality checks make sure incoming data is complete, valid, and sensible *before* anyone trusts it.

**Picture this:** A passport-control officer at the airport. Before you enter the country, they check your passport isn't expired, the photo matches, and the dates make sense. Validation is passport control for data — bad records get stopped at the gate.

**How it actually works:** As data flows through a pipeline, you run automated checks: are required fields missing (null)? Are values in a sensible range (age isn't −5 or 900)? Are IDs unique? Is the data *fresh* — did today's file actually arrive? If a check fails you "fail fast": stop the pipeline and alert someone, rather than letting wrong numbers reach a dashboard where they'd be believed.

**In the real world:** Netflix runs quality checks on viewing data before it feeds recommendation models. If a broken upload made half the "watch" events vanish, a freshness-and-volume check catches it — otherwise the app might suddenly recommend the wrong shows to millions.

**Why you'd use it (and when not to):** Add checks wherever bad data would cause wrong decisions — which is almost everywhere serious. The cost is a little extra runtime and maintenance, so a quick personal experiment may not need formal validation.

**Connects to:** [[dags-schedulers]] · [[idempotency]] · [[automated-testing]]
