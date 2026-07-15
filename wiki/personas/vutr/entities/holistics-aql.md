---
persona: vutr
kind: entity
sources:
- raw/llms-ai-agents-and-vector-databases-additional/why-is-text-to-sql-so-hard.md
last_updated: '2026-07-15'
qc: passed
slug: holistics-aql
topics:
- llms-ai-agents-and-vector-databases
---

Holistics, established in 2015, is a self-service BI tool built around a [[semantic-layer-and-data-modeling|semantic layer]] from the start: before users can present or organize data, they must define the mapping between business concepts and underlying tables through Holistics's "model" abstraction, which specifies a source (a physical table or SQL query), its dimensions and measures, and its relationships to other models — Holistics uses those declared relationships to construct joins automatically.

Because that semantic foundation already existed, Holistics's path to Text-to-SQL didn't start with training a model to emit raw SQL. Their first approach had the AI translate natural language into an intermediate format the semantic layer could consume — a JSON payload naming metrics and dimensions (e.g. `{"metrics": ["total_sales"], "dimensions": ["country"]}`) — but that format tops out on simple questions and can't express nested aggregation or period-over-period comparisons that real analytical questions need.

Their actual solution is AQL, a proprietary analytics query language that predates the LLM effort and was built specifically to operate over the semantic layer, so users can query at a higher level of abstraction than raw tables and columns. AQL treats metrics as first-class, composable, reusable objects — unlike SQL, where reusing a calculation means saving the query that produces it in a CTE, view, or table, and touching every copy whenever the logic changes. Queries are written against business concepts (`total_revenue` by `user_country`) without hand-written joins, and AQL's pipe operator (`|`) threads the output of one expression into the next, producing a readable, sequential, top-to-bottom flow instead of nested SQL clauses.

Holistics trained its models to generate AQL rather than SQL directly, with the AQL then mechanically converted to SQL by Holistics's own well-tested conversion layer. The stated payoff has four parts: AQL output is more compact and human-readable than raw SQL, so a reviewer can verify the AI's intent at a glance; it's more reliable because the model no longer has to reproduce dialect-specific syntax, join logic, or advanced-analytics formulas from scratch — it only has to map intent onto predefined metrics and dimensions; it's governed because every AQL query is forced through the semantic layer and therefore inherits its access controls and single source of truth for business definitions, so the model can't invent its own metric math; and it stays flexible enough for complex analytics, unlike the earlier JSON-payload approach.

*See also: [[text-to-sql-challenges]] · [[semantic-layer-and-data-modeling]] · [[rag]]*
