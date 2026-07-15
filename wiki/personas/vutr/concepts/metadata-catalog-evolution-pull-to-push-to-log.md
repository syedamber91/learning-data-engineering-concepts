---
persona: vutr
kind: concept
sources:
- raw/linkedin-data-infrastructure/datahub-the-metadata-platform-developed.md
last_updated: '2026-07-15'
qc: passed
slug: metadata-catalog-evolution-pull-to-push-to-log
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

LinkedIn's data catalog went through three architectural generations before arriving at [[datahub]], and each generation is a direct response to a specific failure of the one before it — pull, then push, then log.

**Generation 1** was a classic monolith: a frontend (e.g. a Flask app) backed by a database for lookups (MySQL/Postgres) and a search index (Elasticsearch), later extended with a graph index (Neo4j) for lineage queries. LinkedIn open-sourced this generation in 2016 as WhereHows. A single scheduled crawler process (e.g. once a day) pulled metadata from sources — database catalogs, the Hive catalog, the Kafka schema registry — transformed it into the target metadata model inline in the ingestion job, and wrote it into the database, occasionally spinning up Spark jobs when the transformation needed more compute. Its virtue was simplicity: few components, and a single team could own the whole path from source access to serving. Its cost was staleness — pulled-at-intervals metadata is never quite fresh — plus an operational tax: the crawler runs in a different environment from the source it's crawling, so a central team has to manage credentials and network access, and every crawl schedule and batch size is itself a decision that affects the source system's stability.

**Generation 2** split the monolith into a metadata service in front of the storage database, exposing a push API: producers of metadata could now push instead of waiting to be crawled, and any program needing metadata could call the same API. Underneath, everything still landed in one metadata store (relational or key-value). This established a real contract — a schema-defined push interface — between producers and the central metadata team, and enabled genuinely programmatic use of the catalog. But it had no built-in way to ingest metadata *changes* from external systems, which made rebuilding the search or graph index from scratch unreliable when something went wrong, and it offered no subscription mechanism: anything wanting to react to a metadata change (a data trigger, an access-control abuse check) was forced into polling, full scans, or waiting on a scheduled ETL of a database snapshot. The central team was still a bottleneck for the metadata model, the service, and the store.

**Generation 3** is DataHub, and its founding insight is that a centralized store — however it's accessed — cannot keep pace with an enterprise's demand for metadata. Two changes follow from that insight. First, metadata becomes free-flowing, event-based, and subscribable: producers push to a stream-based API or perform CRUD against the catalog's service API, every mutation generates an entry in a metadata changelog, and that log is materialized into whichever downstream store needs it — a search index, a data lake, an OLAP system. Because the log, not any one downstream store, is now the source of truth, a corrupted or lost index can simply be recreated by replaying it. Second, the metadata model itself becomes extensible and strongly typed, so a team can add a domain-specific extension to the global metadata model without waiting on the central team to bless it. The payoff was integration (clients can tap the changelog for ingestion and change-tracking, do low-latency lookups, full-text search, graph queries, or full analytical scans, all from the same underlying data) and trust — LinkedIn reports that moving from WhereHows (Gen 2) to DataHub (Gen 3) tremendously improved internal trust in the catalog's freshness, which is what let the system become the enterprise's actual center of metadata. The cost is admitted plainly: this generation is more complex than the two before it.

*See also: [[datahub]] · [[linkedin-data-infrastructure]]*
