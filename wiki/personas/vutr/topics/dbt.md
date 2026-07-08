---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: dbt
---

Related: [[star-schema]] · [[scd-type-2]] · [[surrogate-key]] · [[dimensional-modeling]] · [[etl-vs-elt]]

## Comparisons
A dbt model is a SQL+Jinja transformation script; a data model defines how data is structured and related (tool-agnostic). Writing dbt models is NOT itself data modeling — see [[dimensional-modeling]], [[etl-vs-elt]].

## Open questions
- Where does ETL still beat ELT once storage is cheap?

## Synthesis
dbt (a CLI that compiles SQL, not an engine or database) democratized transformation; paired with Kimball [[dimensional-modeling]] and [[star-schema]] it lets analysts own the T in ELT.
