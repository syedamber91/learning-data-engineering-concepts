---
persona: vutr
kind: entity
sources:
- raw/dbt-and-dimensional-modeling/why-is-dbt-so-popular.md
- raw/dbt-and-dimensional-modeling/how-to-learn-dbt-cheap-and-fast.md
last_updated: '2026-07-15'
qc: passed
slug: dbt-origin-and-adoption
topics:
- dbt
---

dbt was created in 2016 by Tristan Handy while at RJMetrics, to address the pain of managing complex data transformation pipelines: it let analysts write modular SQL code, version-control it, and test it, aiming to make data workflows both more efficient and more reliable. Vu frames the deeper motivation as encouraging data analysts to take on more transformation responsibility by adopting software-engineering best practices — the same collaboration story told in [[democratization-of-transformation]].

Its adoption curve, as Vu tracks it from dbt Core's own GitHub star history: 3 companies in 2016 (launch year), 100 by 2017, 280 by 2018, still 280 in 2019 (steady rather than explosive growth), past 5,000 by 2021, and past 9,000 by 2022. McDonald's, Nasdaq, Discord, and Shopify are among the named adopters. His summary line: if your company transforms data with SQL, there's a high chance dbt is already somewhere in its stack — and by the time he was writing (2025/2026), he treats dbt as having proven itself "far more than hype," on its way to becoming a de facto transformation standard.

To explain *why* it specifically won rather than some other tool solving the same problem, Vu borrows the Unified Theory of Acceptance and Use of Technology (UTAUT) framework and applies its four factors directly to dbt:
- **Performance Expectancy** — dbt gives data analysts and engineers a real framework for unifying how SQL transformation logic is written, tested, and documented.
- **Effort Expectancy** — the barrier to entry is low: anyone already comfortable with SQL (which DE, DA, and DS all speak) needs roughly 30 minutes learning dbt's Jinja to build a first model; it installs with pip, and its simplicity makes containerizing a whole dbt project straightforward (running on Kubernetes via Airflow, or wiring CI/CD through a GitLab runner).
- **Social Influence** — growing adoption within the data community, plus endorsement from recognizable organizations, reinforces its perceived importance and nudges others toward adopting it too.
- **Facilitating Conditions** — the prerequisites are minimal: an IDE, a SQL-capable warehouse, and the willingness to write transformation SQL. No dedicated hardware, no storage capacity planning, no CPU/RAM estimation. Documentation and community support cover most of what a team needs to raise its standard of writing, testing, and documenting SQL, and dbt's integration surface has grown over time as more organizations adopted it, lowering the barrier further.

Vu credits one additional, structural factor beyond UTAUT: the emergence of the cloud data warehouse itself — see [[elt-vs-etl]] for the mechanism — is what made ELT-style, in-warehouse SQL transformation viable in the first place, and dbt is the tool that showed up right as that shift created a mass of SQL-capable people who suddenly needed a disciplined way to manage transformation logic. By his account, dbt is now among the most in-demand data engineering tools precisely because dbt, Airflow, and a cloud data warehouse alone are enough for a company to stand up a complete data analytics pipeline.

*See also: [[dbt]] · [[elt-vs-etl]] · [[democratization-of-transformation]] · [[dimensional-modeling]]*
