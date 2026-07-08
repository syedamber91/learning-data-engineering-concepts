# Persona wikis (synthesized layer)

Incremental research-memory derivatives, one subtree per persona
(`<persona>/topics/`, `entities/`, `concepts/`, `index.yaml`, `log.md`).
Built by the `persona-wiki` CLI (`src/persona_wiki/`). This is synthesized
output — safe to regenerate. It never modifies the authored course.

- `persona-wiki bootstrap` — seed from `data/personas/<persona>.md`.
- `persona-wiki update` — fold new sources in (stdin: `id<TAB>text`).
- `persona-wiki query "<question>"` — route to the relevant notes.

## Smoke-run status (POC)

- `persona-wiki bootstrap --dry-run` — verified: parses all 23 `###` sections
  from `data/personas/vutr.md` (Airflow, Spark, Kafka, …). No LLM called.
- Unit suite — 49 tests pass, exercising the full pipeline (derive, CDC,
  QC gating, index, 4-shape log, query) with the LLM injected as a stub.
- Real `bootstrap`/`update`/`query` (which shell out to the `claude` CLI):
  **run these in a normal terminal.** They cannot be validated from inside a
  Claude Code session — a nested `claude -p` call returns HTTP 401 (the parent
  session's credentials are not inherited by the child process).

### Known limitation (follow-up)

`bootstrap` currently saves `index.yaml`/`log.md` only after all sections
finish, and does not catch a per-section LLM failure — so a single failed
`claude` call aborts the whole run and leaves no partial output. `update`
(the incremental path) already tolerates per-source failures. Making
`bootstrap` resilient (per-section try/except + incremental save) is the
first follow-up before running it over a full persona.
