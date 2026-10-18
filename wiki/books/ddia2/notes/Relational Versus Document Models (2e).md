---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
type: topic
tags: [ddia2, relational, document, nosql, newsql, json]
sources:
  - raw/ch03.md
---
# Relational Versus Document Models
The best-known data model today is probably SQL's, based on the **relational model proposed by Edgar Codd in 1970**: data organised into *relations* (tables), each an unordered collection of *tuples* (rows). It began as a theoretical proposal that many doubted could be implemented efficiently, but by the mid-1980s relational database management systems and SQL had become the tools of choice for anyone storing and querying data with regular structure — and decades later many use cases, business analytics prominently among them, remain dominated by relational data.

The history of challengers is short and consistent. In the 1970s and early 1980s the **network** and **hierarchical** models were the main alternatives, and the relational model beat both. **Object databases** came and went in the late 1980s and early 1990s (not to be confused with today's object *storage* for large files). **XML databases** appeared in the early 2000s and saw only niche adoption. Each competitor generated a lot of hype in its time; none lasted. Instead SQL grew to incorporate other types of data — XML, JSON, and graph support were added to it.

In the 2010s **NoSQL** was the latest buzzword attempting to overthrow relational dominance. It referred not to a single technology but to a loose set of ideas around new data models, schema flexibility, scalability, and open source licensing. Some databases branded themselves **NewSQL**, aiming to combine NoSQL's scalability with the relational data model and transactional guarantees. Both sets of ideas were very influential in the design of data systems — but as the principles became widely adopted, use of the terms faded.

The lasting effect of NoSQL is the popularity of the **document model**, usually representing data as JSON. It was popularised by specialised document databases such as MongoDB and Couchbase, though most relational databases have since added JSON support. Compared to relational tables, often seen as rigid and inflexible, JSON documents are thought to be more flexible.

## Subtopics
- [[The Object-Relational Mismatch (2e)]] — the translation layer between objects and tables, ORMs, and their costs.
- [[Normalization, Denormalization, and Joins (2e)]] — storing an ID or a string, and what each choice costs.
- [[Many-to-One and Many-to-Many Relationships (2e)]] — the relationship shapes that resist a single document.
- [[Stars and Snowflakes - Schemas for Analytics (2e)]] — the relational conventions that dominate data warehouses.
- [[When to Use Which Model (2e)]] — the decision criteria, including schema flexibility and locality.

## Key Takeaways
- Every challenger to the relational model has been absorbed rather than victorious. SQL added XML, JSON, and graph support; document databases added joins and secondary indexes.
- The document model's real appeal is a **tree of one-to-many relationships loaded as a unit**, which maps well onto application objects and gives good locality.
- **Declarative query languages** (SQL, Cypher, SPARQL, Datalog) specify the pattern of data you want and how it should be transformed — not how to obtain it. That is attractive because such queries are more concise, and more importantly because hiding query-engine implementation details lets the database introduce performance improvements without changing any queries. A database can, for example, execute a declarative query in parallel across CPU cores and machines without you implementing that parallelism yourself; in a handcoded algorithm that would be a lot of work.
- Codd's original description of the relational model already allowed something like JSON: **nonsimple domains**, where a value in a row need not be a primitive but can be a nested relation, giving arbitrarily nested trees. The JSON and XML support added to SQL over 30 years later is comparable.

## Since the 1st Edition
The 1st edition covered the same ground across [[The Birth of NoSQL]], [[Relational Versus Document Databases Today]], and its Chapter 2 introduction. The 2nd edition's framing has visibly aged forward: NoSQL and NewSQL are described in the **past tense** as terms whose use has faded because their ideas were absorbed, rather than as a live movement. The list of failed challengers is expanded and the nonsimple-domains note is new.

## Related
- chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[Graph-Like Data Models (2e)]] — the model for when relationships dominate
- [[When to Use Which Model (2e)]] — where the locality argument is worked out
- 1st edition: [[Relational Model Versus Document Model]] — the same topic
