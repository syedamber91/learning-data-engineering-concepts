---
persona: vutr
kind: entity
sources:
- raw/data-pipeline-design-framework-additional/i-spent-12-hours-rebuilding-my-junior.md
last_updated: '2026-07-15'
qc: passed
slug: iam-user-vs-role-based-auth-for-pipelines
topics:
- data-pipeline-design-framework
---

Minh Pham's rebuilt Skytrax pipeline (guest-posted on Vu Trinh's publication) authenticates two completely different callers against the same S3 bucket using two deliberately different AWS mechanisms, and the post is explicit about why each fits its caller. Airflow, reading and writing raw/processed files, authenticates as an **IAM User** (`skytrax-airflow-dev`): Terraform provisions it with a long-lived access-key pair (access key ID + secret), which gets baked directly into the Airflow connection URI in `.env`. This is direct, user-level authentication — every S3 call carries the key — and it's the right fit specifically because Airflow runs in a Docker container without access to an AWS instance-metadata service that could otherwise supply temporary credentials automatically.

Snowflake, reading from S3 during `COPY INTO` via an external stage, instead assumes an **IAM Role** (`skytrax-snowflake-s3-dev`). Under the hood, Snowflake has its own internal AWS account with its own IAM users, and it assigns one of *those* internal users to the customer's stage; when `COPY INTO` runs, that internal user calls `sts:AssumeRole` on the customer's role to obtain temporary, auto-rotating credentials, then uses those to read from S3. Snowflake itself never sees a long-lived secret.

The setup has a genuine chicken-and-egg problem the post calls out by name: the role's trust policy has to name the specific ARN of Snowflake's internal IAM user before that user can assume it, but that ARN is only revealed *after* the Snowflake stage has already been created (via `STORAGE_AWS_IAM_USER_ARN` in `DESCRIBE STAGE` output). The fix is a two-pass Terraform apply — create the role first with a trust policy scoped to the customer's own account, create the Snowflake stage, retrieve the internal ARN, feed it back into the AWS module's `tfvars`, and re-apply so the trust policy now also trusts Snowflake's user. The stated rationale for the split, end to end: long-lived credentials suit Airflow because it needs to work reliably in an environment without a metadata service, while the role gives Snowflake scoped, temporary, auto-rotating access without either side ever manually sharing a secret. All of it — the S3 bucket (versioned, encrypted, lifecycle-tiered to Infrequent Access after 30 days, public access fully blocked), the IAM user, the IAM role, and their policies — is provisioned as 11 Terraform-managed resources, torn down cleanly with a single `terraform destroy`.

*See also: [[credentials-and-configuration-management]] · [[data-access-control-layers]] · [[staging-area-raw-to-processed]]*
