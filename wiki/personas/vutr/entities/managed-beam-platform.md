---
persona: vutr
kind: entity
sources:
- raw/linkedin-data-infrastructure/4-trillion-events-daily-at-linkedin.md
last_updated: '2026-07-15'
qc: passed
slug: managed-beam-platform
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

After some successful pilots of [[apache-beam]], internal demand for Beam pipeline development grew enough at LinkedIn that the company built Managed Beam — a platform designed to streamline and automate the internal process of developing, deploying, and running Beam pipelines, rather than leaving every team to wire up the SDK by hand.

Managed Beam has four distinguishing pieces. First, the Beam SDK itself lets engineers package reusable custom logic as standard PTransforms, which become building blocks for other pipelines. Second, a control plane provides a deployment UI, an operational dashboard, administrative tools, and automated pipeline lifecycle management, so pipeline operators don't have to build their own tooling per team. Third, to keep the platform's own runner code independent from user-defined logic, Managed Beam packages the runner and the user-defined functions (UDFs) as two separate JAR files, executed inside a Samza container as two distinct processes that communicate over gRPC — that separation is what lets LinkedIn roll out framework upgrades to the runner without any risk of breaking a team's own pipeline logic. Fourth, an auto-sizing controller tool consumes diagnostic information that Beam pipelines emit as Kafka topics; that diagnostic data is itself processed by dedicated Beam pipelines and written into Apache Pinot, which powers Managed Beam's own operational and analytics dashboards. The control plane then scales LinkedIn's streaming applications and clusters based on the signal the auto-sizing controller produces.

The clearest measure of what the platform buys is LinkedIn's real-time ML feature generation use case. Before Managed Beam, the offline ML feature pipeline that core functionality like job recommendations and search feeds depends on was delayed 24 to 48 hours after a member's action. LinkedIn built a hosted feature-generation platform on top of Managed Beam: engineers define features and deploy them through Managed Beam; a streaming Beam pipeline pre-processes Kafka events in real time to generate the features and writes them to a feature store; a second Beam pipeline reads from that feature store, processes it, and routes the result into the recommendation system. The platform's abstraction over deployment and operational complexity is what took that 24-48 hour lag down to a few seconds.

*See also: [[apache-beam]] · [[unified-batch-stream-pipelines-via-beam]] · [[linkedin-data-infrastructure]]*
