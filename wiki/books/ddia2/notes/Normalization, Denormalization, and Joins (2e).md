---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
topic: Relational Versus Document Models
type: subtopic
tags: [ddia2, normalization, denormalization, joins, hydration, derived-data]
sources:
  - raw/ch03.md
---
# Normalization, Denormalization, and Joins
> Store an ID or store the text? The whole normalization debate collapses into that one question, and the answer is a read/write trade — not a moral position.

## The Idea
In the résumé example, `region_id` is stored as an ID rather than the plain string `Washington, DC, United States`. Why? If the UI has a free-text region field, a string makes sense. But a standardized list of regions chosen from a dropdown or autocompleter buys you: consistent style and spelling across profiles; **disambiguation** (does the string `Washington, DC` mean the district or the state?); **ease of updating**, since the name lives in one place and can be changed globally — a city renamed after political events, say; **localization**, because standardized lists can be translated so the region displays in the viewer's language; and **better search**, because the region list can encode that Washington is on the US East Coast, which the bare string cannot.

Whether you store an ID or a text string is the question of **normalization**. Using an ID makes data more normalized: human-meaningful information lives in exactly one place and everything referring to it uses an ID meaningful only inside the database. Storing the text directly duplicates human-meaningful information in every record — a **denormalized** representation.

## How It Works
- **The argument for IDs:** because an ID has no meaning to humans, it never needs to change; it can stay the same even when the information it identifies changes. Anything meaningful to humans may need to change eventually — and if it is duplicated, every redundant copy must be updated, requiring more code, more writes, more disk space, and risking inconsistency when some copies are updated and others are not.
- **The cost of IDs:** displaying a record containing an ID needs an extra lookup to resolve it into something human-readable. In relational data that is a **join** (`SELECT users.*, regions.region_name FROM users JOIN regions ON users.region_id = regions.id WHERE users.id = 251`).
- Document databases can store both normalized and denormalized data, but are often *associated* with denormalization — partly because JSON makes adding denormalized fields easy, and partly because weak join support in many document databases makes normalization inconvenient. Some don't support joins at all, so you fetch a document containing an ID and then issue a second query to resolve it. MongoDB can also join with the `$lookup` operator inside an aggregation pipeline.
- **Trade-offs of normalization.** In the résumé, `organization` and `school_name` are plain strings — denormalized, with no ID linking the many people who worked at the same company. Should they be entities? The same arguments apply: to show a school or company logo, a denormalized representation puts the logo's image URL on every individual profile, making each document self-contained but creating a headache when the logo changes, since every occurrence of the old URL must be found and updated. A normalized representation creates an organization entity holding name, logo URL, and other attributes once, and every résumé references its ID.
- **The general principle:** normalized data is usually **faster to write** (only one copy) but **slower to query** (needs joins); denormalized data is **faster to read** (fewer joins) but **more expensive to write** (more copies to update, more disk space). It is helpful to view denormalization as a form of **derived data**, since you must set up a process to update the redundant copies.

## Trade-offs & Pitfalls
- Beyond update cost, consider **consistency if a process crashes halfway through** its updates. Databases offering atomic transactions make this easier, but not all offer atomicity across multiple documents; consistency can also be maintained through stream processing.
- Normalization tends to suit **OLTP**, where both reads and updates must be fast; analytical systems often fare better **denormalized**, since they update in bulk and read-query performance dominates. At small to moderate scale a normalized model is often best — no copies to keep consistent, and join cost is acceptable. At very large scale, join cost can become problematic.
- **The social network case study shows the answer is mixed.** The materialized timeline is a cache of the expensive posts⋈follows join, kept consistent by fan-out. But X's real implementation **does not store the post text** — each entry stores only the post ID, the sender's user ID, and a little information identifying reposts and replies. So reading a timeline still performs two joins: looking up the post ID for content and statistics like like and reply counts, and looking up the sender's profile for username and picture. This resolving of IDs in application code is called **hydrating** the IDs.
- The reason for storing only IDs is that **the referenced data is fast-changing**: like and reply counts may change many times per second on a popular post, and users change usernames and photos. The timeline must show the latest values, so denormalizing them would not make sense — and storage cost would rise significantly.
- The lesson the book draws is pointed: **having to perform joins when reading data is not, as sometimes claimed, an impediment to high-performance scalable services.** Hydrating post and user IDs scales easily because it parallelises well and its cost does not depend on how many accounts you follow or how many followers you have. The most scalable approach may denormalize some things and leave others normalized; you must weigh how often each piece of information changes against read and write costs, which may be dominated by outliers. **Normalization and denormalization are not inherently good or bad.**

## Examples & Systems
MongoDB's `$lookup` aggregation-pipeline operator; X's materialized timelines storing IDs only, with hydration at read time.

## Since the 1st Edition
The 1st edition treated normalization mostly within [[Many-to-One and Many-to-Many Relationships]] and did not have this as its own subtopic. **Substantially new:** the explicit read/write trade framing, denormalization as derived data, the crash-consistency point, and above all the **X hydration case study** — a concrete, current counterexample to the "joins don't scale" folklore that the 1st edition left unchallenged.

## Related
- up: [[Relational Versus Document Models (2e)]] · chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[Materializing and Updating Timelines (2e)]] — the case study this analyses
- [[Systems of Record and Derived Data (2e)]] — the frame for treating denormalization as derivation
- [[Many-to-One and Many-to-Many Relationships (2e)]] — where IDs become unavoidable
