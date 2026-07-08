# Persona wikis — usage guide

Incremental research-memory derivatives, one subtree per persona
(`<persona>/topics/`, `entities/`, `concepts/`, `index.yaml`, `log.md`), built by
the `persona-wiki` CLI (`src/persona_wiki/`). This is synthesized output — safe to
regenerate. It never modifies the authored course. The `vutr` wiki currently holds
22 topics (~150 entities, ~55 concepts) as one connected graph.

## Setup (once per machine)

Run from the repo root, in a **normal terminal** (not inside a Claude Code
session — a nested `claude` call returns HTTP 401), with a venv **outside iCloud**
(iCloud eviction breaks editable installs):

```bash
cd "<repo root>"                       # this repo's root (the iCloud vault folder)
python3 -m venv /tmp/pw-venv
/tmp/pw-venv/bin/pip install -e ".[dev]"
alias pw='/tmp/pw-venv/bin/persona-wiki'
```

Output lands in `wiki/personas/<persona>/`, which is inside your Obsidian vault.

## The three commands

| Command | What it does |
|---|---|
| `pw bootstrap --persona <p> --vault-dir "$PWD"` | One-time seed from `data/personas/<p>.md`. Re-derives every section — use once per persona. |
| `pw update --persona <p> --vault-dir "$PWD"` | Fold new sources in. Reads stdin, one `id<TAB>text` per line. Incremental: skips already-ingested sources, QC-gates, cross-links. |
| `pw query "<question>" --persona <p> --vault-dir "$PWD"` | Route a question to the relevant topic note + its linked entities/concepts. |

## Common workflows

**Read / use the knowledge**
- Obsidian: browse `wiki/personas/<persona>/`, use graph view, follow `[[links]]`.
- Terminal: `pw query "how does kafka get exactly-once?"`.
- As agent memory: point an assistant at `<persona>/index.yaml` first, then let it
  open only the notes it needs.

**Grow a persona with a new post** (stdin is `id<TAB>text`)
```bash
printf 'substack/vutr/kafka-tiered-storage\t<paste the post text>\n' \
  | pw update --persona vutr --vault-dir "$PWD"
```

**Add a new persona** — create `data/personas/<name>.md` with a
`## TECHNICAL POSITIONS` section of `### Topic Title` subsections (mirror
`data/personas/vutr.md`), then `pw bootstrap --persona <name> --vault-dir "$PWD"`.

After any build: commit + push, then on other devices `git pull` and **fully
reload Obsidian** so it reindexes the graph.

## Topic routing (`src/persona_wiki/topics.py`)

`update` routes a source by matching a small keyword vocabulary (`VUTR_TOPICS`)
against its text and filing it under every matching topic slug. The vocabulary now
covers all 22 current `vutr` topics (kafka, spark, airflow, dbt, iceberg/table
formats, parquet, flink, S3/GFS/HDFS, Arrow, Pinot/Druid, CDC, data architecture,
career, pipeline design, history, LLMs/vector DBs, LSM-trees, OLAP engines,
single-node engines, SQL fundamentals, storage models). A source about a topic
**not** in the vocabulary is silently skipped — add the slug + distinctive aliases
to `VUTR_TOPICS` before ingesting new subject areas. Keep aliases specific; generic
words (`data`, bare `log`, bare `sql`) over-match.

## Invariants & known limitation

- The canonical tree only ever holds QC-passed notes; a failing bundle goes to
  `_rejected/` (with `qc: failed` + reason) and never overwrites a good note.
- A source already recorded in a topic note is skipped on re-run.
- `bootstrap` groups sections sharing a topic slug, runs each under its own error
  boundary, and saves the index after each — one failed `claude` call can't abort
  the run or clobber a sibling.
- Every atomic note carries a `*See also: …*` footer linking topic-siblings, so the
  graph renders as connected clusters rather than single-edge dust. Vendor/support
  files are excluded from the Obsidian graph via `.obsidian/app.json`.

Known limitation (follow-up): when a shared entity/concept is re-derived from a
second topic, its frontmatter back-refs are unioned but its *body* is replaced with
the latest derivation, not LLM-merged across topics.
