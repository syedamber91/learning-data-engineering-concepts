---
persona: vutr
kind: concept
sources:
- raw/dbt-and-dimensional-modeling/dimensional-modeling-overview.md
- raw/dbt-and-dimensional-modeling/deep-dive-into-the-kimball-dimensional.md
- raw/dbt-and-dimensional-modeling/i-spent-6-hours-learning-about-slowly.md
last_updated: '2026-07-15'
qc: passed
slug: dimensional-modeling
topics:
- dbt
---

Dimensional modeling was first introduced in Ralph Kimball's 1996 book *The Data Warehouse Toolkit* (1st edition), and companies have widely adopted it since to organize analytic data. Vu frames its appeal as a fit with how business users already think: a retail manager naturally wants to analyze sales performance by product category, across regions, over time — products, regions, and time are distinct dimensions through which the same measurement can be sliced. Kimball's approach earns its popularity by aligning with that instinct rather than fighting it; clear thinking, in Vu's words, leads to simple data modeling.

He sets the historical stage first. Since Bill Inmon laid the foundation of data warehousing in the late 1980s, companies have separated the systems that produce data (the OLTP "left side" — sign-ups, web tracking, orders, optimized for high-concurrency point queries) from the system that answers analytic questions about that data (the OLAP "right side" — optimized for high-performance queries over large historical volumes, not high concurrency). A data warehouse, in Vu's list of criteria, must be intuitive for business users and not just developers, present data from disparate sources under consistent labels and definitions, adapt to changing needs, safeguard sensitive information, and — the criterion he calls out explicitly — be *accepted* by business users, because a technically excellent warehouse nobody uses was not, in the end, a great solution. Kimball's dimensional modeling is his candidate for meeting all of these at once.

The technique organizes data into a **star schema**: a central fact table surrounded by dimension tables, named for its resemblance to a star. Vu contrasts this deliberately with third normal form (3NF) modeling, whose goal is removing redundancy by splitting data into many separate relational entities — appropriate for operational systems where data integrity is the priority, but punishing for analytics: figuring out January revenue for users in India becomes overwhelming once you're navigating an ERD with hundreds of entities. The star schema is a considered trade of some redundancy for query simplicity and business-user legibility.

**The fact table** sits at the schema's center and stores the performance measurements from a business process's events. Kimball's guidance, which Vu repeats across every post that touches this topic, is to keep the *low-level* measurement — the individual transaction, not a pre-aggregate — because low granularity preserves flexibility for whatever question comes next. Each fact row carries foreign keys into the surrounding dimension tables plus its measures (revenue, quantity, profit). The row's level of detail is its **grain**, and every row in a fact table must sit at the same grain.

**Dimension tables** supply the context the fact table's numbers need to mean anything: the "who, what, where, when, how, and why" of each measurement event. A skyrocketing revenue number alone tells you nothing about the business; a product or territory dimension is what lets you ask *why*. Kimball's stance is that a warehouse is only as good as its dimensions, and that dimension attributes should be modeled as close to the business's own terminology as possible — "robust dimension attributes deliver robust analytic slicing-and-dicing capabilities," as Vu quotes it. Referential integrity between the two — every foreign key in the fact table correctly matching a primary key in its dimension table — is what makes the join (and the analysis) work at all.

**The four-step design process** is the method Kimball prescribes for building this schema, and Vu treats each step as strictly dependent on the one before it: (1) select the business process to analyze (sales, inventory, customer interactions); (2) declare the grain — are you tracking individual transactions, daily summaries, or monthly aggregates?; (3) identify the dimensions that describe that process's attributes; (4) identify the facts — the quantitative metrics tied to the process. Skipping ahead breaks the chain: you cannot sensibly pick dimensions before the grain is fixed, and you cannot pick facts before the dimensions are named.

Vu's own assessment, offered as personal reflection rather than received wisdom, is double-edged. On one hand, Kimball modeling is well-suited to how people actually observe a business (a measurement with context) and can be faster to deliver than more elaborate approaches — a reasonable default for a newly hired data engineer on a team short of time and resources. On the other hand, because the model is designed around specific analytical requirements, it can struggle to adapt when a genuinely new requirement shows up, forcing the modeler back in to add facts and dimensions. He is also explicit that Kimball is not the only game in town — Inmon and Data Vault are real alternatives — and that the choice has to be made for the organization's actual needs, not because you've read *The Data Warehouse Toolkit* three times. What he does defend without qualification is that a proven, community-tested modeling approach beats dumping data into a warehouse with no modeling discipline at all: an idiosyncratic scheme that only you understand is much harder to troubleshoot and scale than one the wider community already knows how to debug.

*See also: [[star-schema]] · [[grain-declaration]] · [[surrogate-keys]] · [[dbt]] · [[scd-type-2]] · [[scd-type-1-and-3]] · [[data-modeling-is-not-dbt-modeling]]*

## Related in the other wiki
- [[Stars and Snowflakes - Schemas for Analytics]] — DDIA's description of the fact-table-plus-dimension-tables shape (and its explicit note that the star schema "accepts some denormalization") is the schema-level mechanics behind the four-step Kimball process this note walks through in Vu's own words.
- [[Data Warehousing]] — DDIA's OLTP/OLAP separation is the same "left side vs right side" distinction Vu opens this note with, before narrowing to Kimball's specific answer for how to organize the OLAP side.
