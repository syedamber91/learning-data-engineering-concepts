---
title: "dbt (Data Build Tool) — Roadmap (MOC)"
tags: [moc, dbt, roadmap]
---

# dbt (Data Build Tool) — Roadmap

*Up: [[data-pipelines-moc|Data Pipelines]]*

This is your complete learning path for **dbt**, the tool that owns the **T** (transform) in modern **ELT** pipelines. You have already learned how raw data is *moved* and *scheduled* in [[dags-schedulers|DAGs & Schedulers]] and guarded in [[data-quality-validation|Data Quality & Validation]]. dbt is what you reach for *after* the data has landed in the warehouse, to turn raw tables into clean, tested, documented models that analysts can trust.

Work through the lessons top to bottom — each one recaps the one before and points to the next, so the whole topic reads as a single connected course. **Prerequisites from elsewhere in the vault:** [[tables-keys-sql-basics|Tables, Keys & SQL Basics]] (you must be comfortable with SQL `SELECT`), and ideally [[star-schema|Star Schema]] and [[slowly-changing-dimensions|Slowly Changing Dimensions]] for the modelling lessons.

---

## Phase 1 — Foundations
*Get a project running and write your first connected models.*

- [[what-dbt-is-the-t-in-elt|What dbt Is & the T in ELT]] — why dbt exists and where it fits in ELT.
- [[dbt-projects-profiles-targets|dbt Projects, Profiles & Targets]] — the project layout and how dbt connects to a warehouse.
- [[models-the-ref-function|Models & the ref() Function]] — models are SELECTs; `ref()` wires them into a dependency graph.
- [[sources-the-source-function|Sources & the source() Function]] — declare the raw tables where data enters dbt.

> **Milestone:** You can stand up a dbt project, connect it to a warehouse, and build a small chain of models that read from declared sources.

## Phase 2 — Building models well
*Decide how results are stored and how to organise many models.*

- [[materializations|Materializations]] — view vs table vs ephemeral, and the cost trade-offs.
- [[incremental-models|Incremental Models]] — process only new rows instead of rebuilding everything.
- [[project-structure-staging-intermediate-marts|Project Structure: Staging, Intermediate & Marts]] — the staging → intermediate → marts layering.

> **Milestone:** You can choose the right materialization for a model, build large tables incrementally, and lay out a project that stays readable as it grows.

## Phase 3 — Reuse & templating
*Stop repeating SQL; capture history and static data.*

- [[jinja-templating-in-dbt|Jinja Templating in dbt]] — variables, loops, and conditionals that generate SQL.
- [[macros-packages|Macros & Packages]] — reusable functions and community packages like dbt_utils.
- [[seeds|Seeds]] — load small static CSV lookup tables.
- [[snapshots-scd-type-2|Snapshots & SCD Type 2]] — capture how source rows change over time.

> **Milestone:** You can factor repeated SQL into macros, pull in packages, load reference data, and track slowly changing dimensions automatically.

## Phase 4 — Quality & shipping
*Make the project correct, understandable, and production-ready.*

- [[tests|Tests]] — generic and singular assertions that block bad data.
- [[documentation-lineage|Documentation & Lineage]] — a generated docs site and the lineage DAG.
- [[the-dbt-build-workflow|The dbt build Workflow]] — run, test, snapshot, and seed together in one command.
- [[deployment-environments-ci|Deployment, Environments & CI]] — scheduled prod runs and CI on every pull request.

> **Milestone:** You can test, document, build, and deploy a dbt project the way a real analytics-engineering team does.

---

> Tip: open the graph view (Ctrl/Cmd+G) to see how these lessons connect to the wider vault — especially the modelling notes in [[data-modeling-moc|Data Modeling]].
