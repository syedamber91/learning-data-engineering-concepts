---
persona: vutr
kind: entity
sources:
- raw/dbt-and-dimensional-modeling/deep-dive-into-the-kimball-dimensional.md
- raw/dbt-and-dimensional-modeling/i-spent-6-hours-learning-about-slowly.md
last_updated: '2026-07-15'
qc: passed
slug: surrogate-keys
topics:
- dbt
---

Kimball's guidance, as Vu applies it, is that a dimension's primary key should not be the same key used by the operational system that produced the data — using a separate surrogate key decouples how the warehouse manages identity from however the source system happens to manage its own keys. Historically, standard practice was a monotonically increasing integer surrogate key; Vu notes the alternative — the one he actually uses — of computing the surrogate key with a cryptographic hash function over the record's data.

In his own dbt project, he generates surrogate keys with the `dbt_utils.generate_surrogate_key` macro, which hashes a list of input columns using MD5. The key detail he calls out explicitly: you only need to hash the columns that are actually expected to change — for his `dim_product` table he assumed every field could change, so every field went into the hash. This is also what makes SCD Type 2 work mechanically: when a dimension record changes, the new row gets a *different* surrogate key from the original (because the hashed inputs changed), while the business key — the source system's original identifier — stays the same across versions, letting the pipeline detect "this is a new version of an existing entity" rather than "this is a brand-new entity." Fact rows reference whichever surrogate key corresponds to the dimension version valid at the fact's own point in time.

*See also: [[star-schema]] · [[grain-declaration]] · [[dbt]] · [[scd-type-2]] · [[scd-type-1-and-3]] · [[dbt-origin-and-adoption]] · [[dbt-incremental-strategies-for-scd]]*
