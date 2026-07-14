---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
type: topic
tags: [ddia, query-languages, declarative, sql]
sources:
  - raw/ch02.md
---
# Query Languages for Data
> Say *what* data you want, not *how* to fetch it: declarative querying hands execution strategy to the database, buying concision, safe internal optimization, and a path to parallelism.

The relational model didn't just change how data was laid out — it changed how it was asked for. IMS and CODASYL required imperative code that stepped through records in a fixed order; SQL, closely following relational algebra (e.g., the selection operator picking rows matching a condition), lets you declare the pattern of results — conditions, sorting, grouping — while the query optimizer picks indexes, join methods, and execution order. That abstraction has three payoffs. First, concision and ease. Second, freedom for the engine: because a SQL query promises nothing about row ordering or storage layout, the database can reorganize itself (say, compacting disk space) without breaking queries — imperative code might silently depend on ordering. Third, parallelism: since CPUs now scale by adding cores rather than clock speed, declarative queries, which pin down only the result pattern and not an instruction sequence, are far easier to spread across cores and machines. The chapter widens the lens with two case studies: CSS/XSL versus DOM-manipulating JavaScript in the browser, and [[MapReduce]] as a halfway house between declarative and imperative that MongoDB eventually supplemented with a declarative aggregation pipeline — a NoSQL system reinventing SQL in JSON clothing.

## Subtopics
- [[Declarative Queries on the Web]] — CSS selectors and XSL/XPath versus imperative DOM JavaScript: the same declarative-wins argument, outside databases.
- [[MapReduce Querying]] — MongoDB's map/emit/reduce model, its pure-function restrictions, and why usability pressure produced the declarative aggregation pipeline.

## Key Takeaways
- Imperative code fixes an order of operations; declarative queries fix only the shape of the answer, leaving strategy to the optimizer.
- Hiding engine internals lets the database improve performance without any query rewrites — the API is the pattern, not the algorithm.
- Limited expressiveness is a feature: the less a query can promise, the more the engine may safely rearrange.
- Declarative languages parallelize better because they never encode a sequential recipe.
- MapReduce sits between the two styles: query logic lives in code snippets (pure functions — no side effects, no extra queries) that the framework may run anywhere, in any order, and retry on failure.
- Writing two coordinated map/reduce functions is harder than one query and blinds the optimizer — hence MongoDB 2.2's aggregation pipeline, SQL-like expressiveness in JSON syntax.

## Related
- chapter: [[Ch 02 - Data Models and Query Languages]]
- [[Relational Model Versus Document Model]] — the data-model debate this querying story runs alongside
- [[Graph-Like Data Models]] — Cypher, SPARQL, and Datalog extend declarative querying to graphs
- [[MapReduce Job Execution]] — Ch 10's full cluster-scale treatment of the model
- [[Parallel Query Execution]] — MPP engines cashing in the declarative promise
