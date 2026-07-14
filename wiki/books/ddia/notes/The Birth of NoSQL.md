---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
topic: Relational Model Versus Document Model
type: subtopic
tags: [ddia, nosql, data-models, polyglot-persistence]
sources:
  - raw/ch02.md
---
# The Birth of NoSQL
> NoSQL began as a catchy hashtag, not a technology — a loose banner for nonrelational databases challenging three decades of relational dominance.

## The Idea
Codd's relational model (1970) started as pure theory that skeptics doubted could ever run efficiently, yet by the mid-1980s RDBMSes and SQL had become the default answer for any regularly structured data — and stayed that way for roughly 25–30 years. Relational databases were born in mundane 1960s–70s mainframe business workloads (transaction entry, reservations, invoicing, payroll) but generalized astonishingly well: most of today's web — publishing, ecommerce, social apps, SaaS — still runs on them. Repeated challengers (the network and hierarchical models in the 70s–80s, object databases around 1990, XML databases in the 2000s) each generated hype and then faded. NoSQL, arriving around 2009–2010, is the newest challenger in that lineage.

## How It Works
The label itself carries no technical meaning: it was coined as a Twitter hashtag for a 2009 meetup about open source, distributed, nonrelational databases, and only later got back-fitted as "Not Only SQL." What unites the systems under the banner are the pressures that drove adoption:

- **Scale** — datasets or write rates that stretch a single relational server (see [[Approaches for Coping with Load]]).
- **Open source preference** — a cultural shift away from commercial database licensing.
- **Specialized queries** — access patterns the relational model serves poorly.
- **Schema frustration** — a desire for more dynamic, expressive structures than rigid relational schemas allow.

## Trade-offs & Pitfalls
Because different applications genuinely have different requirements, no single winner is expected. The realistic outcome is *polyglot persistence*: relational stores coexisting with a variety of nonrelational ones, each chosen per use case. The pitfall is treating NoSQL as a wholesale replacement — history shows every "relational killer" so far either faded or was absorbed, and document databases in particular resurrect old problems around joins and many-to-many data (see [[Are Document Databases Repeating History]]).

## Examples & Systems
The relational lineage traces to Edgar Codd's 1970 proposal and the SQL systems that followed. Earlier rivals named here: IMS (hierarchical), CODASYL (network), object databases, XML databases. The NoSQL wave includes the document stores covered next (MongoDB, CouchDB, RethinkDB) and graph systems (Neo4j, Datomic).

## Related
- up: [[Relational Model Versus Document Model]] · chapter: [[Ch 02 - Data Models and Query Languages]]
- [[The Object-Relational Mismatch]] — the schema frustration that fed NoSQL
- [[Relational Versus Document Databases Today]] — how the contest settled
- [[Partitioning]] — scalability driver behind distributed NoSQL stores
- [[Schema Evolution]] — flexible-schema desire, formalized in Chapter 4
