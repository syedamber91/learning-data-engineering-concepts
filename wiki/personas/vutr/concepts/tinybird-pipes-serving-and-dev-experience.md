---
persona: vutr
kind: concept
sources:
- raw/clickhouse-internals/clickhouse-real-time-insight-in-15.md
last_updated: '2026-07-15'
qc: passed
slug: tinybird-pipes-serving-and-dev-experience
topics:
- clickhouse-internals
---

In Tinybird, a **pipe** is the abstraction for transforming, filtering, joining, or aggregating data — Vu describes it as a data pipeline that can be broken into smaller call **nodes**, where each node is a SQL query and nodes combine to form a complete pipeline. A pipe can end in one of two serving directions: a **sink**, which exports the pipe's output to Kafka or object storage and is fully managed by Tinybird, or an **endpoint**, a pipe type that exposes an API for external applications — accepting caller-supplied parameters for filtering, sorting, pagination, or column selection, the same way a hand-built API endpoint would. Vu frames the endpoint as solving a specific, often-underestimated cost: in a traditional stack, exposing an analytical metric means building pipelines into a warehouse *and* a backend server that queries it and meets its own latency/concurrency requirements — Tinybird's endpoint pipes remove the need to build that backend server at all. Connections, sources, pipes, endpoints, and other Tinybird objects are defined via a custom domain-specific language in files; a TypeScript SDK is also available for defining the same objects in TypeScript.

The **developer toolkit** covers the whole project lifecycle: the **Tinybird CLI** (which can run in an AI-powered mode) manages it end to end; **Tinybird Local** is a Docker container for testing a project locally; **Tinybird Cloud** is the web interface managing the deployed project. The intended flow: initialize a git repo for version control, use the CLI to start Tinybird Local (including a local ClickHouse instance) and scaffold the project structure (connections/, datasources/, pipes/ folders plus CI/CD templates), define connections/sources and build pipes to develop the application, test by deploying to Tinybird Local and running the test suite via the CLI, then deploy to Tinybird Cloud through a CI/CD pipeline once ready.

Vu's own demo walks this exact path concretely: sign up for the free tier, install the CLI (`curl https://tinybird.co | sh`), run `tb login`, `tb local start` (spins up the Docker container including ClickHouse), and `tb create` to scaffold the project. Separately he provisions a free-tier Aiven Kafka service with SASL authentication, creates a topic, and streams a handful of JSON records to it via `kafka-python`. Back in Tinybird, `tb connection create kafka` creates a `.connection` file, `tb datasource create --kafka` creates a `.datasource` file (Tinybird infers the schema from the messages already on the topic, and shows the MergeTree storage engine and connection name it picked), and `tb sql "select * from <source>"` previews the ingested data before `tb deploy` pushes it to Tinybird Local. He then writes a `kafka_expose.pipe` file with a single `NODE` that aggregates `click_count` per `user_id`, filtered by a `country` query parameter (defaulting to `'US'`) via `TYPE ENDPOINT` and a `TOKEN ... READ` declaration, deploys it, retrieves a caller token with `tb endpoint token kafka_expose`, and calls the resulting URL (`http://localhost:7182/v0/pipes/<endpoint>.<format>?param=value`) both via Postman and via a small Python/Pandas snippet. The final step, `tb --cloud deploy`, pushes the same project to Tinybird Cloud.

*See also: [[tinybird]] · [[tinybird-ingestion-and-scaling]]*
