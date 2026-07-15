---
persona: vutr
kind: entity
sources:
- raw/data-engineering-career-roadmap-and-learning-philosophy-additional/9-software-engineering-skills-a-de.md
- raw/data-engineering-career-roadmap-and-learning-philosophy-additional/the-data-engineer-roadmap.md
last_updated: '2026-07-15'
qc: passed
slug: nine-software-engineering-skills-for-des
topics:
- data-engineering-career-roadmap-and-learning-philosophy
---

Vu opens "9 software engineering skills a DE should have" with a confession: for years he equated software engineering with "creating working code" and nothing more. His corrected definition — "the discipline of building systems that keep working. Even when requirements change, when bugs arise, and when the guy who originally created them has left the company" — reframes the nine skills that follow not as a checklist but as answers to that single reliability question.

The nine, each paired with his own "how to learn it" prescription:
1. **Writing understandable code** — expressing logic so another engineer (or future-you) can modify it without a day of reverse-engineering; learned via two-sided code review and reading/contributing to well-organized open-source projects.
2. **Version control** — explicitly broader than Git: "if something changes and it could break production, it should be tracked," extending the discipline to config files, Docker image registries, and shared documents, not just source code (see [[git-mental-model-for-data-engineers]] for the Git-specific mechanics).
3. **Environment separation** (dev/staging/production) — mitigates risk and, in his telling, makes engineers *braver* about changes rather than merely safer; the harder 60% of the skill is cost management (three environments ≠ 3x cost), configuration sync, and representative-but-safe test data via profiling and sampling rather than copying production wholesale.
4. **APIs** — both consuming third-party endpoints (pagination, rate limits, back-off retry, error handling) and exposing data via frameworks like FastAPI; motivated by his own experience at a company where 70% of data lived behind third-party APIs rather than an OLTP database.
5. **Testing** — layered as unit tests (transformation logic), integration tests (the whole pipeline), and data quality tests (nullability, uniqueness, referential constraints); his key reframe is that tests don't slow you down, they let you go faster *by making things safer*.
6. **CI/CD** — Continuous Integration triggers checks (test/lint/build) on every change; Continuous Deployment then automates the deploy once checks pass; the full data-engineer flow he describes is a dbt model change → PR → automated tests → review → merge → staged then production deploy.
7. **Observability** — the three pillars (logging, metrics, alerts), with an explicit warning that over-alerting breeds complacency: alerts need calibrated severity tied to downstream impact (a non-critical job failure is a Slack message; a primary key with 20% nulls in a revenue table is a multi-departmental page).
8. **Debugging (investigating)** — deliberately kept as its own section rather than folded into observability, because "observability is more about tools to support that process" while debugging is "finding, understanding, and fixing failures"; for data-specific bugs he recommends working backward along the data lineage.
9. **Dependency management and containerization** — from Python virtual environments and lockfiles (`venv`, `uv`) up to Docker, which "doesn't just lock your Python packages; it freezes the entire runtime environment," so a pipeline behaves identically on laptop, CI, staging, and production.

The-data-engineer-roadmap situates a subset of this list (Git, testing, Docker, CI/CD, Kubernetes-optional) as the "software engineering" stage of the broader learning order, positioned deliberately *after* data modeling/SQL/Python/OLAP/dbt/formats/processing/orchestration and *before* Kafka/Flink/AI — see [[recommended-learning-order-2026]].

*See also: [[git-mental-model-for-data-engineers]] · [[recommended-learning-order-2026]] · [[fundamentals-over-tools]] · [[simplicity-over-complexity-in-pipeline-design]]*
