---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
type: chapter-moc
tags: [ddia2, architecture, oltp, olap, cloud, distributed-systems, moc]
sources:
  - raw/ch01.md
---
# Ch 01 – Trade-Offs in Data Systems Architecture
An entirely new opening chapter, and its thesis is in the title: there are no solutions, only trade-offs. Rather than teaching a technology, it lays out four axes along which every data architecture is positioned — operational versus analytical, cloud versus self-hosted, distributed versus single-node, and business need versus the rights of the people in the data — and defines the vocabulary the remaining thirteen chapters lean on. The chapter's quiet argument is that most architectural disagreements are not technical disputes at all: they are two teams with different priorities using the same words for different things.

## Map
- [[Operational Versus Analytical Systems (2e)]] — the OLTP/OLAP split, why analytics gets its own copy of the data, and who is served by each
  - [[Characterizing Transaction Processing and Analytics (2e)]] — point queries versus aggregating scans, and the real-time analytics systems that blur the line
  - [[Data Warehousing (2e)]] — a separate read-only database fed by ETL; the drift to data lakes, streams, and reverse ETL
  - [[Systems of Record and Derived Data (2e)]] — the source of truth versus everything you can rebuild from it
- [[Cloud Versus Self-Hosting (2e)]] — build-or-buy applied to data infrastructure
  - [[Pros and Cons of Cloud Services (2e)]] — when renting is cheaper, and the loss-of-control costs nobody prices in
  - [[Cloud Native System Architecture (2e)]] — services layered on services; [[Separation of Storage and Compute (2e)]] and multitenancy
  - [[Operations in the Cloud Era (2e)]] — DevOps/SRE, and capacity planning turning into financial planning
- [[Distributed Versus Single-Node Systems (2e)]] — the eight reasons to go distributed, and the standing advice not to rush
  - [[Problems with Distributed Systems (2e)]] — partial failure, network cost, [[Observability (2e)]], cross-service consistency
  - [[Microservices and Serverless (2e)]] — a technical solution to a people problem, plus function-as-a-service
  - [[Cloud Computing Versus Supercomputing (2e)]] — why HPC's checkpoint-and-restart model does not transfer
- [[Data Systems, Law, and Society (2e)]] — GDPR, the right to be forgotten versus append-only logs, and data minimization

## Chapter Summary
The chapter's four comparisons all resolve the same way: it depends, and the job is knowing on what. **Operational (OLTP) systems** handle floods of small point queries against the current state of the data and are where data is born; **analytical (OLAP) systems** run few, large, aggregating queries over history and hold a read-only copy. That split produced the data warehouse, then the data lake (files, no imposed schema), then pipelines that carry events rather than nightly dumps, and now reverse ETL pushing analytical output back into production. Cutting across it is the **system of record versus derived data** distinction — a property of how you use a database, not of the database itself — which is the single most clarifying question to ask of a confusing architecture.

**Cloud versus self-hosting** is a business question wearing technical clothes: rent when your load is spiky or the system is one you don't know how to operate, own when your load is predictable and you already have the skills. The genuinely new technical consequence is **cloud native** design — building on object storage rather than virtual disks, disaggregating storage from compute, and running multitenant — which is why Aurora, Spanner, Snowflake, and BigQuery behave unlike the self-hosted systems they resemble.

**Distributed systems** buy fault tolerance, scale, geographic latency, elasticity, specialized hardware, and legal compliance, and pay for it with partial failure, network latency, and troubleshooting difficulty; single-node engines like DuckDB and SQLite have grown enough that the book explicitly warns against distributing prematurely. Finally, the chapter insists that **law and ethics are architectural inputs**: the right to erasure sits in genuine tension with the immutable append-only logs that later chapters build on, and the honest response is often to store less.

## Since the 1st Edition
This chapter did not exist in the 1st edition. Its material is partly new (cloud native architecture, serverless, data lakes, HTAP, legal compliance as a design constraint) and partly promoted from elsewhere: the OLTP/OLAP comparison and data warehousing were a mid-chapter detour inside 1st-edition Chapter 3 ([[Transaction Processing or Analytics]] and [[Data Warehousing]]), and systems-of-record/derived-data was introduced late, in 1st-edition Chapter 12 ([[Derived Data]]). Moving all of it to the front changes the book's argument: the 1st edition opened by defining *quality* (reliability, scalability, maintainability); the 2nd edition opens by defining *context* and defers quality to [[Ch 02 - Defining Nonfunctional Requirements (2e)]].

## Related
- home: [[Home (2e)]] · next: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Ch 04 - Storage and Retrieval (2e)]] — why the OLTP/OLAP split shows up as two different physical layouts
- [[Ch 11 - Batch Processing (2e)]] — the pipelines that move data from operational systems into analytical ones
- [[Ch 14 - Doing the Right Thing (2e)]] — the full treatment of the ethics and privacy sketched here
- 1st edition: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]] — the chapter this one displaced from the opening slot
