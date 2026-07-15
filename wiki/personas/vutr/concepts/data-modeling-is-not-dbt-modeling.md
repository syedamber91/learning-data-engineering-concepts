---
persona: vutr
kind: concept
sources:
- raw/dbt-and-dimensional-modeling/why-is-dbt-so-popular.md
- raw/dbt-and-dimensional-modeling/dimensional-modeling-overview.md
- raw/dbt-and-dimensional-modeling/deep-dive-into-the-kimball-dimensional.md
last_updated: '2026-07-15'
qc: passed
slug: data-modeling-is-not-dbt-modeling
topics:
- dbt
---

Vu's recurring warning, stated most directly in his dbt-popularity research, is that many people think writing dbt models is doing data modeling — and that's wrong. A data model defines how data is structured and related, and ensures consistency; it's tool-agnostic. A dbt model, by contrast, is a SQL-based transformation script that shapes raw data into a structured format inside the warehouse. Giving a wide range of people the ability to run SQL transformations does not mean those transformations happen in a meaningful order or shape — that still depends on the organization's data modeling, and dbt only manages the SQL, not the design decisions behind it. If you dump data into the warehouse without a model, adopting dbt on top of it is, in his word, pointless.

He draws the same line again in his hands-on dbt/Kimball project, this time against a specific architectural pattern rather than dbt in the abstract. There, he organizes the project's transformation through three stages — raw data loaded as-is to landing, standardized in staging, and turned into facts and dimensions in a curated layer — explicitly comparing this to the Medallion Architecture's bronze/silver/gold layers. His caution is pointed: whatever you call these layers, they are not data modeling; they are a way to facilitate data cleaning and transformation, nothing more. The modeling work — deciding what a fact table's grain is, which dimensions matter, how they relate — is a separate, prior question that the layering scheme doesn't answer for you.

The same distinction underlies his skepticism about One Big Table (OBT) in his dimensional-modeling notes: OBT only proves its value when a careful modeling layer already sits beneath it. Put all your data into one table from the start, with no modeling discipline behind it, and you trade away data understandability for query performance — which he calls "terrible." He also pushes back on a related folk belief that cloud warehouses' nested/array denormalization features (used to avoid joins) prove that "joins are bad" and therefore that "data modeling is bad for performance." His counter-observation is that BigQuery, Snowflake, and Databricks have all introduced Primary Key/Foreign Key constraints and join-optimization techniques in recent years — a sign, in his reading, that these platforms are nudging users *toward* organizing data properly, not away from it.

He locates the root failure in an era-level habit: people belittle data modeling because they need to move fast, and believe that "throwing more resources" at a slow, messy query will somehow fix it. A tool — dbt, a semantic layer, a medallion architecture, an OBT — layered over that absence doesn't resolve it; the mess in the modeling layer has to be fixed at the source.

*See also: [[dbt]] · [[dimensional-modeling]] · [[democratization-of-transformation]] · [[one-big-table]] · [[star-schema]] · [[grain-declaration]]*

## Open questions
- How far does the democratization of transformation via dbt go before the lack of a real data model starts to hurt — where is the line between enabling analysts and quietly reintroducing the mess a model is supposed to prevent? Vu raises the tension but does not draw the line.
