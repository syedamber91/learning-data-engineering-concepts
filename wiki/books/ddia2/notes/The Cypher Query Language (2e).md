---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
topic: Graph-Like Data Models
type: subtopic
tags: [ddia2, cypher, opencypher, gql, pattern-matching, neo4j]
sources:
  - raw/ch03.md
---
# The Cypher Query Language
> `-[:WITHIN*0..]->` means "follow a WITHIN edge, zero or more times." That one operator is why graph queries are short and SQL graph queries are not.

## The Idea
**Cypher** is a query language for property graphs, originally created for Neo4j and later developed into an open standard as **openCypher**. Besides Neo4j it is supported by Memgraph, KùzuDB, Amazon Neptune, and Apache AGE (with storage in PostgreSQL). It is named after a character in *The Matrix* and has nothing to do with cryptographic ciphers.

## How It Works
**Writing data.** Each vertex is given a symbolic name used only within the query, not stored, and edges are created with arrow notation:

```cypher
CREATE
  (namerica :Location {name:'North America', type:'continent'}),
  (usa      :Location {name:'United States', type:'country'  }),
  (idaho    :Location {name:'Idaho',         type:'state'    }),
  (lucy     :Person   {name:'Lucy'}),
  (idaho) -[:WITHIN ]-> (usa) -[:WITHIN]-> (namerica),
  (lucy)  -[:BORN_IN]-> (idaho)
```

`(idaho) -[:WITHIN]-> (usa)` creates an edge labeled `WITHIN` with `idaho` as tail and `usa` as head.

**Querying.** To find everyone who emigrated from the United States to Europe — vertices with a `BORN_IN` edge to a location within the US and a `LIVES_IN` edge to a location within Europe:

```cypher
MATCH
  (person) -[:BORN_IN] -> () -[:WITHIN*0..]-> (:Location {name:'United States'}),
  (person) -[:LIVES_IN]-> () -[:WITHIN*0..]-> (:Location {name:'Europe'})
RETURN person.name
```

The same arrow notation appears in `MATCH` to find patterns. `(person) -[:BORN_IN]-> ()` matches any two vertices joined by a `BORN_IN` edge, binding the tail to `person` and leaving the head unnamed. `:WITHIN*0..` means **follow a `WITHIN` edge, zero or more times** — like `*` in a regular expression — which is what handles the fact that a `LIVES_IN` edge might point at a street, city, district, region, or state, any number of hops below the country.

## Trade-offs & Pitfalls
- **The query does not specify execution strategy.** The reading above suggests scanning all people and examining each one's birthplace and residence. But equivalently the engine could start from the two `Location` vertices and work backward: with an index on `name`, find the US and Europe vertices efficiently, follow all *incoming* `WITHIN` edges to collect every location inside each, then find people via incoming `BORN_IN` or `LIVES_IN` edges. This freedom is precisely the benefit of a declarative language.
- Standardisation is still settling. The **GQL (Graph Query Language) ISO standard**, based on Cypher, was published in **2024**; it is not widely adopted yet, but the book expresses hope it will bring greater uniformity among graph databases.

## Examples & Systems
Neo4j, Memgraph, KùzuDB, Amazon Neptune, Apache AGE (Cypher over PostgreSQL); openCypher and the 2024 GQL ISO standard.

## Since the 1st Edition
The language, the example queries, and the variable-length-path explanation carry over from the 1st edition's [[The Cypher Query Language]]. **New:** openCypher as an open standard, the expanded list of supporting engines, and — the significant update — the **2024 GQL ISO standard**, which did not exist in 2017.

## Related
- up: [[Graph-Like Data Models (2e)]] · chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[Graph Queries in SQL (2e)]] — the same query, at 31 lines
- [[Property Graphs (2e)]] — the model Cypher queries
- 1st edition: [[The Cypher Query Language]] — the same subtopic
