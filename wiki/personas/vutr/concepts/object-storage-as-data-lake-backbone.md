---
persona: vutr
kind: concept
sources:
- raw/cloud-kubernetes-docker-infrastructure-tooling/how-to-start-learning-cloud-as-a.md
last_updated: '2026-07-15'
qc: passed
slug: object-storage-as-data-lake-backbone
topics:
- cloud-kubernetes-docker-infrastructure-tooling
---

Vu calls object storage (S3 on AWS, GCS on GCP, Blob Storage on Azure) "the backbone of every modern data architecture," and treats it as the correct first cloud service for anyone to actually touch. Unlike a computer's file hierarchy, object storage manages data as **objects** inside a **flat structure**, grouped into containers called **buckets** — no real nested folders, just objects that can *look* organized by naming convention. Because it can "store anything," it's the natural home for a data lake: raw data lands there first, centralized, before other services consume it.

Learning object storage well means learning three things, in his framing. First, **storage classes**: vendors offer multiple classes trading storage cost against request cost — the higher (more expensive-per-GB) the class, the cheaper each request against it, so hot, frequently-accessed data belongs in a class like S3 Standard while cold, rarely-touched data belongs in something like S3 Glacier Deep Archive. Second, **lifecycle management**: a configuration feature that automatically moves objects to a different (typically cheaper/colder) storage class, or expires objects and old versions, without manual intervention. Third, **read/write performance**: for large objects, vendors offer optimizations like multipart upload (uploading an object's parts simultaneously) and ranged reads (fetching only a byte range of an object to save bandwidth) — both S3 and GCS support these.

Vu's practical case for starting here: object storage is one of the friendliest services for a new learner because it's cheap (around $25 for 1TB in the standard class — a side project's few MBs or GBs costs under $5/month, easily covered by free credits) and because the default setup is already safe (vendors prevent a new bucket from being publicly exposed by default). Interacting with it also stays conceptually simple, centering on three actions: LIST, PUT, GET. His concrete first exercise: create an account and a bucket, then adjust a Python script to read/write against object storage (with proper credentials) instead of the local filesystem — the on-ramp he recommends before touching any other cloud data service, including compute (see [[cloud-compute-abstraction-spectrum]]).

*See also: [[cloud-regions-and-availability-zones]] · [[cloud-access-cost-and-observability-fundamentals]] · [[aws-glue]]*
