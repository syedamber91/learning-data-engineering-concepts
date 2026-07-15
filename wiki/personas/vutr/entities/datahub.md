---
persona: vutr
kind: entity
sources:
- raw/linkedin-data-infrastructure/datahub-the-metadata-platform-developed.md
last_updated: '2026-07-15'
qc: passed
slug: datahub
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

DataHub is LinkedIn's metadata platform — its data catalog — open-sourced in 2019 as the third generation of an internal lineage that began with the 2016 open-source release of WhereHows (see [[metadata-catalog-evolution-pull-to-push-to-log]] for the full three-generation arc that led here). Its own documentation names three architectural highlights. It takes a schema-first approach to metadata modeling: the metadata model is described in a serialization-agnostic language, and DataHub exposes both REST and GraphQL APIs over it plus an Avro-based API over Kafka for communicating and subscribing to metadata changes. It is a stream-based, real-time metadata management platform: changes propagate through the system within seconds, and users can subscribe to them to build their own reactive, metadata-driven systems. And it supports federated metadata serving: DataHub runs a single central metadata service, but different teams can operate their own federated metadata services that communicate with the central search and graph index via Kafka — enabling global search and discovery while letting ownership of metadata stay decentralized, which is what makes the architecture a natural fit for companies building a data mesh.

DataHub's metadata is modeled with four abstractions. **Entities** represent a class of metadata asset — a Dataset, a Data Pipeline — and are the primary nodes of the metadata graph; each entity instance is identified by a unique urn. **Aspects** define a set of attributes on an entity instance and are the atomic writing unit — an instance's aspects can be updated independently of each other, and an aspect (like ownership or a tag) can be shared across multiple entity instances. A **relationship** is a named edge between two entities. **Identifiers** (keys and urns) are a special kind of aspect: a key holds the fields that uniquely identify an instance, and that key serializes into an urn — the stringified form used for primary-key lookup.

Structurally, DataHub is four components. The **Metadata Store** stores the entities and aspects that make up the metadata graph and exposes an API for ingesting metadata, fetching by primary key, searching entities, or fetching relationships; it's built as a Spring Java service backed by MySQL, Elasticsearch, and Kafka for storage and indexing. The **Ingestion Framework** is a modular, extensible Python library that extracts metadata from source systems — Snowflake, BigQuery, Kafka among them — transforms it into DataHub's metadata model, and writes it in either via Kafka or directly against the Metadata Store's REST APIs. The **GraphQL API** gives a strongly typed, entity-oriented interface for interacting with entities, including adding and removing tags, owners, and links. Finally, a React-based **User Interface** lets users discover, govern, and debug entities directly.

*See also: [[metadata-catalog-evolution-pull-to-push-to-log]] · [[linkedin-data-infrastructure]]*
