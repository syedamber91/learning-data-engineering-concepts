---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
type: chapter-moc
tags: [ddia2, data-models, relational, document, graph, event-sourcing, dataframes, moc]
sources:
  - raw/ch03.md
---
# Ch 03 – Data Models and Query Languages
Data models are perhaps the most important part of developing software, because of their profound effect not only on how software is written but on **how we think about the problem we are solving**. Most applications layer one data model on another, and for each layer the key question is how it is represented in terms of the next layer down: the developer models the real world as objects and APIs; those structures are expressed in a general-purpose data model (JSON or XML documents, relational tables, graph vertices and edges) — the subject of this chapter; database engineers represent that in bytes in memory, on disk, or on a network — the subject of Chapter 4; and hardware engineers represent bytes as electrical currents, pulses of light, and magnetic fields. Each layer hides the complexity below it behind a clean data model, which is what lets database vendors and application developers work together effectively.

## Map
- [[Relational Versus Document Models (2e)]] — the long argument between tables and JSON, and why both sides won
  - [[The Object-Relational Mismatch (2e)]] — impedance mismatch, ORMs, and the N+1 query problem
  - [[Normalization, Denormalization, and Joins (2e)]] — IDs versus text, and the read/write trade underneath
  - [[Many-to-One and Many-to-Many Relationships (2e)]] — where the document model runs out of road
  - [[Stars and Snowflakes - Schemas for Analytics (2e)]] — fact tables, dimensions, and one big table
  - [[When to Use Which Model (2e)]] — schema-on-read versus schema-on-write, locality, and convergence
- [[Graph-Like Data Models (2e)]] — when anything might relate to everything
  - [[Property Graphs (2e)]] — labeled vertices and edges with properties on both
  - [[The Cypher Query Language (2e)]] — pattern matching with variable-length traversal
  - [[Graph Queries in SQL (2e)]] — the same query in 31 lines instead of 4
  - [[Triple Stores and SPARQL (2e)]] — subject-predicate-object, RDF, and the Semantic Web's legacy
  - [[Datalog - Recursive Relational Queries (2e)]] — building queries rule by rule
  - [[GraphQL (2e)]] — deliberately restrictive, because the queries come from untrusted clients
- [[Event Sourcing and CQRS (2e)]] — write an immutable log, derive every read model from it
- [[DataFrames, Matrices, and Arrays (2e)]] — the analytics and ML models that rarely appear in OLTP

## Chapter Summary
The **relational model**, more than half a century old, remains central — especially in data warehousing and business analytics, where star and snowflake schemas and SQL are ubiquitous. But alternatives took hold in other domains. The **document model** targets self-contained JSON documents where relationships between documents are rare; its advantages are schema flexibility, locality, and closeness to the application's object model, and its weakness is many-to-one and many-to-many relationships. **Graph models** go the opposite way: anything is potentially related to everything, and queries may need to traverse multiple hops — a need met by recursive queries in Cypher, SPARQL, or Datalog. **DataFrames** generalise relational data to very large numbers of columns and bridge databases to the multidimensional arrays underlying machine learning, statistics, and scientific computing.

One model can often be emulated in another — graph data in a relational database, for instance — but the result can be awkward, as the 31-line SQL version of a 4-line Cypher query demonstrates. Specialist databases exist for each model, but there is also a strong trend of **convergence**: relational databases added JSON columns and operators, document databases added joins and secondary indexes, and SQL support for graph data is gradually improving. The chapter's practical conclusion is that relational–document hybrids are a powerful combination.

**Event sourcing** represents data as an append-only log of immutable events, with read-optimised **materialized views** derived from it via CQRS — a model that suits complex business domains, communicates intent, makes views reproducible, reduces irreversibility, and doubles as an audit log, at the cost of care around external information, GDPR deletion, and side effects during reprocessing.

## Since the 1st Edition
The 1st edition's Chapter 2 covered relational versus document, graph-like models, and query languages. Retained and updated: the object-relational mismatch, normalization, many-to-many, property graphs, Cypher, SQL recursive CTEs, triple stores, SPARQL, and Datalog. **Genuinely new here:** [[Event Sourcing and CQRS (2e)]] and [[DataFrames, Matrices, and Arrays (2e)]] as full topics, [[GraphQL (2e)]] as a query language, and [[Stars and Snowflakes - Schemas for Analytics (2e)]] relocated from the 1st edition's storage chapter into the data-modelling chapter where it belongs. **Restructured:** the 1st edition's separate [[Query Languages for Data]] topic is gone — its declarative-query material is now a terminology box, its MapReduce-querying subtopic moved to the batch chapter, and its remaining content is distributed among the query-language subtopics. The 1st edition's [[The Birth of NoSQL]] and [[Relational Versus Document Databases Today]] are absorbed into [[Relational Versus Document Models (2e)]] and [[When to Use Which Model (2e)]], reflecting that the NoSQL argument has been settled by convergence rather than victory.

## Related
- home: [[Home (2e)]] · previous: [[Ch 02 - Defining Nonfunctional Requirements (2e)]] · next: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Ch 04 - Storage and Retrieval (2e)]] — how these models are represented as bytes
- [[Ch 05 - Encoding and Evolution (2e)]] — schemas and how they change over time
- 1st edition: [[Ch 02 - Data Models and Query Languages]] — the chapter this one rewrites
