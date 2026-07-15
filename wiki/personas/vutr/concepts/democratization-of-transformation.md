---
persona: vutr
kind: concept
sources:
- raw/dbt-and-dimensional-modeling/why-is-dbt-so-popular.md
- raw/dbt-and-dimensional-modeling/how-to-learn-dbt-cheap-and-fast.md
last_updated: '2026-07-15'
qc: passed
slug: democratization-of-transformation
topics:
- dbt
---

Vu traces the democratization of data transformation to a specific staffing bottleneck. A team of highly skilled data engineers is expensive, and most organizations — especially mid-sized companies and startups — run with only one or two. A data engineer can manage two or three pipelines well, but as that number grows toward fifty, development, testing, and deployment overhead slows everything down: data quality suffers, requested changes queue up, and the data team falls behind business demand. In Vu's framing, the data engineer becomes the bottleneck.

The alternative he lays out is to stop requiring a small group of specialists to own every transformation, and instead let data analysts take a more active role. Since DAs already understand the business domain deeply, letting them define and build transformations directly — rather than waiting on a DE to implement each request — means the final datasets are more likely to align with business needs from the start, without the back-and-forth of a handoff. What made this practically possible, in his account, was the same ELT-era shift discussed under [[elt-vs-etl]]: cheaper storage, powerful in-warehouse SQL, and the arrival of dbt gave SQL-literate analysts a route into transformation work that used to require robust coding skills.

He's explicit that this does not mean analysts replace engineers. His stated view is that dbt lets DEs and DAs collaborate: DAs contribute business-domain knowledge and write the transformation logic itself, while DEs contribute the harder engineering judgment — how to optimize a query against the underlying engine, how to enforce organizational standards for writing modular, reusable dbt macros, and the infrastructure work (scaling Spark clusters, maintaining Airflow) that democratized SQL transformation still depends on underneath.

He also draws a firm boundary around what democratization does *not* license: giving a wide range of people the ability to write SQL transformations doesn't mean those transformations can be done arbitrarily. The transformation still has to serve the organization's data modeling — see [[data-modeling-is-not-dbt-modeling]] — and dbt's role is to manage the SQL, not to decide whether that SQL is organized well.

*See also: [[dbt]] · [[dbt-origin-and-adoption]] · [[data-modeling-is-not-dbt-modeling]] · [[elt-vs-etl]] · [[dimensional-modeling]]*

## Open questions
- How far can this democratization go before the absence of a real data model starts to hurt — where is the boundary between enabling analysts and letting transformation happen without modeling discipline behind it? Vu names the tension but does not resolve it.
