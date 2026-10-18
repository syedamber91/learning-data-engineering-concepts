---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
topic: Operational Versus Analytical Systems
type: subtopic
tags: [ddia2, oltp, olap, point-query, real-time-analytics]
sources:
  - raw/ch01.md
---
# Characterizing Transaction Processing and Analytics
> OLTP fetches a few records by key and changes them; OLAP scans a huge number of records and returns a number. Almost every other difference follows from that one.

## The Idea
The word *transaction* is a historical accident: early business databases recorded actual commercial transactions — a sale, an order, a salary payment — and the term stuck even as databases spread to social posts, game moves, and address books. What persisted was not the commerce but the **access pattern**: look up a small number of records by key (a **point query**), then insert, update, or delete based on user input. Because these applications are interactive, this became **online transaction processing (OLTP)**. Analytics inverted the pattern: scan an enormous number of records and compute an aggregate — count, sum, average — rather than hand individual records back to a user. That became **online analytical processing (OLAP)**. (The *online* in OLAP is genuinely unclear; it probably signals that analysts query interactively and exploratively rather than only running predefined reports.)

## How It Works
The book's comparison table is worth carrying around:

| Property | Operational (OLTP) | Analytical (OLAP) |
|---|---|---|
| Main read pattern | Point queries — fetch individual records by key | Aggregate over a large number of records |
| Main write pattern | Create, update, delete individual records | Bulk import (ETL) or an event stream |
| Human user | End user of a web/mobile app | Internal analyst, for decision support |
| Machine use | Checking whether an action is authorized | Detecting fraud/abuse patterns |
| Type of queries | Fixed, predefined by the application | Arbitrary, ad-hoc exploration |
| Query volume | Lots of small queries | Few queries, each complex |
| Data represents | Latest state, at the current point in time | History of events over time |
| Dataset size | Gigabytes to terabytes | Terabytes to petabytes |

Two consequences the book draws out. First, **who is allowed to write SQL** differs: operational users are not given arbitrary query access, because they could read or modify data they lack permission for, or issue a query expensive enough to hurt everyone else — so OLTP runs a fixed set of queries baked into application code, with one-off queries reserved for maintenance. Analytical systems do the opposite, handing users free-form SQL or generating it from a dashboard tool such as Tableau, Looker, or Power BI. Second, "the latest state" versus "the history of events" is a data-modelling difference, not just a size one.

## Trade-offs & Pitfalls
- The boundary is not clear-cut, and the table lists *typical* characteristics, not a definition. Treating it as a hard classifier is the mistake.
- A third category has grown between them: **product analytics** or **real-time analytics** — analytical workloads (aggregating over many records) embedded in user-facing products. Pinot, Druid, and ClickHouse are built for this: ingest in real time, answer with low latency. Traditional OLAP goes the other way — batch ingest, optimised for query throughput rather than latency.
- Because OLTP query volume is high and each query is cheap, latency dominates; because OLAP query volume is low and each query is huge, throughput dominates. Optimising the wrong one is the standard tuning error.

## Examples & Systems
Tableau, Looker, and Microsoft Power BI as the query-generating front ends for OLAP; Apache Pinot, Apache Druid, and ClickHouse as the real-time/product-analytics engines that sit between the two poles.

## Since the 1st Edition
The 1st edition's [[Transaction Processing or Analytics]] carried a very similar comparison table, so the core is stable. What is new: the *real-time analytics / product analytics* category with Pinot, Druid, and ClickHouse named — in 2017 that category barely existed in the book — and the explicit note that "online" in OLAP has no clean meaning.

## Related
- up: [[Operational Versus Analytical Systems (2e)]] · chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Data Warehousing (2e)]] — the architectural response to these two patterns colliding
- [[Storage and Indexing for OLTP (2e)]] — the engines built for the left column
- [[Data Storage for Analytics (2e)]] — the engines built for the right column
- 1st edition: [[Transaction Processing or Analytics]] — the same table, one chapter later in the book
