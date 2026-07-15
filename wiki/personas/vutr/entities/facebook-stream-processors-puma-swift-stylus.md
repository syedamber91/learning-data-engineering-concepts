---
persona: vutr
kind: entity
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/how-did-facebook-design-their-real.md
last_updated: '2026-07-15'
qc: passed
slug: facebook-stream-processors-puma-swift-stylus
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Puma, Swift, and Stylus are the three stream processing systems the notes describe from Facebook's 2018 real-time processing paper, and each one embodies a different point on the "language paradigm" design axis — declarative, scripting, or procedural — with a corresponding ease-of-development-versus-performance trade-off.

Puma is written in an SQL-like language with Java UDFs, letting users develop and test an application within an hour; it's designed for long-term deployments running for months or years, stores state in a shared HBase cluster, and serves two purposes at Facebook: providing pre-computed results for simple aggregation queries, and filtering/processing Scribe streams for downstream consumers. Swift is Facebook's checkpointed stream reader, mostly written in Python, aimed at prototyping and low-throughput tasks; it reads a Scribe stream with checkpoints set every N strings or B bytes, so an app that crashes restarts from its last checkpoint, guaranteeing all data is read at least once. Stylus is a low-level C++ stream processing framework offering the most flexibility and highest throughput of the three, at the cost of a development cycle the notes describe as often taking a few days; its core component takes input from one Scribe stream and outputs to another Scribe stream or a data store, and application developers must explicitly identify event-time data in exchange for Stylus's built-in ability to estimate an event-time watermark within a given confidence interval.

The notes describe a real usage pattern across the three: applications commonly start in Puma or Swift for speed of iteration, then migrate to Stylus once they need more control or higher throughput — letting teams prove value cheaply before investing in a heavier system.

*See also: [[persistent-message-bus-data-transfer]] · [[state-and-output-processing-semantics]] · [[stream-state-saving-mechanisms]] · [[facebook-laser-keyvalue-store]] · [[scribe]] · [[scuba]]*
