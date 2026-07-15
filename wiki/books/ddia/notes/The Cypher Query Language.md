---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
topic: Graph-Like Data Models
type: subtopic
tags: [ddia, cypher, neo4j, graph-queries]
sources:
  - raw/ch02.md
---
# The Cypher Query Language
> Cypher expresses graph patterns as ASCII-art arrows and leaves the traversal strategy to the optimizer.

## The Idea
Cypher is the declarative query language created for the Neo4j property-graph database (named for a character in *The Matrix*, not for cryptography). Its signature is arrow notation that draws the graph pattern directly in the query text, making variable-length graph traversals dramatically more concise than the relational equivalent.

## How It Works
**Inserting data:** a `CREATE` statement assigns each vertex a symbolic name and then draws edges between the names. Using my own toy data — cities inside countries:

```cypher
CREATE
  (Kyoto:Location {name:'Kyoto', type:'city'}),
  (Japan:Location {name:'Japan', type:'country'}),
  (Kyoto) -[:WITHIN]-> (Japan)
```

The `(tail) -[:LABEL]-> (head)` arrow creates a labeled edge; here `Kyoto` is the tail vertex and `Japan` the head.

**Querying:** the same arrow notation inside a `MATCH` clause finds patterns instead of creating them. The chapter's flagship query — people who emigrated from the US to Europe — matches vertices that have (a) a birth edge leading, through a chain of zero-or-more containment edges, to the US location vertex, and (b) a residence edge leading likewise to the Europe vertex, then returns each match's name property. The crucial construct is `[:WITHIN*0..]`, meaning "follow a WITHIN edge zero or more times" — the graph analogue of a regex `*`, handling the fact that a residence edge might point at a street, city, region, or state, each nested arbitrarily deep inside larger regions.

Being declarative, the query says nothing about execution order. The engine could scan all people and check each one's birthplace and residence chains — or run backward: index-lookup the two named locations, expand outward along incoming containment edges to enumerate everything inside the US and Europe, then find people attached by birth/residence edges. The query optimizer picks whichever strategy it predicts is fastest, so the application developer doesn't have to.

## Trade-offs & Pitfalls
Cypher's brevity (the emigration query fits in about four lines versus ~29 in recursive SQL — see [[Graph Queries in SQL]]) is evidence that data models are tuned for different use cases, not that one language is universally superior. Cypher's pattern matching is borrowed from the older SPARQL, so skills transfer between them.

## Examples & Systems
Neo4j (origin system); syntactic kinship with SPARQL ([[Triple-Stores and SPARQL]]); contrast with imperative graph languages like Gremlin.

## Related
- up: [[Graph-Like Data Models]] · chapter: [[Ch 02 - Data Models and Query Languages]]
- [[Property Graphs]] — the data model Cypher queries
- [[Graph Queries in SQL]] — the same query, painfully, in SQL
- [[Declarative Queries on the Web]] — why leaving strategy to the engine wins
