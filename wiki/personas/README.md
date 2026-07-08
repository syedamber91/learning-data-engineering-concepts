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

### Invariants & known limitation

- The canonical tree (`topics/`, `entities/`, `concepts/`) only ever holds
  QC-passed notes. A bundle that fails QC is written under `_rejected/`
  (with `qc: failed` + reason) and never overwrites a good note.
- A source already recorded in a topic note is skipped on re-run — no repeat
  LLM call, no rewrite.
- `bootstrap` groups sections that share a topic slug, processes each group
  under its own error boundary, and saves the index after every group, so one
  failed `claude` call can't abort the run or clobber a sibling section.

Known limitation (follow-up): when a shared entity/concept is re-derived from a
second topic, its note *frontmatter* back-refs are unioned correctly, but its
*body* is replaced with the latest derivation rather than LLM-merged across
topics. Merging atomic bodies needs a dedicated LLM merge step.
