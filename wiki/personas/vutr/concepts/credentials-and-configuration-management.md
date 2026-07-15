---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/my-framework-to-build-a-data-pipeline.md
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9-4c5.md
last_updated: '2026-07-15'
qc: passed
slug: credentials-and-configuration-management
topics:
- data-pipeline-design-framework
---

Vu Trinh's rule for credentials and configuration is stated the same way across both his sink/source/middle-steps framework and his deeper processing-layer piece: don't hardcode them. Most orchestration frameworks expose an interface for managing credentials and config directly; if a team doesn't use one, every major cloud offers a secrets/config management service instead. The direct payoff is portability — a pipeline that reads its credentials and config from an external, swappable source can run across dev, staging, and prod environments unchanged, since only the input values differ per environment, not the pipeline itself.

The deeper piece adds a distinction the framework version doesn't make: configuration that affects business logic — thresholds, date ranges, processing parameters — is a different animal from a plain secret, and it should be versioned alongside the pipeline code rather than just stored securely. His example is concrete: if the "active user" lookback window changes from 30 days to 60, that change needs to be traceable, reviewable, and reversible, which a bare secrets-manager entry doesn't give you — it needs to live in the same review process as the code that depends on it.

A concrete, worked instance of the credentials half of this principle — two entirely different auth mechanisms used deliberately for two different callers in the same pipeline — is [[iam-user-vs-role-based-auth-for-pipelines]].

*See also: [[iam-user-vs-role-based-auth-for-pipelines]] · [[business-rules-and-data-modeling-drift]] · [[data-access-control-layers]]*
