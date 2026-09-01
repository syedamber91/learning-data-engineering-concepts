---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
topic: Graph-Like Data Models
type: subtopic
tags: [ddia2, property-graph, neo4j, vertices, edges, hypergraph]
sources:
  - raw/ch03.md
---
# Property Graphs
> Two tables — vertices and edges — with a JSON blob of properties on each, and an index on both ends of every edge. That is the whole model, and it is remarkably flexible.

## The Idea
In the **property graph** (or labeled property graph) model, each **vertex** has a unique identifier, a **label** (string) describing the type of object it represents, a set of outgoing edges, a set of incoming edges, and a collection of **properties** (key-value pairs). Each **edge** has a unique identifier, the vertex it starts at (the **tail vertex**), the vertex it ends at (the **head vertex**), a label describing the kind of relationship, and its own collection of properties.

## How It Works
You can think of a graph store as two relational tables:

```sql
CREATE TABLE vertices (
  vertex_id integer PRIMARY KEY,
  label     text,
  properties jsonb
);
CREATE TABLE edges (
  edge_id     integer PRIMARY KEY,
  tail_vertex integer REFERENCES vertices (vertex_id),
  head_vertex integer REFERENCES vertices (vertex_id),
  label       text,
  properties  jsonb
);
CREATE INDEX edges_tails ON edges (tail_vertex);
CREATE INDEX edges_heads ON edges (head_vertex);
```

Three consequences matter:
- **Any vertex can have an edge to any other vertex.** There is no schema restricting which kinds of thing may be associated.
- Given any vertex you can efficiently find both its incoming and outgoing edges, and therefore **traverse the graph forward and backward** — which is exactly why there are indexes on both `tail_vertex` and `head_vertex`.
- Using different labels for different kinds of vertex and relationship lets you store several kinds of information in a single graph while keeping a clean data model.

The edges table is the many-to-many associative/join table, **generalised to allow many types of relationship in the same table**. There may also be indexes on labels and properties, so vertices or edges with certain properties can be found efficiently.

## Trade-offs & Pitfalls
- **An edge can associate only two vertices.** A relational join table can represent three-way or higher-degree relationships with multiple foreign keys on one row. In a graph you must either create an additional vertex per join-table row with edges to and from it, or use a **hypergraph**.
- The flexibility is the selling point: the running example expresses things awkward in a traditional relational schema — different regional structures in different countries (France has départements and régions, the US has counties and states), historical quirks such as a country within a country, and **varying granularity of data** (Lucy's residence given as a city, her birthplace only as a state).

## Examples & Systems
Neo4j, Memgraph, KùzuDB as property graph databases; Amazon Neptune supporting both property graphs and triples; PostgreSQL `jsonb` as the illustration of property storage.

## Since the 1st Edition
The model description and the two-table SQL illustration are carried over from the 1st edition's [[Property Graphs]] largely intact. **New:** the hypergraph/higher-degree-relationship limitation stated explicitly, and the updated engine list.

## Related
- up: [[Graph-Like Data Models (2e)]] · chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[The Cypher Query Language (2e)]] — how you actually query this
- [[Triple Stores and SPARQL (2e)]] — the same expressive power, different vocabulary
- 1st edition: [[Property Graphs]] — the same subtopic
