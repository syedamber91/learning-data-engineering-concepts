---
title: "DataHub: The Metadata Platform Developed at LinkedIn"
channel: vutr
author: "Vu Trinh"
published: 2024-11-05
url: https://vutr.substack.com/p/datahub-the-metadata-platform-developed
paid: false
topics: ["Apache Kafka", "Apache Spark", "Snowflake", "BigQuery", "Data Lake", "ETL"]
tags: [metadata, https, datahub, auto, image, catalog]
---

# DataHub: The Metadata Platform Developed at LinkedIn

*How did LinkedIn manage the data catalog at scale?*

> Source: [Open post](https://vutr.substack.com/p/datahub-the-metadata-platform-developed)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]] · [[data-lake|Data Lake]] · [[etl|ETL]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=151061734)

[![](https://substackcdn.com/image/fetch/$s_!FvYR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e85c635-3395-4331-aaae-d37fa2c8ae2e_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!FvYR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e85c635-3395-4331-aaae-d37fa2c8ae2e_2000x1429.png)

Image created by the author.

---

## Intro

What is the data catalog? I Google search and found this [from IBM](https://www.ibm.com/topics/data-catalog):

> *“A data catalog is a detailed inventory of all data assets in an organization, designed to help data professionals quickly find the most appropriate data for any analytical or business purpose.”*

If you’ve just been onboarded at a company a few days ago and need to find a dataset but end up asking three colleagues about it, you will know why we need the data catalog ;)

This week, we will learn how LinkedIn built its data catalog solution —DataHub, and later open-sourced in 2019.

First, we will examine LinkedIn's data catalog iterations as they improved and evolved their catalog over three generations, leading to Datahub's development. Then, we will explore DataHub’s architecture and components.

---

## The First Generation

At first, LinkedIn’s data catalog was designed as a classic monolith frontend (e.g., a Flask app) with connectivity to a database for lookups (e.g., MySQL/Postgres) and a search index for serving search queries (e.g., Elasticsearch). Later, the architecture evolved to introduce a graph index for handling graph queries for lineage (e.g., Neo4j).

> *LinkedIn open-source the first version of Datahub called WhereHows in 2016 which also leverage this architecture.*

[![](https://substackcdn.com/image/fetch/$s_!8BEd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9912aa31-7c1d-4703-b6d0-8e90ce6b8664_1400x798.png)](https://substackcdn.com/image/fetch/$s_!8BEd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9912aa31-7c1d-4703-b6d0-8e90ce6b8664_1400x798.png)

Image created by the author.

The system ingests and crawls the metadata from the sources, connects to the database catalog, Hive catalog, or the Kafka schema registry, and writes the metadata into the database. The data is then indexed with a search and graph index.

This crawling is executed as a single process running based on a schedule (e.g., once a day). The raw metadata is often transformed into the desired metadata model. These transformations are embedded directly into the ingestion job.  When they need more computing power to process metadata at scale, LinkedIn will define Spark jobs.

### Pros

* Few components
* Helping a single team that can access metadata sources and build an application to serve it.

### Cons

* The pull approach means the metadata isn’t always fresh; it has to wait to be pulled at set intervals.

* Since the crawler operates in a different environment from the data source, managing configurations falls to a central team, which can lead to challenges like network issues and credential management.
* Crawling-based ingestion often leads to batch and non-incremental workloads. How frequently does the system ping the source? How many records should they pull each time? These decisions impact the data source’s stability and performance.

---

## The Second Generation

The monolith application from the first generation was split into a metadata service in front of the storage database. The service exposes an API that allows the source to push metadata to the system, and other programs that need to consume the metadata can use this API, too. Behind the science, all the metadata is still stored in a single metadata store; it could be a relational database or a key-value store.

[![](https://substackcdn.com/image/fetch/$s_!tZrI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7c6842f-0451-4ea8-951c-d923e7750fca_1330x854.png)](https://substackcdn.com/image/fetch/$s_!tZrI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7c6842f-0451-4ea8-951c-d923e7750fca_1330x854.png)

Image created by the author.

### Pros

* Implementing a push-based, schema-defined interface establishes clear contracts between metadata producers and the central metadata team.
* With a service API, the central team can enable programmatic use cases for metadata.

### Cons

* The lack of built-in support for ingesting metadata changes from external systems makes it harder to recreate the search and graph index reliably when issues arise.
* Additionally, the catalog does not allow subscriptions to the metadata changes. This makes building reactive systems, such as data triggers or access control abuse detection, on top of the data catalog becomes challenging. Other applications are forced to access the metadata through polling or full scans, or they may need to wait for a scheduled ETL of the metadata database to process the snapshot.
* It still depends on a centralized team for too many aspects: managing the metadata model, operating the metadata service, and maintaining the metadata store.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=151061734)

---

## Third Generation

Based on the lessons from two previous generations, the critical insight leading to the third generation is that a centralized-based solution for metadata struggles to keep pace with the enterprise’s demands. To solve this problem, two needs must be met.

* First, the metadata must be free-flowing, event-based, and subscribable in real time. In the third generation, the metadata producer can push to a stream-based API or perform [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operations against the catalog’s service API. The mutations to the metadata will generate the metadata changelog. This metadata log can be materialized into different stores (e.g., search index, data lake, or OLAP system). Now that the log becomes the source of truth for the metadata, in the event of any inconsistency, the user can recreate the graph index or the search index as desired.

[![](https://substackcdn.com/image/fetch/$s_!JovK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbe0a3fc-bfd3-4203-9a3d-cb9a8bda11a7_1604x748.png)](https://substackcdn.com/image/fetch/$s_!JovK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbe0a3fc-bfd3-4203-9a3d-cb9a8bda11a7_1604x748.png)

Image created by the author.

* The second is that the metadata model must support evolution without being blocked by a central team. The third generation enables extensible, strongly typed metadata models and relationships. This modeling allows teams to evolve the global metadata model by adding domain-specific extensions without getting bottlenecked by the central team.

[![diagram-of-an-example-metadata-model-graph](https://substackcdn.com/image/fetch/$s_!qZe8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2716e619-e4f9-4ae2-8976-1bc45cc1e007_800x372.png "diagram-of-an-example-metadata-model-graph")](https://substackcdn.com/image/fetch/$s_!qZe8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2716e619-e4f9-4ae2-8976-1bc45cc1e007_800x372.png)

An example metadata model graph: Types, aspects, relationships. [DataHub: Popular metadata architectures explained](https://www.linkedin.com/blog/engineering/data-management/datahub-popular-metadata-architectures-explained) (2020)

### Pros

* **Integration**: clients can flexibly interact with the metadata database based on their needs. They can tap into a stream-based metadata log for ingestion and change tracking, perform low-latency metadata lookups, conduct full-text searches on metadata attributes, or execute graph queries on metadata relationships. Full scans and analytical capabilities are also supported, which enable various use cases.
* **Trustworthy**: With the introduction of a metadata change log, metadata is now being pushed efficiently and reliably instead of pulled from the source. LinkedIn internal users now always read and take action on the freshest metadata without losing consistency. They found that they improved the trust in the data catalog tremendously when transitioning from Gen 2 (WhereHows) to Gen 3 (Datahub), leading to the system becoming the center of the enterprise.

### Cons

* It is more complex than the two previous generations.

---

## The DataHub architecture

> *After learning the context behind DataHub, let’s explore its architecture*

[![](https://substackcdn.com/image/fetch/$s_!kRJB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16d650ec-4a06-4683-aeac-5e056ebc9e2a_1400x622.png)](https://substackcdn.com/image/fetch/$s_!kRJB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16d650ec-4a06-4683-aeac-5e056ebc9e2a_1400x622.png)

Image created by the author.

From the official documentation, there are three main highlights of DataHub's architecture:

* **Schema-first approach to Metadata Modeling**: The metadata model is described using a [serialization-agnostic language](https://linkedin.github.io/rest.li/pdl_schema). It supports both [REST](https://github.com/datahub-project/datahub/blob/master/metadata-service) and [GraphQL APIs](https://github.com/datahub-project/datahub/blob/master/datahub-web-react/src/graphql). In addition, DataHub supports an [AVRO-based API](https://github.com/datahub-project/datahub/blob/master/metadata-events) over Kafka to communicate metadata changes and subscribe to them.
* **Stream-based Real-time Metadata Management Platform:** DataHub's infrastructure allows metadata changes to be reflected in the platform within seconds. Users can also subscribe to changes in DataHub's metadata, allowing them to build real-time metadata-driven systems.
* **Federated Metadata Serving:** DataHub has a single [metadata service](https://github.com/datahub-project/datahub/blob/master/metadata-service). However, it supports federated metadata services operated by different teams. The federated services communicate with the central search index and graph using Kafka to support global search and discovery while still enabling decoupled ownership of metadata. This kind of architecture is very suitable for companies implementing [data mesh](https://martinfowler.com/articles/data-monolith-to-mesh.html).

---

## The components

### The Metadata Models

DataHub metadata is modeled using the following abstractions:

[![](https://substackcdn.com/image/fetch/$s_!15Zj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F272d75da-081e-426f-b632-7a1982433689_826x739.png)](https://substackcdn.com/image/fetch/$s_!15Zj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F272d75da-081e-426f-b632-7a1982433689_826x739.png)

An example metadata graph from DataHub official documentation. [Source](https://datahubproject.io/docs/metadata-modeling/metadata-model/)

* **Entities** represent a specific class of metadata asset, such as a Dataset or Data Pipeline. Each *instance* of an Entity is identified by a unique identifier called an urn. The entities are the primary nodes in the metadata graph.
* An **Aspect**defines a set of attributes belonging to an entity instance. In DataHub, aspects are the atomic writing units; the instance’s multiple aspects can be updated independently. In addition, aspects can be shared across entity instances. Examples of aspects can be listed, such as the instance owners or the instance tag.
* A **relationship** defines a named edge between 2 entities.
* **Identifiers (Keys & Urns)**: A key is a special aspect containing the fields that uniquely identify an instance. The key can be serialized into *Urns*, representing a stringified form of the fields used for primary-key lookup.

### The Metadata Store

The store is responsible for storing the DataHub Entities and Aspects comprising the Metadata Graph. These stores also expose an API for ingesting metadata, fetching metadata by primary key, searching entities, or fetching relationships between entities. The store consists of

* A Spring Java Service hosts a set of API endpoints.
* MySQL, Elasticsearch, and Kafka are used for storage and indexing.

### Ingestion Framework

This component is a modular, extensible Python library for extracting metadata from source systems such as Snowflake, BigQuery, or Kafka. The metadata is transformed into DataHub's metadata model and written into DataHub via either Kafka or directly using the Metadata Store Rest APIs.

### GraphQL API

The [GraphQL](https://graphql.org/) API provides a strongly typed, entity-oriented API that makes interacting with entities simple. It includes APIs for adding and removing tags, owners, links, and more.

### User Interface

DataHub has a React UI, including features to discover, govern, and debug the entities.

---

## Outro

Thank you for reading this far.

In this article, we’ve explored LinkedIn’s journey in developing and refining its internal data catalog solution, which led to the creation of DataHub. We also examined DataHub's architecture and its components.

See you on my next blog ;)

---

## **References**

*[1] Shirshanka Das, [DataHub: Popular metadata architectures explained](https://www.linkedin.com/blog/engineering/data-management/datahub-popular-metadata-architectures-explained) (2020)*

*[2] [DataHub Official Documentation](https://datahubproject.io/docs/features)*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/datahub-the-metadata-platform-developed/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
