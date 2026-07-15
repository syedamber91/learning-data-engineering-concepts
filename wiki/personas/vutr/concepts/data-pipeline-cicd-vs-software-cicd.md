---
persona: vutr
kind: concept
sources:
- raw/google-infrastructure/how-did-youtube-engineers-build-cicd.md
last_updated: '2026-07-15'
qc: passed
slug: data-pipeline-cicd-vs-software-cicd
topics:
- google-infrastructure
---

CI/CD for software is mature practice; CI/CD for data pipelines, per YouTube's engineers, is still a new practice without settled best-practice answers, and the gap traces back to fundamental differences between code and data rather than any tooling immaturity. Software tests compare deterministic output against a fixed expected result. Data has no such fixed target: it's dynamic in volume, variety, schema, semantics, and quality, and the very definition of "good" data shifts as the business evolves — so a data test might need synthetic data to be "big enough" to be meaningful, or its schema might need updating out from under it, before the test even runs. On top of that, data pipeline testing carries a security bar software testing usually doesn't: YouTube's pipelines touch information from billions of users, so test data itself has to be handled as sensitive.

The [[youtube-cicd-framework|YouTube CI/CD framework]] post also lists challenges beyond pure data complexity that a software CI/CD pipeline doesn't face in the same way. Replicating the production environment for testing is much harder: a production pipeline spans sources, distributed systems, cloud services, and on-demand hardware, and simply duplicating all of it for every test would be prohibitively expensive — which is exactly the problem [[production-aligned-test-environments-via-config-rewriting|the Configuration Rewriter]] exists to solve without full duplication. Deployment itself is a bigger lift than shipping a Docker image, because the infrastructure for testing and the data sources themselves have to be provisioned too. Observability has to work across a genuinely distributed system rather than a single deployable unit. And collaboration is harder because pipelines built by different teams routinely consume each other's output, so a CI/CD system has to guarantee that a change in one team's pipeline doesn't silently break another team's downstream pipeline — a failure mode software CI/CD's per-repository test suites don't usually have to reason about at all.

*See also: [[youtube-cicd-framework]] · [[production-aligned-test-environments-via-config-rewriting]]*
