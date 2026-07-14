---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
type: chapter-moc
tags: [ddia, data-models, query-languages, moc]
sources:
  - raw/ch02.md
---
# Ch 02 – Data Models and Query Languages
Data models shape not only how software is written but how we think about the problem — every application stacks models in layers, each hiding the complexity beneath it. This chapter surveys the general-purpose storage-and-query layer: the relational model that has dominated since the 1970s, the document model revived by NoSQL for tree-shaped, self-contained data, and graph models for data where everything connects to everything. Alongside the models come their query languages — and a running argument that *declarative* querying (SQL, CSS, Cypher, SPARQL, Datalog) beats imperative code because it hands execution strategy to an optimizer, survives internal reorganization, and parallelizes. [[Denormalization]], [[MapReduce]], and [[Schema Evolution]] all get their first appearance here before later chapters take them up in depth.

## Map
- [[Relational Model Versus Document Model]] — the decades-long tables-vs-documents contest and its pragmatic settlement
  - [[The Birth of NoSQL]] — the forces (scale, open source, specialized queries, schema frustration) behind the nonrelational wave
  - [[The Object-Relational Mismatch]] — the impedance mismatch between objects and tables; JSON's locality appeal
  - [[Many-to-One and Many-to-Many Relationships]] — IDs vs duplicated strings, normalization, and data growing interconnected
  - [[Are Document Databases Repeating History]] — IMS's hierarchical model, CODASYL access paths, and the relational optimizer's victory
  - [[Relational Versus Document Databases Today]] — schema-on-read vs schema-on-write, locality, and convergence toward hybrids
- [[Query Languages for Data]] — declarative "what" versus imperative "how", and why the limitation is a superpower
  - [[Declarative Queries on the Web]] — CSS/XSL versus DOM JavaScript: the same argument outside databases
  - [[MapReduce Querying]] — pure map/reduce functions in MongoDB, and the declarative aggregation pipeline that followed
- [[Graph-Like Data Models]] — vertices and edges for highly interconnected, heterogeneous data
  - [[Property Graphs]] — vertices, labeled edges, and key-value properties; two relational tables underneath
  - [[The Cypher Query Language]] — Neo4j's declarative pattern matching with variable-length traversal
  - [[Graph Queries in SQL]] — recursive CTEs: 4 lines of Cypher become ~29 lines of SQL
  - [[Triple-Stores and SPARQL]] — subject–predicate–object statements, RDF/Turtle, and the semantic web detour
  - [[The Foundation - Datalog]] — composable recursive rules, the academic root of graph querying

## Chapter Summary
Data began as one big tree (the hierarchical model), which handled one-to-many well but choked on many-to-many relationships — the gap the relational model was invented to fill. When some applications later strained against relations too, NoSQL split in two directions: document databases for self-contained records with rare cross-document relationships, and graph databases for the opposite extreme where anything may connect to anything. All three models thrive today in their own domains; each can emulate the others, but awkwardly — which is exactly why different systems exist for different purposes rather than one universal database. Document and graph stores share a reluctance to enforce schemas, easing adaptation to change, though the structure assumption merely moves: explicit and enforced on write, or implicit and interpreted on read. Each model brings its own query language — SQL, MapReduce, MongoDB's aggregation pipeline, Cypher, SPARQL, Datalog, with CSS and XSL/XPath as instructive non-database parallels — and the chapter closes by noting models it couldn't cover, from genome sequence-similarity search (GenBank) to the Large Hadron Collider's hundreds of petabytes to full-text search. Chapter 3 turns to how these models are actually implemented by storage engines.

## Related
- part: [[Part I - Foundations of Data Systems]] · home: [[Home]]
- previous: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]] — the qualities any data system must deliver, whatever its model
- next: [[Ch 03 - Storage and Retrieval]] — implementing these models: how storage engines lay data on disk
