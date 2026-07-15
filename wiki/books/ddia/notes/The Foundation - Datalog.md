---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
topic: Graph-Like Data Models
type: subtopic
tags: [ddia, datalog, query-languages, recursion]
sources:
  - raw/ch02.md
---
# The Foundation: Datalog
> Datalog — heavily studied in the 1980s and a subset of Prolog — underlies later graph query languages: facts as predicate(subject, object) plus reusable rules that derive new predicates recursively.

## The Idea
Datalog long predates SPARQL and Cypher, and although few working engineers know it, it matters because it supplies the theoretical foundation those newer languages build on. Where Cypher and SPARQL open directly with a match-and-return query, Datalog proceeds in small composable steps: you define named rules, and rules can reference other rules or themselves, so complex queries are assembled from reusable pieces. That composability is its superpower — less convenient for a quick one-off lookup, markedly better once the data and the questions get complex.

## How It Works
The data model generalizes the triple-store: instead of a (subject, predicate, object) triple, a fact is written *predicate(subject, object)* — e.g., a location's name, its type, a `within` fact linking it to its parent region, or a `born_in` fact linking a person to a place. Queries are built from **rules** using the `:-` operator: the head (left side) is treated as a newly derived fact whenever bindings can be found that satisfy every predicate on the body (right side). Capitalized words are variables, matched against stored facts exactly as patterns match in [[The Cypher Query Language]] or [[Triple-Stores and SPARQL]]. Derived predicates are not stored — they exist by inference. Recursion handles variable-depth traversal: one rule says a location trivially "is within" the region carrying its own name; a second says a location is within region N if it is `within` some intermediate place that is itself (recursively) within N. Repeated application walks the containment chain step by step — Idaho → USA → North America — and a third rule then joins birth-place and residence chains to answer the chapter's emigration question (who was born in the US and lives in Europe), with the person left as the unknown variable the system solves for.

## Trade-offs & Pitfalls
Datalog demands a different mental model — declaring inference rules rather than composing one pattern — which feels heavyweight for simple queries. The payoff arrives with complexity: rules are combined and reused across many queries, like functions calling functions, whereas Cypher/SPARQL patterns are one-shot. Syntax is a surface detail: Datomic and Cascalog use Clojure S-expressions rather than the Prolog-style notation, with no functional difference.

## Examples & Systems
Datomic uses Datalog as its query language; Cascalog applies Datalog to querying large datasets on [[Hadoop]]. Datalog itself is a subset of Prolog, familiar from computer-science curricula.

## Related
- up: [[Graph-Like Data Models]] · chapter: [[Ch 02 - Data Models and Query Languages]]
- [[Triple-Stores and SPARQL]] — the triple model Datalog generalizes
- [[The Cypher Query Language]] — the jump-straight-in style Datalog contrasts with
- [[Graph Queries in SQL]] — recursive CTEs are SQL's clumsier answer to the same recursion
