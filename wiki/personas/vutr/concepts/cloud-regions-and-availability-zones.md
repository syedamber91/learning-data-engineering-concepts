---
persona: vutr
kind: concept
sources:
- raw/cloud-kubernetes-docker-infrastructure-tooling/how-to-start-learning-cloud-as-a.md
last_updated: '2026-07-15'
qc: passed
slug: cloud-regions-and-availability-zones
topics:
- cloud-kubernetes-docker-infrastructure-tooling
---

A **region** is a physical cluster of data centers in a specific geographic location — Vu's examples are AWS's `us-east-1` (Virginia), `ap-southeast-1` (Singapore), and `eu-west-1` (Ireland), with GCP and Azure offering equivalent setups. Regions are completely independent of one another. Inside a region sit multiple **availability zones (AZs)**: separate physical facilities, each with its own independent power and networking, specifically so that one zone's failure doesn't take down the others.

Region choice isn't cosmetic — Vu names three concrete costs it drives. **Latency**: if application servers sit in Singapore and the data warehouse sits in the US, every query crosses the Pacific, adding tens to hundreds of milliseconds per round trip. **Service availability**: not every managed service is available in every region — newer services often launch in a flagship region like `us-east-1` first and take months to reach others. **Cross-region/cross-zone cost**: data transfer within the same region and same AZ is free or nearly free, but the moment data crosses a region or zone boundary, egress charges kick in — a cost Vu calls "often overlooked" but capable of "significantly" moving the bill. His rule of thumb follows directly from this: every service you provision — storage, compute, database — should live in the same region. Companies do sometimes spread services across regions deliberately (e.g., different business teams serving different geographies), but doing so means consciously owning the cross-region transfer cost whenever data has to move between those services, such as pulling historical data from a regional service into a centralized warehouse.

This concept sits underneath Vu's broader cloud-learning advice: pick one cloud vendor and stick with it rather than learning two or three at once, on the reasoning that the region/AZ fundamentals (and the interaction/access-control/cost/observability layer built on top of them — see [[cloud-access-cost-and-observability-fundamentals]]) transfer once you eventually need a second cloud.

*See also: [[cloud-access-cost-and-observability-fundamentals]] · [[cloud-compute-abstraction-spectrum]] · [[object-storage-as-data-lake-backbone]]*
