---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
type: topic
tags: [ddia2, use-cases, etl, analytics, machine-learning, derived-data]
sources:
  - raw/ch11.md
---
# Batch Use Cases
**Batch jobs are excellent for processing large datasets in bulk but aren't good for low-latency use cases.** **So you'll find batch jobs wherever there's a lot of data and data freshness isn't important.** **That might sound limiting, but a significant amount of data processing fits this model:**
- **Accounting and inventory reconciliation**, where companies verify that transactions line up with their bank accounts and inventory, are often batch jobs.
- **In manufacturing, demand forecasting commonly runs as a periodic batch job.**
- **Ecommerce, media, and social media companies train their recommendation models with batch jobs.**
- **Many financial systems are batch-based** — **the US banking network runs almost entirely on batch jobs.**

## Subtopics
- [[Extract-Transform-Load (2e)]] — the archetypal batch workload, and why schedulers make it manageable.
- [[Analytics (2e)]] — the lakehouse architecture, pre-aggregation, and ad hoc queries.
- [[Machine Learning (2e)]] — feature engineering, training, batch inference, graph algorithms, and LLM data preparation.
- [[Serving Derived Data (2e)]] — getting batch output back into production systems safely.

## Key Takeaways
- **The organising criterion is simple and worth remembering: a lot of data, and freshness doesn't matter.** Everything in this topic satisfies both.
- **The four use cases correspond to four different destinations for the output** — a warehouse (ETL), an analyst's screen (analytics), a model (ML), and a production database (derived data) — and **the last one is the only one where the output crosses into an online system**, which is why it needs the most care.
- **The banking observation is a useful corrective**: batch processing is not a legacy technique being displaced by streaming; it underpins the financial system.

## Since the 1st Edition
**Entirely new as a topic.** The 1st edition's batch chapter ended with [[The Output of Batch Workflows]] — covering search indexes and key-value stores as batch output — and a philosophical section on the Unix philosophy and dataflow. **The 2nd edition replaces that with a survey of what batch processing is actually used for across industries**, which is more useful and reflects the book's broader shift toward practical framing.

## Related
- chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Batch Processing Models (2e)]] — the models these use cases run on
- [[Data Warehousing (2e)]] — the architectural context for ETL and analytics
- 1st edition: [[The Output of Batch Workflows]] — the closest predecessor
