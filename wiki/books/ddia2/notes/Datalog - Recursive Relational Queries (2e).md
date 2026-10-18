---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
topic: Graph-Like Data Models
type: subtopic
tags: [ddia2, datalog, recursion, rules, datomic, derived-tables]
sources:
  - raw/ch03.md
---
# Datalog: Recursive Relational Queries
> Cypher and SPARQL jump straight in with SELECT. Datalog takes a small step at a time — defining rules that build on rules, the way you break code into functions.

## The Idea
**Datalog** is much older than SPARQL or Cypher, arising from academic research in the 1980s. It is less well known among software engineers and not widely supported in mainstream databases, but the book argues it **ought to be better known**, since it is very expressive and especially powerful for complex queries. It is based on a **relational** data model, not a graph — it appears in this section because **recursive queries on graphs are a particular strength of Datalog**.

## How It Works
The contents of a Datalog database are **facts**, each corresponding to a row in a relational table. If a `location` table has columns ID, name, and type, the fact that the US is a country is written `location(2, "United States", "country")`. In general `table(val1, val2, …)` means the table contains a row with those values.

Rather than a single query, you **define rules that derive new virtual tables from the underlying facts**. These derived tables are like SQL views: not stored, but queryable like stored facts. The book defines three — `within_recursive`, `migrated`, and `us_to_europe`. A rule's name and columns are given by what appears **before** the `:-` symbol; its content is defined by what appears **after**, where you try to find rows matching a pattern. `person(PersonID, PName)` matches the row `person(100, "Lucy")`, binding `PersonID` to 100 and `PName` to `"Lucy"`. **A rule applies when the system can find a match for all patterns on the righthand side of `:-`; when it applies, it is as though the lefthand side were added to the database**, with variables replaced by matched values.

The recursion works by repeated application:
1. `location(1, "North America", "continent")` exists, so rule 1 applies, generating `within_recursive(1, "North America")`.
2. `within(2, 1)` exists and step 1 produced `within_recursive(1, "North America")`, so rule 2 applies, generating `within_recursive(2, "North America")`.
3. `within(3, 2)` exists and step 2 produced `within_recursive(2, …)`, so rule 2 applies again, generating `within_recursive(3, "North America")`.

By repeatedly applying rules 1 and 2, `within_recursive` comes to contain every location inside North America. Rule 3 then finds people born in some `BornIn` and living in some `LivingIn`; rule 4 invokes rule 3 with `BornIn = 'United States'` and `LivingIn = 'Europe'` and returns just the names — arriving at the same answer as the Cypher and SPARQL versions.

## Trade-offs & Pitfalls
- **Datalog requires a different kind of thinking** from the other query languages in the chapter. It lets complex queries be built up rule by rule, with one rule referring to others, much as you break code into functions that call each other. And just as functions can be recursive, **Datalog rules can invoke themselves** — which is what enables graph traversal.
- The trade is up-front comprehension cost against composability on genuinely complex queries. Its limited mainstream support is the practical obstacle.

## Examples & Systems
Datomic, LogicBlox, CozoDB, and LinkedIn's **LIquid** as Datalog-based systems.

## Since the 1st Edition
The 1st edition's version was titled [[The Foundation - Datalog]] and presented Datalog largely as the historical foundation underlying other query languages. The 2nd edition **retitles and repositions it** as a live, under-used option for recursive relational queries, adds CozoDB and LinkedIn's LIquid to the systems list, and makes the function-decomposition analogy explicit.

## Related
- up: [[Graph-Like Data Models (2e)]] · chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[Graph Queries in SQL (2e)]] — recursion the clumsy way
- [[The Cypher Query Language (2e)]] — recursion as a path operator
- 1st edition: [[The Foundation - Datalog]] — the same subtopic under its old title
