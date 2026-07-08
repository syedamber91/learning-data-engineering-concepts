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
   the relevant Area/Topic MOC, then drill into concept notes. This is a primary source of
   truth for data-engineering questions. (Note: the dbt course topic and the `synthesized/`
   folder were removed on purpose — dbt knowledge now lives in the persona wiki at
   `wiki/personas/vutr/topics/dbt.md`; see the Persona Wiki section below.)
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

## Persona Wiki (`src/persona_wiki/`)

An incremental "LLM wiki" that turns a persona snapshot (`data/personas/<persona>.md`)
into research-memory derivatives — atomic entity/concept notes + topic notes, cross-linked,
under `wiki/personas/<persona>/`. CLI: `persona-wiki bootstrap | update | query`. Design +
plan live in the sibling `knowledge-toolkit` repo under `docs/superpowers/`. Tests:
`tests/persona_wiki/` (offline; the LLM is an injected `Callable[[str], str]` seam). The
`vutr` wiki is built: 22 topics / ~150 entities / ~55 concepts, one connected graph.

### Hard-won lessons — READ BEFORE touching persona-wiki or rebuilding a vault

These are real failures from building this feature. Do not relearn them the hard way.

1. **Never write `f"{kind}s"` for atomic dirs.** `"entity" + "s"` = `"entitys"`, not
   `"entities"`. This bug shipped once (caught in code review) and was *reintroduced* in a
   later maintenance script. Always use `persona_wiki.index.atomic_dir(kind)`.

2. **Parallel derivation with sealed vocabularies destroys the graph.** The whole point of
   the "LLM wiki" is an *interlinked* graph. If you generate topics in parallel and tell each
   writer "only reference slugs you defined," you get N disconnected star-clusters (the
   article's V1/V2 failure mode). Cross-links must be designed in: `build_derive_prompt` /
   `build_bootstrap_prompt` take `known_slugs` (the existing index registry) and instruct the
   model to REUSE existing slugs and reference them across topics. `bootstrap`/`update` thread
   this from the live index. Prefer *sequential* derivation so each topic sees prior slugs; if
   you must fan out in parallel, run an explicit connectivity pass afterward.

3. **"0 unresolved wikilinks" is NOT a connectivity metric.** A vault of perfect islands
   passes an integrity check. Verify the graph with union-find over shared atomics +
   topic→topic links and assert a small cluster count (ideally 1). Islands are the failure.

4. **QC (grounding) ≠ coverage.** `qc_check` verifies no claim overreaches its source; it does
   NOT verify the derivation *kept* everything important. Parallel writers tend to drop
   origin/history facts and hard numbers in favor of mechanisms. Run a separate coverage audit
   (source vs bundle: "what significant fact is missing?") and gap-fill. Also note: QC
   hard-gates the `update` path but NOT `bootstrap` (the persona snapshot is treated as
   trusted) — a known gap, not a bug.

5. **The pipeline rolls back the index, not the filesystem — respect the seam.** Candidate
   notes are QC'd in memory (`render_bundle`) and only written canonical on pass; rejects go to
   `_rejected/`. Never make a mutating maintenance script that writes canonical before it
   validates.

6. **Restore from a committed state before re-running a mutating script.** A mid-loop crash
   leaves a half-applied state (files deleted, index unsaved, refs unrewritten). `git checkout
   -- wiki/personas/<persona> && git clean -f …` first, then re-run. Make such scripts
   idempotent.

7. **`bootstrap` groups sections by topic slug.** Two persona sections mapping to the same
   slug (e.g. two dbt sections) are *merged*, not clobbered — do not "fix" this by
   disambiguating slugs.

### Environment gotchas (cost real time this build)

- **Nested `claude -p` returns HTTP 401.** The default LLM shells out to the `claude` CLI,
  which cannot authenticate when invoked *inside* a Claude Code session (parent creds are not
  inherited). To generate real derivatives from a session, use the Agent tool as the LLM
  transport (or run `persona-wiki bootstrap` in a plain terminal). Tests never call it — the
  seam is stubbed.
- **Put the venv OUTSIDE iCloud.** This repo lives under iCloud; an editable install into a
  `.venv` *inside* the iCloud tree flickers off `sys.path` when iCloud evicts files. Create the
  venv elsewhere (e.g. `/tmp`) and `pip install -e ".[dev]"` from there.
- **Git worktrees are invisible to Obsidian.** Building into `.worktrees/<name>/wiki/...` means
  Obsidian never shows it — Obsidian ignores any dotfolder. Build/merge into the repo's real
  working tree (the `main` checkout) so the vault appears in the app.
- **A fast-forward merge aborts if the target working tree has uncommitted changes** to files
  the merge touches (this repo's `main` carries pre-existing vendor mode-bit noise). `git stash`
  them (recoverable), FF, then leave the stash for the human — don't discard.
