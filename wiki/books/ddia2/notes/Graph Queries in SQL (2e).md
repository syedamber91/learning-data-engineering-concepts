---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
topic: Graph-Like Data Models
type: subtopic
tags: [ddia2, sql, recursive-cte, with-recursive, pgql, gsql]
sources:
  - raw/ch03.md
---
# Graph Queries in SQL
> Yes, you can. The four-line Cypher query becomes 31 lines of `WITH RECURSIVE`, which is the argument for graph query languages in a single statistic.

## The Idea
Graph data can be represented in a relational database — the vertices/edges two-table schema shows that. Can you also query it in SQL? **Yes, but with some difficulty.**

## How It Works
Every edge you traverse in a graph query is effectively a **join with the edges table**. In a relational database you usually know in advance which joins a query needs. In a graph query you may need to traverse a **variable number of edges** before finding the vertex you want — so the number of joins is not fixed in advance. That is exactly what `() -[:WITHIN*0..]-> ()` expresses in Cypher: a `LIVES_IN` edge may point at a street, city, district, region, or state, and the location hierarchy may be several levels deep.

Variable-length traversal is expressible in SQL using **recursive common table expressions** — the `WITH RECURSIVE` syntax. The book gives the full 31-line version of the US-to-Europe query, which works in four stages:
1. Build `in_usa`: start from the vertex whose `name` property is `United States`, then repeatedly follow all *incoming* `within` edges, adding each tail vertex to the set, until every incoming `within` edge has been visited.
2. Build `in_europe` the same way, starting from the `Europe` vertex.
3. Build `born_in_usa`: for each vertex in `in_usa`, follow incoming `born_in` edges to find people born somewhere in the US.
4. Build `lives_in_europe`: for each vertex in `in_europe`, follow incoming `lives_in` edges.

Then intersect the two people sets with a join, and project the `name` property.

## Trade-offs & Pitfalls
- **The comparison is the point:** a 4-line Cypher query requires 31 lines in SQL. As the book puts it, this shows how much difference the right choice of data model and query language can make — and it is only the beginning, since there are further details to handle around **cycles** and choosing **breadth-first versus depth-first traversal**.
- Portability is imperfect: **Oracle has a different SQL extension** for recursive queries, which it calls *hierarchical*.
- Other graph query languages exist beyond Cypher and SPARQL — **TigerGraph's GSQL** and the **Property Graph Query Language (PGQL)** among them.

## Examples & Systems
`WITH RECURSIVE` in standard SQL; Oracle's hierarchical queries; GSQL and PGQL as further graph languages.

## Since the 1st Edition
Carried over from the 1st edition's [[Graph Queries in SQL]] with the same 4-versus-31-line comparison and the same recursive-CTE example. **New:** GSQL and PGQL named, Oracle's hierarchical extension noted, and the pointer toward cycle handling and traversal-order choice.

## Related
- up: [[Graph-Like Data Models (2e)]] · chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[The Cypher Query Language (2e)]] — the four-line version
- [[Datalog - Recursive Relational Queries (2e)]] — recursion made comfortable instead of clumsy
- 1st edition: [[Graph Queries in SQL]] — the same subtopic
