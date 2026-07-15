---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9.md
last_updated: '2026-07-15'
qc: passed
slug: data-access-control-layers
topics:
- data-pipeline-design-framework
---

Vu Trinh describes a specific failure pattern that motivates access-control design: a team ships fast early on by giving everyone broad access, promising to "tighten it up later." Time passes, hundreds of tables accumulate alongside a handful of sensitive datasets, and any user can reach all of them. The first security audit forces a full month of retrofitted access control, done while hoping nothing has already leaked or been deleted by someone who shouldn't have had write access in the first place.

His design-time questions: does the serving infrastructure need to sit in a private network or can it be publicly reachable; which teams or services can connect, and how are permissions granted and revoked; do different users need different rows or columns, or just different tables? He then lays out five enforcement levels, from broadest to narrowest. Infrastructure: private VPCs, private endpoints, IP allowlists — usually requiring the infrastructure team. Service: service accounts, API keys, IAM roles, credential rotation — verifying which caller (warehouse, dashboard, API endpoint) is actually authorized. Table: granting or revoking access at the dataset or table level — the most common layer, handled natively by most warehouses. Row-level: policies supported by Snowflake, BigQuery, and Databricks, or a filtered view with its own grants, restricting which rows a given user can see. Column-level: different users seeing different fields within the same table, supported by some warehouses but not universally.

A concrete instance of the service-level layer — using an IAM role rather than a long-lived key so a caller (Snowflake, in that case) never has to be handed a secret at all — is [[iam-user-vs-role-based-auth-for-pipelines]].

*See also: [[credentials-and-configuration-management]] · [[iam-user-vs-role-based-auth-for-pipelines]] · [[safe-writes-and-schema-evolution-in-serving]]*
