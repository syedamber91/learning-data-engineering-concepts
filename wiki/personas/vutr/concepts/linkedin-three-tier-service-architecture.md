---
persona: vutr
kind: concept
sources:
- raw/linkedin-data-infrastructure/diving-deep-into-linkedins-data-infrastructure.md
last_updated: '2026-07-15'
qc: passed
slug: linkedin-three-tier-service-architecture
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Before any individual LinkedIn system makes sense on its own, it helps to see where it sits: LinkedIn's core infrastructure is organized into three logical service tiers, communicating over RPC. The data tier maintains persistent state — user data and the like. The service tier implements an API layer over that state. The display tier translates those APIs into the actual user interface. The service and display tiers are deliberately stateless, and statelessness is the whole point: because they hold no data of their own, adding or removing a node doesn't require moving any data around — a stateless node just reloads whatever it needs from the persistent (data) tier.

Underneath the data tier, LinkedIn's own paper breaks the core data system into five pieces, each with its own job: **Live storage** is a variant of a traditional OLTP database, powering web applications and serving most user-facing data requests — this is the role [[voldemort]] and [[espresso]] fill. **Stream systems** deliver data to applications and to other data systems — the role [[databus]] plays as LinkedIn's change-capture backbone. **Social Graph** serves graph queries, such as finding paths between users. **Recommendation and Search systems** power people search, one of LinkedIn's core features. **Batch computing** covers large-scale offline jobs run on a fixed schedule (hourly, daily), split into two categories: jobs that generate datasets consumed by the website's own users, and jobs that serve internal analytics.

The architectural discipline worth noticing is what's *not* here: no tier is asked to be both stateful and horizontally elastic at once. Statelessness is pushed up into the service and display tiers precisely so that the hard, expensive problem of resharding and rebalancing live data stays contained within the data tier's own systems — which is exactly the problem [[voldemort]]'s consistent hashing and admin-service rebalancing, and [[espresso]]'s partition-aware routing, exist to solve.

*See also: [[voldemort]] · [[databus]] · [[espresso]] · [[linkedin-data-infrastructure]]*
