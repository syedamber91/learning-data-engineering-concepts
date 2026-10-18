---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
type: topic
tags: [ddia2, graph, vertices, edges, adjacency-list, knowledge-graph]
sources:
  - raw/ch03.md
---
# Graph-Like Data Models
The type of relationship in your data is the important distinguishing feature across data models. If your application has mostly one-to-many relationships — tree-structured data with few other relationships between records — the document model is appropriate. But **what if many-to-many relationships are very common?** The relational model handles simple cases, but as connections become more complex it becomes more natural to model the data as a graph.

A graph consists of two kinds of object: **vertices** (also called nodes or entities) and **edges** (also called relationships or arcs). Typical examples:
- **Social graphs** — vertices are people, edges indicate who knows whom.
- **The web graph** — vertices are web pages, edges are HTML links.
- **Road or rail networks** — vertices are junctions, edges are the roads or railway lines between them.

Well-known algorithms operate on these: map navigation apps search for the shortest path between two points in a road network, and **PageRank** runs on the web graph to determine a page's popularity and hence its ranking in search results.

## Subtopics
- [[Property Graphs (2e)]] — labeled vertices and edges, each carrying properties.
- [[The Cypher Query Language (2e)]] — declarative pattern matching over property graphs.
- [[Graph Queries in SQL (2e)]] — the same thing with recursive CTEs, at four times the length.
- [[Triple Stores and SPARQL (2e)]] — subject-predicate-object, RDF, and the Semantic Web's useful residue.
- [[Datalog - Recursive Relational Queries (2e)]] — deriving virtual tables rule by rule.
- [[GraphQL (2e)]] — restrictive by design, because its queries come from untrusted clients.

## Key Takeaways
- **Representation choice matters.** In the **adjacency list** model, each vertex stores the IDs of its neighbours one edge away. In an **adjacency matrix**, a two-dimensional array has a row and column per vertex, with 0 for no edge and 1 for an edge. Adjacency lists are good for graph traversals; matrices are good for machine learning.
- **Graphs are not limited to homogeneous data.** An equally powerful use is providing a consistent way to store completely different types of object in one database. Facebook maintains a single graph whose vertices are people, locations, events, check-ins, and comments, and whose edges say who is friends with whom, which check-in happened where, who commented on which post, who attended which event. Search engines use **knowledge graphs** to record facts about entities that often occur in queries — organisations, people, places — obtained by crawling and analysing website text, with some sites such as Wikidata publishing structured graph data directly.
- The chapter covers two closely related models: the **property graph** model (Neo4j, Memgraph, KùzuDB, and others) and the **triple store** model (Datomic, AllegroGraph, Blazegraph, and others). They are fairly similar in expressive power, and some graph databases such as Amazon Neptune support both.
- **Graphs are good for evolvability.** As you add features, a graph extends easily to accommodate changes in the application's data structures — the book's illustration is adding food allergies as allergen vertices with person→allergen edges, then linking allergens to foods containing them, so you can query what is safe for each person to eat.
- The running example throughout is a small genealogical/social graph: Lucy from Idaho and Alain from Saint-Lô, France, married and living in London, with each person and each location a vertex.

## Since the 1st Edition
The 1st edition's [[Graph-Like Data Models]] used the same Lucy-and-Alain example and covered property graphs, Cypher, SQL recursive CTEs, triple stores, SPARQL, and Datalog. **New in the 2nd edition:** adjacency list versus adjacency matrix as a representation choice (and its ML connection), knowledge graphs and Wikidata, [[GraphQL (2e)]] as a sixth query language, and an updated system roster — Memgraph, KùzuDB, Amazon Neptune, Apache AGE. The 1st edition's [[The Foundation - Datalog]] framing is replaced by a fuller [[Datalog - Recursive Relational Queries (2e)]].

## Related
- chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[Many-to-One and Many-to-Many Relationships (2e)]] — the relational and document handling of the same shapes
- [[DataFrames, Matrices, and Arrays (2e)]] — where adjacency matrices lead
- 1st edition: [[Graph-Like Data Models]] — the same topic
