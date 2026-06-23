# CLAUDE.md

Guidance for Claude Code when working in this repo.

## What this repo is

Two things in one repository:

1. **`de-toolkit`** (`src/de_toolkit/`) — a Python CLI that turns a curated syllabus
   (`data/content.json`) into a linked **Obsidian vault** of leveled lessons. Entry points:
   `de-toolkit init | build-vault | teach | status` (see `src/de_toolkit/cli.py`).
   `teach.py` shells out to the local `claude` CLI to generate lessons (no API key needed).
2. **`learning-vault/`** — the authored, generated data-engineering course that ships in the
   repo. Structure: `Home.md` → Area MOCs (`*-moc.md`) → Topic MOCs → leveled concept notes.

### Vault conventions (authoritative: `prompts/vault-teaching-engine.md`)
- YAML frontmatter on every note: `title`, `area`, `topic`, `tags` (4–6 lowercase).
- Wikilinks `[[slug|Display Text]]`; each concept links up to its Topic MOC → Area MOC →
  `Home.md`, with prev/next sequential links and a "Connects To" / "Coming Up Next" section.
- Diagrams are native ```mermaid``` blocks (render in Obsidian desktop + mobile).
- **Do not hand-edit generated lessons to "fix" structure** — change the syllabus or the
  teaching prompt and regenerate.

## PKM second-brain layer (claude-obsidian plugin)

The **claude-obsidian** plugin is vendored at `vendor/claude-obsidian/` (pinned `v1.9.2`)
and registered via `.claude/settings.json`. It adds skills/commands like `/wiki`, `/save`,
`/autoresearch`, `/canvas`, `wiki-query`, and `wiki-lint`. See `WIKI.md` for the wiring.

It runs as a **complementary layer**, not a replacement:
- It **reads** `learning-vault/` (the course) for context.
- It **writes** synthesized notes only into `wiki/` (LYT mode: `wiki/mocs/`, `wiki/notes/`).
- It must **never** modify `learning-vault/`, `data/content.json`, or `src/de_toolkit/`.

### Wiki Knowledge Base (read order)

When a `wiki-*` skill needs knowledge, the **authored vault is `learning-vault/`**. Read in
this order and stop as soon as you have enough:

1. `wiki/hot.md` — recent-context cache.
2. `wiki/index.md` — the synthesized layer's catalog.
3. **`learning-vault/`** — the authored course. Start at `learning-vault/Home.md`, follow
   the relevant Area/Topic MOC, then drill into concept notes (e.g. dbt lives under
   `learning-vault/data-pipelines/dbt-data-build-tool/`). This is the primary source of
   truth for data-engineering questions.
4. Other `wiki/` notes only if the above is insufficient.

Do **not** consult the wiki for general coding tasks unrelated to the course material.

### Environment caveats (this matters)

This repo is often worked on **headless** (no running Obsidian app):
- **Works headless** — the filesystem-floor skills: `wiki-query`, `wiki-lint`,
  `autoresearch`, `wiki-ingest`, `save`, `think`. They use plain `Read`/`Glob`/`Grep`.
- **Needs a running Obsidian (or extra setup) on your own machine** — the `wiki-cli`
  transport (Obsidian Local REST API), hybrid retrieval (BM25/rerank via
  `vendor/claude-obsidian/bin/setup-retrieve.sh`), advisory locking, and the `canvas`
  visual layer. These degrade gracefully (skills fall back to the filesystem floor).

### Safety
- `.vault-meta/auto-commit.disabled` keeps the plugin's auto-commit hook **off**. Only
  commit when a human asks. Develop on the feature branch
  `claude/obsidian-vault-connect-w7tbq7`; never push elsewhere without permission.
