---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
topic: Graph-Like Data Models
type: subtopic
tags: [ddia, graphs, property-graph, neo4j]
sources:
  - raw/ch02.md
---
# Property Graphs
> Vertices and labeled, property-carrying edges with no connection restrictions — maximum flexibility for highly interconnected, evolving data.

## The Idea
When many-to-many relationships dominate, graphs become the natural model. A graph has *vertices* (nodes/entities) and *edges* (relationships/arcs). Classic homogeneous examples: social graphs (people ↔ acquaintance), the web graph (pages ↔ links, enabling PageRank), and road/rail networks (junctions ↔ routes, enabling shortest-path navigation). But graphs are equally powerful for *heterogeneous* data in one store: Facebook's single graph mixes people, places, events, checkins, and comments as vertices, with edge types for friendship, attendance, commenting, and checkin location. The chapter's running example is a genealogy-style graph of two people — one born in Idaho (USA), one born in Beaune (France) — married and living in London.

## How It Works
In the property graph model (Neo4j, Titan, InfiniteGraph), each **vertex** carries a unique ID, sets of outgoing and incoming edges, and a key-value property collection. Each **edge** carries a unique ID, a *tail* vertex (where it starts), a *head* vertex (where it ends), a *label* naming the relationship kind, and its own property collection.

You could model this relationally with two tables — one for vertices, one for edges (with a JSON column for properties, foreign keys for head/tail, and indexes on both `tail_vertex` and `head_vertex`). Three properties define the model's power:

1. **No connection schema** — any vertex may connect to any other; nothing restricts which kinds of things can relate.
2. **Efficient bidirectional traversal** — given a vertex, both incoming and outgoing edges are cheap to find (hence indexing both columns), so paths can be walked forward and backward.
3. **Multiple relationship kinds via labels** — one graph cleanly stores many types of information.

## Trade-offs & Pitfalls
The flexibility handles cases that strain fixed relational schemas: regional structures that differ by country (French *départements/régions* vs US counties/states), historical oddities like a country inside a country, and mixed granularity (residence recorded as a city, birthplace only as a state). Graphs also excel at *evolvability* — new features extend the graph without restructuring: e.g., add allergen vertices, person→allergen "allergic to" edges, and food→allergen "contains" edges, then query what each person can safely eat. The flip side: for data that is mostly tree-shaped or unconnected, the document model remains simpler.

## Examples & Systems
Neo4j, Titan, InfiniteGraph (property graph); contrast with the triple-store family (Datomic, AllegroGraph) in [[Triple-Stores and SPARQL]]. Declarative graph queries: Cypher, SPARQL, Datalog; imperative alternative: Gremlin; large-scale processing: Pregel (see [[Graphs and Iterative Processing]]).

## Related
- up: [[Graph-Like Data Models]] · chapter: [[Ch 02 - Data Models and Query Languages]]
- [[The Cypher Query Language]] — the query language built for this model
- [[Many-to-One and Many-to-Many Relationships]] — the problem graphs solve natively
- [[Graph Queries in SQL]] — emulating this model relationally
