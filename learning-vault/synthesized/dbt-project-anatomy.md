---
title: "dbt Project Anatomy: Files, Folders & Naming"
area: "Data Pipelines"
topic: "dbt (Data Build Tool)"
tags: [dbt, project-structure, configuration, naming, reference]
---

# dbt Project Anatomy: Files, Folders & Naming

*Part of [[dbt-data-build-tool-moc|dbt (Data Build Tool)]] · [[data-pipelines-moc|Data Pipelines]]*

*Synthesized companion · see [[synthesized-moc|Synthesized Notes]]*

---

A one-page reference for *where everything lives* in a dbt project: the two config files, the
standard folders, and the naming conventions that let you read a project at a glance. It pulls
together details scattered across the foundations, structure, and reuse lessons.

---

## The two config files

dbt is configured by two files that do very different jobs and live in different places:

| File | Role | Controls | Where it lives | In git? |
|---|---|---|---|---|
| `dbt_project.yml` | the **blueprint** | project name, version, folder paths, default materializations | inside the project | **yes** |
| `profiles.yml` | the **keychain** | warehouse connection: type, host, user, password, dbname, schema | outside the repo, at `~/.dbt/` | **no** |

The split exists for **security**: the blueprint is safe to share, but the keychain holds
secrets, and git keeps history forever — so a committed password stays leaked. Connection
details and passwords go in `profiles.yml`, with the password itself pulled from an
environment variable (`{{ env_var('DBT_PASSWORD') }}`) rather than written in plain text.
([[dbt-projects-profiles-targets|dbt Projects, Profiles & Targets]])

A **target** is one named connection block inside `profiles.yml` (like `dev` or `prod`). You
switch between them with `--target`; the same SQL then writes to a different schema.
([[dbt-projects-profiles-targets|dbt Projects, Profiles & Targets]], [[deployment-environments-ci|Deployment, Environments & CI]])

```yaml
# dbt_project.yml — committed
name: 'jaffle_shop'
version: '1.0.0'
profile: 'jaffle_shop'      # must match a profile name in profiles.yml

models:
  jaffle_shop:
    staging:
      +materialized: view
    marts:
      +materialized: table
```

The `profile:` value in the blueprint must exactly match a profile name in `profiles.yml`, or
dbt errors out. Run `dbt debug` to check the connection before building anything.

---

## The standard folders

`dbt init` scaffolds these folders; each has one job:

| Folder | Holds | Loaded / built by |
|---|---|---|
| `models/` | your SQL `SELECT` transformations | `dbt run` / `dbt build` |
| `seeds/` | small static CSV lookup tables | `dbt seed` |
| `snapshots/` | SCD Type 2 history definitions | `dbt snapshot` |
| `tests/` | singular (custom `.sql`) data tests | `dbt test` / `dbt build` |
| `macros/` | reusable Jinja functions | (compiled into models) |
| `analyses/` | one-off queries, compiled but not run | `dbt compile` |

Two more folders are generated, not authored: `target/` (compiled SQL — read
`target/compiled/` to debug Jinja) and `dbt_packages/` (installed packages, filled by
`dbt deps`). ([[dbt-projects-profiles-targets|dbt Projects, Profiles & Targets]], [[jinja-templating-in-dbt|Jinja Templating in dbt]], [[macros-packages|Macros & Packages]])

---

## The naming convention that makes a project readable

Inside `models/`, the convention is three layers, each with a prefix that tells you a model's
job instantly. This is what keeps a 300-model project navigable.
([[project-structure-staging-intermediate-marts|Project Structure: Staging, Intermediate & Marts]])

| Prefix | Layer | Purpose | Typical materialization | 1:1 with a source? |
|---|---|---|---|---|
| `stg_` | staging | clean one raw source — rename, cast, standardise | view | yes |
| `int_` | intermediate | reusable logic shared by several marts | ephemeral / view | no |
| `fct_` | marts (fact) | business events, one row per event | table | no |
| `dim_` | marts (dimension) | descriptive entities (customers, products) | table | no |

A typical layout:

```bash
models/
├── staging/
│   └── jaffle_shop/
│       ├── stg_orders.sql        # view, 1:1 with raw orders
│       └── stg_customers.sql     # view, 1:1 with raw customers
├── intermediate/
│   └── int_orders_joined.sql     # ephemeral, shared join
└── marts/
    └── core/
        ├── fct_orders.sql        # table, one row per order
        └── dim_customers.sql     # table, one row per customer
```

You set the materialization once per folder in `dbt_project.yml` (see above), not on every
file — though any individual model can override the folder default with a `config()` block.

---

## YAML files you'll write alongside models

dbt models are paired with YAML that adds metadata. The same `.yml` files commonly carry
several concerns at once:

- **`_sources.yml`** — declares raw tables as sources, with optional freshness thresholds.
  ([[sources-the-source-function|Sources & the source() Function]])
- **`schema.yml`** — model and column `description`s (for docs) and `tests` (`unique`,
  `not_null`, `relationships`, `accepted_values`). ([[documentation-lineage|Documentation & Lineage]], [[tests|Tests]])
- **`packages.yml`** — third-party packages (e.g. `dbt-labs/dbt_utils`) with **pinned**
  versions, installed by `dbt deps`. ([[macros-packages|Macros & Packages]])

---

## Quick mental model

> **`dbt_project.yml`** = what to build (in git). **`profiles.yml`** = where to connect
> (never in git). **Folders** = one per kind of thing dbt builds. **Prefixes**
> (`stg_/int_/fct_/dim_`) = a model's layer and job at a glance.

---

## Sources

- [[dbt-projects-profiles-targets|dbt Projects, Profiles & Targets]]
- [[project-structure-staging-intermediate-marts|Project Structure: Staging, Intermediate & Marts]]
- [[macros-packages|Macros & Packages]]
- [[seeds|Seeds]]
- [[snapshots-scd-type-2|Snapshots & SCD Type 2]]
- [[tests|Tests]]
- [[sources-the-source-function|Sources & the source() Function]]
- [[documentation-lineage|Documentation & Lineage]]
- [[jinja-templating-in-dbt|Jinja Templating in dbt]]
