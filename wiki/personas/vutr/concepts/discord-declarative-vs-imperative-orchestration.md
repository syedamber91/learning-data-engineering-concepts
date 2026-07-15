---
persona: vutr
kind: concept
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/how-did-discord-evolve-to-handle.md
last_updated: '2026-07-15'
qc: passed
slug: discord-declarative-vs-imperative-orchestration
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Discord's notes frame its orchestration rebuild as a single contrast: imperative scheduling, where you tell the system exactly when to run something, versus declarative automation, where you tell the system what freshness you need and let it work out the schedule.

Discord's first system, Derived (introduced in a 2021 article), used Airflow for job scheduling, visualization, and monitoring — Airflow's model, per the notes, requires specifying the imperative workflow: a defined sequence of tasks that runs on a pre-set schedule, like "at 3:00 PM" or "every 6 hours." That's a natural fit as long as your freshness requirements map cleanly onto a fixed clock, but it starts to strain once different tables downstream of the same raw data need different guarantees about how stale they're allowed to get.

After evaluating the open-source orchestration field — the notes name Airflow, Argo, Prefect, Kestra, and Mage as the candidates considered — Discord picked Dagster specifically for its different approach: declarative automation, where users specify how up-to-date they expect each data asset to be, and Dagster works out the scheduling needed to keep that promise, rather than the user pre-committing to a schedule. Beyond that core decision, the notes list concrete reasons Dagster won: a modern UI giving data engineers and scientists self-service observability into asset state; straightforward local development; out-of-the-box support for deployment and execution on Kubernetes; and built-in tooling for migrating existing Airflow jobs rather than needing a clean rewrite.

The migration also changed *how* transformation logic itself was expressed, not just how it was scheduled. Derived's transformations were dbt-adjacent by hand: users wrote SQL SELECT statements as "derived tables" inside a YAML configuration file, and the system inferred the DAG from the SQL so users never had to declare dependency structure explicitly — the YAML also carried settings like refresh frequency, schema, description, update strategy, and BigQuery-specific optimizations like clustering and partition schemes. In the Dagster era, that YAML-defined transformation logic was replaced with dbt models, integrated into Dagster via what Dagster calls "software-defined assets" — an asset being an object in persistent storage (a table, a file, a model) whose definition makes code, not a manually maintained diagram, the source of truth for what should exist and how it's computed. Each Derived (and later Dagster) transformation still runs as its own independent Kubernetes pod, a deployment-isolation choice both systems inherited from Discord's original design.

*See also: [[dbt-incremental-race-condition]] · [[persistent-message-bus-data-transfer]]*

## Related in the other wiki
- [[Designing Applications Around Dataflow]] — DDIA's discussion of specifying data freshness rather than fixed schedules is the same shift in framing that Dagster's declarative-asset model makes concrete for Discord.
