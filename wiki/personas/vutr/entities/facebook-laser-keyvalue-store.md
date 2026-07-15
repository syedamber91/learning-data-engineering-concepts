---
persona: vutr
kind: entity
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/how-did-facebook-design-their-real.md
last_updated: '2026-07-15'
qc: passed
slug: facebook-laser-keyvalue-store
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Laser is Facebook's high-throughput, low-latency key-value storage service, built on RocksDB, and it can read from either real-time sources (Scribe categories) or offline sources (Hive tables) — making it the serving layer that sits between Facebook's stream processors and its products. The notes describe two common use cases: serving the output stream of a Puma or Stylus application to Facebook's products, and making the results of complex Hive queries or Scribe streams available for consumption by Puma or Stylus applications. Operationally, Laser is deployed as a managed service with a UI: a user picks the desired configuration and the UI returns a single command to deploy the app and another to delete it, in contrast to Stylus apps, which are owned and operated directly by the teams that write them.

*See also: [[facebook-stream-processors-puma-swift-stylus]] · [[persistent-message-bus-data-transfer]]*
