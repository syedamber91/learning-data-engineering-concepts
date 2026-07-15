---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
topic: Graph-Like Data Models
type: subtopic
tags: [ddia, rdf, sparql, triple-store, semantic-web]
sources:
  - raw/ch02.md
---
# Triple-Stores and SPARQL
> Everything as (subject, predicate, object) statements — the property graph in different vocabulary, with a mature toolchain worth knowing despite semantic-web baggage.

## The Idea
The triple-store model says the same things as the property graph model in different words, and it's worth knowing because its ecosystem of tools and languages is genuinely useful. All data becomes three-part statements: *(subject, predicate, object)* — e.g., *(maria, plays, violin)*, where *maria* is the subject, *plays* the predicate, *violin* the object.

## How It Works
The subject is always a vertex. The object is one of two things, which determines the triple's meaning:

1. **A primitive value** (string, number): then predicate + object act as a property key/value on the subject vertex — *(maria, age, 29)* ≈ a vertex with `{"age": 29}`.
2. **Another vertex**: then the predicate is an edge, subject the tail, object the head — *(maria, mentors, kenji)* is an edge labeled by the predicate.

**Turtle notation** (a subset of Notation3) writes triples as plain text lines with `_:name` placeholders for vertices — names meaningful only within the file, existing solely so triples can refer to the same vertex. Semicolons let one subject carry several statements on a single line, keeping the format compact and readable.

**The semantic web** is a *separate* idea often conflated with triple-stores (Datomic, for instance, is a triple-store with no semantic-web ambitions — technically it uses 5-tuples, adding versioning metadata). The vision: sites already publish human-readable pages, so let them also publish machine-readable data via RDF (Resource Description Framework), merging into an internet-wide web of data. It was overhyped in the early 2000s, drowned in acronyms and overcomplex standards, and never materialized — but produced good work regardless, and triples stand on their own as an internal application data model.

**RDF specifics:** Turtle is the pleasant serialization; RDF/XML expresses the same thing far more verbosely (Apache Jena converts between formats). Because RDF targets internet-scale data mixing, subjects/predicates/objects are often URIs acting as namespaces — two sites can both define a "within" predicate without collision since their full URIs differ. The namespace URL needn't resolve to anything; declare the prefix once and move on.

**SPARQL** ("sparkle": SPARQL Protocol and RDF Query Language) queries RDF triple-stores. It *predates* Cypher, which borrowed its pattern matching, so they look alike — the emigration query is even terser in SPARQL. Variables take a `?` prefix, and predicate paths with `*` handle variable-depth traversal. Since RDF makes no property/edge distinction, one syntax matches both.

## Trade-offs & Pitfalls
Don't dismiss the model because of semantic-web cynicism; equally, don't adopt RDF's URI ceremony unless you need cross-dataset merging.

## Examples & Systems
Datomic, AllegroGraph (triple-stores); Turtle/N3, RDF/XML (formats); Apache Jena (tooling); SPARQL (query language).

## Related
- up: [[Graph-Like Data Models]] · chapter: [[Ch 02 - Data Models and Query Languages]]
- [[Property Graphs]] — the equivalent model in other words
- [[The Cypher Query Language]] — pattern matching descended from SPARQL
- [[The Foundation - Datalog]] — triples generalized to predicate(subject, object)
