---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
topic: Graph-Like Data Models
type: subtopic
tags: [ddia2, triple-store, rdf, sparql, turtle, semantic-web]
sources:
  - raw/ch03.md
---
# Triple Stores and SPARQL
> Everything is a three-part statement: (subject, predicate, object). It is the property graph model wearing different words — but the tooling around it is genuinely useful.

## The Idea
The triple store model is **mostly equivalent to the property graph model**, using different words for the same ideas. It is still worth knowing, because its tools and languages are valuable additions to your toolbox.

All information is stored as very simple three-part statements: **(subject, predicate, object)**. In `(Jim, likes, bananas)`, `Jim` is the subject, `likes` the predicate (verb), and `bananas` the object.

## How It Works
The **subject** of a triple is equivalent to a vertex. The **object** is one of two things:
- A **primitive value** such as a string or number. Then the predicate and object are the key and value of a property on the subject vertex — `(lucy, birthYear, 1989)` is a vertex `lucy` with properties `{"birthYear": 1989}`.
- **Another vertex.** Then the predicate is an edge, the subject is the tail vertex, and the object is the head vertex — in `(lucy, marriedTo, alain)` both are vertices and `marriedTo` labels the edge between them.

**Turtle**, a subset of Notation3 (N3), is a readable format for writing triples. Vertices are written `_:someName`, with the name existing only within the file so you can tell which triples refer to the same vertex. Semicolons let you say multiple things about one subject:

```turtle
@prefix : <urn:example:>.
_:lucy     a :Person;   :name "Lucy";          :bornIn _:idaho.
_:idaho    a :Location; :name "Idaho";         :type "state";     :within _:usa.
_:usa      a :Location; :name "United States"; :type "country";   :within _:namerica.
_:namerica a :Location; :name "North America"; :type "continent".
```

**The RDF data model.** Turtle is one encoding of the **Resource Description Framework (RDF)**, a data model designed for the Semantic Web; RDF can also be encoded more verbosely in XML, and tools like Apache Jena convert between encodings. RDF has quirks because it is designed for **internet-wide data exchange**: subjects, predicates, and objects are often **URIs**, so a predicate might be `<http://my-company.com/namespace#within>` rather than just `WITHIN`. The reasoning is that you should be able to combine your data with someone else's — and if they attach a different meaning to `within`, there is no conflict because their predicate is actually `<http://other.org/foo#within>`. The URL need not resolve to anything; from RDF's point of view it is simply a namespace, and you declare the prefix once at the top of the file.

**SPARQL** (a recursive acronym for *SPARQL Protocol and RDF Query Language*, pronounced "sparkle") is the query language for RDF triple stores. It **predates Cypher**, and since Cypher's pattern matching was borrowed from SPARQL, the two look quite similar:

```sparql
PREFIX : <urn:example:>
SELECT ?personName WHERE {
  ?person :name ?personName.
  ?person :bornIn  / :within* / :name "United States".
  ?person :livesIn / :within* / :name "Europe".
}
```

The equivalences are direct: Cypher's `(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (location)` is SPARQL's `?person :bornIn / :within* ?location.` (variables start with `?`). Because **RDF doesn't distinguish properties from edges** — it uses predicates for both — the same syntax matches properties: Cypher's `(usa {name:'United States'})` is SPARQL's `?usa :name "United States".`

## Trade-offs & Pitfalls
- **Databases with a triple-like model often need extra metadata per tuple.** AWS Neptune uses **quads** (4-tuples), adding a graph ID; **Datomic uses 5-tuples**, extending each triple with a transaction ID and a Boolean indicating deletion. Because they retain the subject-predicate-object structure, the book still calls them triple stores.
- **The Semantic Web.** Much triple-store research was motivated by this early-2000s effort to publish data in standardized machine-readable form as well as human-readable pages. **The Semantic Web as originally envisioned did not succeed** — but its legacy survives in linked-data standards such as **JSON-LD**, biomedical-science ontologies, Facebook's **Open Graph protocol** (used for link unfurling), knowledge graphs such as **Wikidata**, and the structured-data vocabularies maintained by **Schema.org**. The book's practical conclusion: even if you have no interest in the Semantic Web, **triples can be a good internal data model for applications**.

## Examples & Systems
Datomic, AllegroGraph, Blazegraph, OpenLink Virtuoso, Apache Jena, Amazon Neptune as SPARQL-supporting stores; Turtle/N3 and RDF/XML as encodings; JSON-LD, Open Graph, Wikidata, Schema.org as Semantic Web residue.

## Since the 1st Edition
The RDF, Turtle, SPARQL, and Semantic Web material carries over from the 1st edition's [[Triple-Stores and SPARQL]] (note the 1st edition hyphenated the title). **New:** the quads/5-tuples caveat naming Neptune and Datomic, and a considerably more concrete account of the Semantic Web's legacy — JSON-LD, Open Graph link unfurling, Wikidata, and Schema.org — where the 1st edition was more dismissive and less specific about what survived.

## Related
- up: [[Graph-Like Data Models (2e)]] · chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[Property Graphs (2e)]] — the same expressive power in different vocabulary
- [[The Cypher Query Language (2e)]] — which borrowed its pattern matching from SPARQL
- 1st edition: [[Triple-Stores and SPARQL]] — the same subtopic
