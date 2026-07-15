---
persona: vutr
kind: concept
sources:
- raw/dbt-and-dimensional-modeling/deep-dive-into-the-kimball-dimensional.md
last_updated: '2026-07-15'
qc: passed
slug: dbt-incremental-strategies-for-scd
topics:
- dbt
---

In his hands-on Kimball-plus-dbt project, Vu implements SCD Type 2 two different ways against the same `dim_product` and `dim_territories` tables, deliberately choosing the harder path first so he'd fully understand the mechanics before reaching for dbt's shortcut.

**The manual approach uses dbt's `merge` incremental strategy.** Merge requires specifying a unique key so dbt can run a merge statement behind the scenes: incoming rows whose keys already exist in the target get updated, rows with new keys get inserted. To drive SCD Type 2 through merge, Vu's model compares incoming data against only the *current* version of each dimension record (filtering `is_current = true`, referencing the target table via dbt's `this` keyword) and joins on the business key to detect two kinds of change: rows whose business key doesn't exist yet in the dimension (new records, condition `t_product_key is null`) and rows whose business key exists but whose surrogate key differs (a new version of an existing record, condition `t_product_key is not null AND s_product_surrogate_key != t_product_surrogate_key`). Both kinds get inserted with `is_current = true`. The existing row being superseded also needs to be explicitly expired — `expired_date` set to the day before the new version's `effective_date`, `is_current` flipped to false — and the new and expired rows are unioned together into the single dataset dbt merges: changed data becomes inserts, expired data becomes updates on the existing rows. He also has to handle first-run vs. incremental-run behavior explicitly using dbt's `is_incremental` macro, since dbt automatically treats a model's very first run as a `full_refresh` regardless of the incremental logic defined for subsequent runs — in his project he sidesteps needing the full historical load by always filtering on a `snapshot_date` variable, so the first run simply seeds the table with a single starting snapshot.

**The alternative is dbt's built-in `snapshot` feature**, which most external resources recommend for SCD Type 2 specifically because it implements the type-2 bookkeeping (new rows, expiry dates, current flags) automatically rather than requiring the merge logic above to be hand-written. Because his dimension logic pulls from multiple staging tables rather than one single source table, he has to work around dbt snapshot's expectation of a single dbt-`source`-registered table: he first materializes a `tmp_dim_product_snapshot` model (overwritten each run with one snapshot date's data), registers *that* model's output as a dbt source, and only then points `dbt snapshot`'s change-tracking configuration at it. Run against successive snapshot dates, this reproduces the same SCD Type 2 history his manual merge logic built by hand. Vu's own verdict, after implementing both: for a production environment the snapshot approach is the better choice, since dbt handles the SCD Type 2 bookkeeping that he found genuinely complex to develop and debug by hand — though he flags that registering a dbt model's materialized output back as a dbt source, just to make it snapshot-eligible, feels like a workaround rather than a clean use of the feature, and he explicitly invites correction from anyone who has implemented it differently.

**For the fact table**, `fact_sale`, he chooses a third incremental strategy: `insert_overwrite`. His stated reason is idempotency — rerunning the model for the same snapshot date should produce the same result rather than duplicating rows. The `append` strategy could also load the data, but repeated runs for the same date would create duplicate fact rows, since append has no notion of "this date's data already exists, replace it." To assemble each fact row, the model joins the sale data to `dim_product` and `dim_territories` on their business keys and confirms the fact's `snapshot_date` falls within the correct dimension version's `effective_date`/`expired_date` range — which is precisely what makes the dimension's SCD Type 2 history queryable at the fact-join level.

*See also: [[dimensional-modeling]] · [[scd-type-2]] · [[surrogate-keys]] · [[grain-declaration]] · [[dbt]]*

## Open questions
- Vu names `insert_overwrite` as idempotent for the fact table but doesn't spell out the underlying mechanism (e.g. whether it's a partition-replace operation and how the affected partition boundary is determined) beyond contrasting it with `append`'s duplication behavior.
