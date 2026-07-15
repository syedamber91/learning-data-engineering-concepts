---
persona: vutr
kind: entity
sources:
- raw/sql-fundamentals-and-execution-model-additional/sql-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: relational-model
topics:
- sql-fundamentals-and-execution-model
- history-of-data-engineering
---

In June 1970, Edgar F. Codd, working at IBM, published "A Relational Model of Data for Large Shared Data Banks," introducing what became the dominant approach for relational database management systems (RDBMS). Before Codd's paper, databases were dominated by navigational models such as the hierarchical and network models, where data was accessed by "navigating" through records via pointers and predefined paths — the programmer had to specify the exact step-by-step procedure (the *how*) to retrieve information. Codd judged that a bad design, because only heavily trained technical users could operate it. His relational model instead organized data into simple tables ("relations") made of rows ("tuples") and columns ("attributes").

The deeper shift Codd made was separating the logical representation of data from its physical storage and access methods. That separation is what enabled a declarative language: a user specifies *what* data they want and leaves the *how* of retrieving it to the database management system. Following Codd's paper, IBM scientists Donald Chamberlin and Raymond Boyce built a language to implement the model, originally called Structured English Query Language (SEQUEL) — later shortened to SQL (still often pronounced "sequel"). The first commercially available SQL implementation came in 1979 from Relational Software, Inc., the company that would later become Oracle Corporation. ANSI standardized SQL in 1986, and ISO followed in 1987.

SQL's declarativeness doesn't mean the database skips procedural work — it still has to translate the query into concrete steps (reading tables, selecting fields, and so on). The mathematical framework underneath that translation is relational algebra, the set of operators over relations detailed in [[selection-operator]] — the historical throughline being that Codd's separation of logical model from physical access is exactly what makes a declarative operator algebra possible in the first place.

*See also: [[selection-operator]] · [[sql-execution-order]] · [[query-lifecycle]]*
