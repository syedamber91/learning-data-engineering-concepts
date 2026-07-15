---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
topic: Graph-Like Data Models
type: subtopic
tags: [ddia, sql, recursive-cte, graph-queries]
sources:
  - raw/ch02.md
---
# Graph Queries in SQL
> SQL can traverse graphs via recursive CTEs, but the 4-line Cypher query balloons to ~29 clumsy lines — proof that model fit matters.

## The Idea
Since a property graph can live in two relational tables (vertices + edges), a natural question follows: can SQL query it? Yes — but awkwardly. The core difficulty is that ordinary SQL assumes you know *in advance* which joins a query needs, whereas graph traversal may cross a *variable, unknown* number of edges before reaching the target vertex — the number of joins isn't fixed when you write the query.

## How It Works
The variable-depth problem is exactly what Cypher's `WITHIN*0..` ("zero or more containment hops") handles in one token: a residence edge might point directly at the sought location or be several levels down a hierarchy of streets, cities, regions, and countries.

SQL gained an equivalent in SQL:1999: *recursive common table expressions* (`WITH RECURSIVE`), supported by PostgreSQL, IBM DB2, Oracle, and SQL Server. The emigration query built this way proceeds in stages:

1. Build a vertex-ID set for "inside the US": seed it with the vertex named for the US, then repeatedly add the tail of every containment edge whose head is already in the set, until no new vertices appear (transitive closure).
2. Build the analogous set for "inside Europe."
3. Derive the people born in the US: tails of birth edges whose heads fall in set 1.
4. Derive the people living in Europe: tails of residence edges whose heads fall in set 2.
5. Join (intersect) the two people sets and return each survivor's name property.

Correct, standard, portable — and roughly 29 lines of dense SQL for what Cypher states in about 4.

## Trade-offs & Pitfalls
- The verbosity isn't a flaw in SQL so much as a mismatch: the relational model wasn't designed around recursive traversal, so expressing it fights the grain.
- The chapter's takeaway is a selection principle: different data models target different use cases; when one language needs 29 lines for another's 4, pick the model that fits your application.
- Emulation always remains *possible* (echoing the Summary: any model can imitate another) — the cost is clumsiness, not impossibility.

## Examples & Systems
PostgreSQL, IBM DB2, Oracle, SQL Server (recursive CTE support); Neo4j/Cypher as the concise baseline.

## Related
- up: [[Graph-Like Data Models]] · chapter: [[Ch 02 - Data Models and Query Languages]]
- [[The Cypher Query Language]] — the concise counterpart
- [[Property Graphs]] — the two-table relational encoding being queried
- [[The Foundation - Datalog]] — recursion as a first-class rule mechanism
