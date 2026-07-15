---
persona: vutr
kind: entity
sources:
- raw/netflix-data-infrastructure/netflix-data-engineer-stack.md
- raw/netflix-data-infrastructure/netflixs-trillions-scale-real-time.md
last_updated: '2026-07-15'
qc: passed
slug: mantis-observability-agent
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Mantis is Netflix's tool for ad-hoc, real-time investigation of raw data events. A user configures a Mantis agent to listen to a raw stream; the agent receives the user's query and lets them investigate or debug the stream live, without a full pipeline or batch job standing between them and the data.

Mantis is also the operational half of Netflix's founding real-time-infrastructure split: when Netflix separated concerns between analytics and operations, it built Mantis for operational use cases and [[keystone-real-time-platform]] for analytics. That split mattered because the two concern sets pull in different directions — analytical stream processing prioritizes correctness and predictability, while operational stream processing prioritizes cost-effectiveness, latency, and availability. Keeping them as separate tools let each optimize for its own priorities rather than compromise on both.

*See also: [[keystone-real-time-platform]] · [[netflix-streaming-platform-build-and-failure-recovery]]*
