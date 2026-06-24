---
title: "dbt Quick-Recall Flashcards"
area: "Data Pipelines"
topic: "dbt (Data Build Tool)"
tags: [dbt, flashcards, review, recall, study]
---

# dbt Quick-Recall Flashcards

*Part of [[dbt-data-build-tool-moc|dbt (Data Build Tool)]] · [[data-pipelines-moc|Data Pipelines]]*

*Synthesized companion · see [[synthesized-moc|Synthesized Notes]]*

---

The lesson "Check yourself" sections test one concept at a time. This note is a **spaced-recall
layer**: one or two crisp prompts per lesson, all in one place, so you can re-encounter the key
facts of the whole dbt course in a few minutes. Cover the answers, work top to bottom, and
follow the link on any card you miss back to the full lesson.

Format: **Q** prompt, then the answer on the next line. Each group links to its source lesson.

---

## Phase 1 — Foundations

**[[what-dbt-is-the-t-in-elt|What dbt Is & the T in ELT]]**

- **Q: What does dbt do, and what does it *not* do?**
  It does the **T** in ELT — transforms data already in the warehouse. It does not extract,
  load, or move data; separate EL tools (Fivetran, Airbyte) do that.
- **Q: If dbt isn't a database, what builds your tables?**
  The warehouse. dbt compiles a `SELECT` into `CREATE TABLE AS` and the warehouse runs it.

**[[dbt-projects-profiles-targets|dbt Projects, Profiles & Targets]]**

- **Q: What's the difference between `dbt_project.yml` and `profiles.yml`?**
  `dbt_project.yml` is the blueprint (name, paths, defaults) and is committed. `profiles.yml`
  holds the warehouse connection + secrets, lives in `~/.dbt/`, and is **never** committed.
- **Q: What is a target?**
  A named connection block inside `profiles.yml` (e.g. `dev`, `prod`). Switch with `--target`.

**[[models-the-ref-function|Models & the ref() Function]]**

- **Q: What two jobs does `ref()` do?**
  Returns the correct fully-qualified table name (dev/prod portable), **and** registers a
  dependency so dbt builds that model first.
- **Q: Why never hard-code another model's table name?**
  It loses dev/prod portability and hides the dependency, so dbt may build in the wrong order.

**[[sources-the-source-function|Sources & the source() Function]]**

- **Q: `source()` vs `ref()` — what does each point at?**
  `source()` points at a **raw** table an EL tool loaded; `ref()` points at a table **dbt
  built**.
- **Q: What does `dbt source freshness` check?**
  How recently the raw source was loaded (`loaded_at` vs now, against `warn_after`/
  `error_after`) — not whether your models ran.

---

## Phase 2 — Building models well

**[[materializations|Materializations]]**

- **Q: Name the four materializations and the default.**
  `view`, `table`, `ephemeral`, `incremental`. Default is **view**.
- **Q: When do you choose `table` over `view`?**
  When the SQL is expensive and read often — build once, read cheaply many times (e.g. marts).

**[[incremental-models|Incremental Models]]**

- **Q: When does `is_incremental()` return false?**
  First run, table doesn't exist yet, or `--full-refresh` — in which cases dbt does a full build.
- **Q: What does `unique_key` change?**
  Switches blind append → merge/upsert on that key, preventing duplicates and making reruns
  idempotent.

**[[project-structure-staging-intermediate-marts|Project Structure: Staging, Intermediate & Marts]]**

- **Q: What are the three layers and their prefixes?**
  Staging (`stg_`, 1:1 clean of a source), intermediate (`int_`, shared logic), marts
  (`fct_`/`dim_`, business-facing).
- **Q: What's the one rule that keeps a big project from becoming spaghetti?**
  Each layer only reads from the layer to its left — never skip backward.

---

## Phase 3 — Reuse & templating

**[[jinja-templating-in-dbt|Jinja Templating in dbt]]**

- **Q: When does a Jinja `for`-loop actually run?**
  At compile time. It unrolls into static SQL; at run time there is no loop left.
- **Q: How do you see the exact SQL the warehouse received?**
  Read the compiled file in `target/compiled/`.

