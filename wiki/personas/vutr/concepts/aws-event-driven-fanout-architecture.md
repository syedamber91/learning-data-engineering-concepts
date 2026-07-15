---
persona: vutr
kind: concept
sources:
- raw/cloud-kubernetes-docker-infrastructure-tooling/practical-data-engineering-using.md
last_updated: '2026-07-15'
qc: passed
slug: aws-event-driven-fanout-architecture
topics:
- cloud-kubernetes-docker-infrastructure-tooling
---

This architecture — shared on Vu's newsletter as a guest post by Junaid Effendi — chains together AWS's native pub-sub and serverless primitives into an end-to-end pipeline without introducing any third-party orchestration tool. It starts with **S3** as the object store, used either directly or through a lakehouse layer on top. An S3 event (a CSV file dropping, or any file landing under a given prefix) triggers **SNS**, configured to fan that single event out to multiple downstream subscribers — SNS's native filtering mechanism lets each subscriber only see the events it cares about.

**SQS** sits between SNS and its consumers as an optional but valuable decoupling layer: it turns the fan-out into asynchronous processing, which unlocks event replay (a dead-letter queue for failed messages, or resetting a message's visibility timeout so it reappears later for retry) and flexible scaling topologies — multiple SQS queues consuming the same SNS topic for different use cases, or a single SQS queue fed by multiple SNS topics. **Lambda** is the piece that actually does something with an event: in this architecture it listens to a single SNS topic attached to a single S3 bucket, acting as a centralized router that performs lightweight processing (parsing, transformation) and branches to different downstream services based on the event's content ("if A, then trigger B; if Y, then trigger Z"). The source notes one topology constraint worth remembering: if multiple Lambdas are involved, a separate SQS queue becomes necessary for each.

**Step Functions** is the orchestrator that stitches everything downstream into one place — the source's architecture runs a separate Step Function per data source, with Lambda acting as the proxy that triggers the right one, because Step Functions cannot be triggered directly from SQS or SNS. Inside a Step Function, several services get called depending on the workload: **Batch** runs custom code against a shared, user-provisioned compute environment for lightweight transforms, downloads, or file movements; **EMR** (Spark on EMR) handles the heavy, MPP-scale workloads, with the Step Function handling the entire cluster lifecycle — creating the cluster, submitting the Spark job, and terminating it once done; **Redshift**'s connector executes SQL statements for end-to-end processing or classic ETL loads; and **DynamoDB** can be called directly for operations like updating a table or running an import job, without custom code. In the source's example architecture, both the Batch and the EMR paths write their results to DynamoDB (for OLTP) and Redshift (for OLAP) after a successful run. Alerting is wired in via SNS attached to the components that need it — in this design, Lambda and the Step Functions themselves.

Vu (via the guest author) closes with a candid trade-off rather than a recommendation: whether this pattern is still the right choice today "depends." Building something from scratch with full organizational support favors a centralized modern orchestrator like Airflow, which can do this whole job within one system. But in an existing environment with real constraints, it's often easier to bolt one more native AWS service onto a working pipeline than to plan a migration off it — evaluating incrementally rather than reflexively reaching for the newer tool.

*See also: [[cloud-compute-abstraction-spectrum]] · [[object-storage-as-data-lake-backbone]] · [[aws-glue]]*
