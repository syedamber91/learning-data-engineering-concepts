---
persona: vutr
kind: concept
sources:
- raw/cloud-kubernetes-docker-infrastructure-tooling/how-to-start-learning-cloud-as-a.md
last_updated: '2026-07-15'
qc: passed
slug: cloud-compute-abstraction-spectrum
topics:
- cloud-kubernetes-docker-infrastructure-tooling
---

Vu's framing is that every cloud compute service is backed by the same physical servers — what differs between services is how much control the user retains over that server. At one end sit **virtual machines** (AWS EC2 is his example): you rent a server and can customize nearly everything — RAM, CPUs, disk, OS. In the middle sit higher-level abstractions that deploy applications faster while still being "backed by a set of virtual machines" whose cost still shows up on the bill — his examples are managed Kubernetes services (available on every major cloud) and Spark-on-YARN clusters. At the top sit **serverless** services, used as if the underlying VMs were invisible entirely.

For a data engineer specifically, Vu's claim is that VMs, one serverless option (he names AWS Lambda), and — to some extent — Kubernetes services are "enough." VMs are, like object storage, beginner-friendly: default networking and security settings are usually sufficient, and the user only needs to choose region, CPU count, RAM, disk, and OS (e.g., Ubuntu, Debian). Stopping a VM when it's not needed avoids being charged for it (new accounts are also typically capped from provisioning very large/expensive machines, a guardrail against runaway learning costs). His suggested on-ramp for getting comfortable with a VM specifically: instead of running `docker-compose` on a laptop, run it on the rented VM instead.

Once the fundamentals (interaction, access control, cost, observability — see [[cloud-access-cost-and-observability-fundamentals]]) and the storage/compute basics are in hand, Vu's next tier is the set of **data-lifecycle services**: orchestration (e.g., a cloud-managed Airflow, or AWS Step Functions), distributed data processing (e.g., AWS EMR, Google Dataproc), and data warehousing (e.g., AWS Redshift, Google BigQuery, Snowflake). If you already know the on-prem/open-source equivalents, his claim is that the only new thing to learn is *how to run them in the cloud* — the same conceptual swap that other posts of his make concrete, e.g., submitting a Spark job to a YARN cluster on AWS instead of a local standalone cluster, or Kubernetes itself as one of the resource clusters a Spark job can run against (see [[spark-on-kubernetes-execution-model]]). Because these services' pricing models are often less straightforward than a VM's, his rule of thumb is to always start with the minimal setup to keep learning costs low, and to remember that most of them don't charge for stopped time either — only scaling the setup up once you've gained confidence.

Optionally, once comfortable operating cloud services by hand, Vu names **Infrastructure as Code (IaC)** — defining infrastructure in text files rather than clicking through a console — as the next layer, specifically to solve the "three months later, you don't remember what you built or why" problem of manual provisioning. He names Terraform as the dominant, cloud-agnostic tool, and frames IaC's data-engineer use cases as spinning up CI environments or replicating dev/staging/prod environments consistently — but explicitly not a first-things-to-learn item; his own practice is to consult or request the infrastructure team for IaC setup rather than own it personally.

*See also: [[kubernetes]] · [[docker]] · [[cloud-regions-and-availability-zones]] · [[object-storage-as-data-lake-backbone]]*
