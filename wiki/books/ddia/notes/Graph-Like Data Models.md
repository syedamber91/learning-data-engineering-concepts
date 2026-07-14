---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
type: topic
tags: [ddia, graph-databases, data-models, query-languages]
sources:
  - raw/ch02.md
---
# Graph-Like Data Models
> When anything can relate to anything, model vertices and edges directly — two data models (property graph, triple-store) and three declarative languages (Cypher, SPARQL, Datalog) make highly connected data natural.

Many-to-many relationships are the fault line between data models: trees suit documents, simple cases suit relations, but as connections multiply, a graph — vertices plus edges — becomes the natural representation. Graphs fit homogeneous data (social networks of people, the web's pages and links, road junctions, powering algorithms like shortest-path routing and PageRank) but equally shine at storing *heterogeneous* objects in one store, as Facebook does with people, places, events, checkins, and comments in a single graph. The chapter's running example — Lucy from Idaho and Alain from Beaune, married and living in London — shows off graph strengths: differing regional hierarchies per country, historical quirks, and mixed granularity, all without schema contortions. Two equivalent models are covered (property graphs in Neo4j-style systems; triples in RDF-style stores) along with declarative query languages for each, plus the humbling demonstration that a 4-line Cypher query balloons to ~29 lines of recursive SQL. Crucially, graph databases are *not* CODASYL reborn: no schema restricts which vertices may connect, any vertex is reachable directly by ID or index rather than only via access paths, vertices and edges are unordered, and high-level declarative languages replace brittle imperative traversal code.

## Subtopics
- [[Property Graphs]] — vertices and edges each carry an ID and key-value properties; edges add tail, head, and a label; representable as two relational tables.
- [[The Cypher Query Language]] — Neo4j's declarative pattern language; arrow notation, variable-length `WITHIN*0..` traversals, optimizer-chosen execution.
- [[Graph Queries in SQL]] — the same emigration query via `WITH RECURSIVE` common table expressions: possible, but painfully verbose because join depth isn't known in advance.
- [[Triple-Stores and SPARQL]] — (subject, predicate, object) statements, Turtle/RDF formats, the semantic web's checkered history, and SPARQL's concise patterns.
- [[The Foundation - Datalog]] — the 1980s academic ancestor: facts as predicate(subject, object) plus composable rules that derive new predicates recursively.

## Key Takeaways
- Choose graphs when many-to-many relationships dominate; document for trees, relational for the middle ground.
- One graph can hold many object types cleanly — edge labels keep distinct relationship kinds separate in a single store.
- Property graphs and triple-stores are essentially the same idea in different vocabulary; Cypher and SPARQL pattern-matching are close cousins (Cypher borrowed from SPARQL).
- Variable-length traversals — "follow this edge zero or more times" — are the operation relational SQL handles worst; line count is a proxy for model fit.
- Graphs beat CODASYL on every count that mattered: no nesting schema, direct/indexed vertex access instead of access paths, no maintained ordering, declarative instead of imperative querying.
- Graphs are good for evolvability — new vertex and edge types extend the model without restructuring what exists.

## Related
- chapter: [[Ch 02 - Data Models and Query Languages]]
- [[Relational Model Versus Document Model]] — the relationship-shape spectrum this model completes
- [[Query Languages for Data]] — the declarative principle all three graph languages inherit
- [[Are Document Databases Repeating History]] — the CODASYL story the network-model comparison answers
- [[Graphs and Iterative Processing]] — Ch 10 processes graphs at Pregel scale