**[[macros-packages|Macros & Packages]]**

- **Q: Where does a macro live and what does it return?**
  A `.sql` file in `macros/`; it returns a string of SQL at compile time.
- **Q: What does `dbt deps` do, and why pin a package version?**
  Downloads packages from `packages.yml` into `dbt_packages/`; pinning gives every install
  identical code (reproducibility).

**[[seeds|Seeds]]**

- **Q: What is a seed and how is it loaded?**
  A small static CSV in `seeds/`, loaded into the warehouse as a table by `dbt seed`.
- **Q: Seed or source for a 50-million-row clickstream table?**
  A **source** — it's large and machine-produced. Seeds are only for small, hand-maintained data.

**[[snapshots-scd-type-2|Snapshots & SCD Type 2]]**

- **Q: What does a `dbt_valid_to` of NULL mean?**
  That version is the current, active one — still true right now.
- **Q: What are the two snapshot strategies?**
  `timestamp` (trust an `updated_at` column) and `check` (compare a listed set of columns).

---

## Phase 4 — Quality & shipping

**[[tests|Tests]]**

- **Q: What does it mean when a dbt test returns more than 0 rows?**
  It **fails** — the returned rows are the bad records. 0 rows = pass.
- **Q: Generic vs singular test?**
  Generic = reusable one-line YAML check on a column (`unique`, `not_null`, `accepted_values`,
  `relationships`). Singular = a custom `.sql` file in `tests/` that selects bad rows.

**[[documentation-lineage|Documentation & Lineage]]**

- **Q: Which part of the docs do you write, and which is automatic?**
  You write the prose `description`s in YAML; dbt derives the column lists and lineage graph
  from your `ref()`/`source()` calls.
- **Q: Two commands to build and view the docs site?**
  `dbt docs generate`, then `dbt docs serve`.

**[[the-dbt-build-workflow|The dbt build Workflow]]**

- **Q: Why is `dbt build` safer than `dbt run` then `dbt test`?**
  `build` tests each node right after building it and skips downstream nodes on failure, so bad
  data never flows on. `run` builds everything first, testing too late.
- **Q: What does `state:modified+` select?**
  Models changed in your branch **plus everything downstream** — the basis of slim CI.

**[[deployment-environments-ci|Deployment, Environments & CI]]**

- **Q: What is the real deliverable when you "deploy" dbt?**
  The freshly built, tested tables in the prod warehouse — you *run* dbt on a schedule, you
  don't copy files to a server.
- **Q: Why must dev and prod use different schemas?**
  So unfinished dev work can never overwrite the trusted tables dashboards read.

---

## Going deeper

Once these come back instantly, use the other synthesized companions to connect them:
[[dbt-end-to-end-from-raw-to-reports|dbt End-to-End: From Raw Data to Reports]],
[[dbt-project-anatomy|dbt Project Anatomy]],
[[dbt-commands-run-build-test|dbt Commands: run vs build vs test]],
[[dbt-reuse-jinja-macros-packages|Reuse in dbt: Inline Jinja vs Macros vs Packages]], and
[[dbt-materializations-when-to-use-which|dbt Materializations — When to Use Which]].

---

## Sources

- [[what-dbt-is-the-t-in-elt|What dbt Is & the T in ELT]]
- [[dbt-projects-profiles-targets|dbt Projects, Profiles & Targets]]
- [[models-the-ref-function|Models & the ref() Function]]
- [[sources-the-source-function|Sources & the source() Function]]
- [[materializations|Materializations]]
- [[incremental-models|Incremental Models]]
- [[project-structure-staging-intermediate-marts|Project Structure: Staging, Intermediate & Marts]]
- [[jinja-templating-in-dbt|Jinja Templating in dbt]]
- [[macros-packages|Macros & Packages]]
- [[seeds|Seeds]]
- [[snapshots-scd-type-2|Snapshots & SCD Type 2]]
- [[tests|Tests]]
- [[documentation-lineage|Documentation & Lineage]]
- [[the-dbt-build-workflow|The dbt build Workflow]]
- [[deployment-environments-ci|Deployment, Environments & CI]]
