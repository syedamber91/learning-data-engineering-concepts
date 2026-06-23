# WIKI.md — claude-obsidian wiring for this repo

This repo has the **claude-obsidian** PKM plugin wired in as a *complementary second-brain
layer*. This file is the short, repo-specific contract; the full upstream schema reference
is vendored at [`vendor/claude-obsidian/WIKI.md`](vendor/claude-obsidian/WIKI.md).

## Two layers — keep them distinct

| Layer | Path | Who writes it | Role |
|---|---|---|---|
| **Authored course** | `learning-vault/` | `de-toolkit` + human authors | The curated, generated data-engineering course. **Read-only** to the plugin. |
| **Synthesized wiki** | `wiki/` | the plugin (`/save`, `ingest`, `/autoresearch`) | New knowledge the plugin accumulates, which *references* the course. |

The plugin **reads** `learning-vault/` for context and **writes** only into `wiki/`. It
never regenerates or edits the authored lessons.

## Methodology mode: LYT

Set in `.vault-meta/mode.json`. New synthesized content routes LYT-style:
- Maps of Content → `wiki/mocs/<topic>-moc.md`
- Atomic notes → `wiki/notes/<slug>.md`

This mirrors the course's own MOC structure (`Home.md` → `*-moc.md` → concept notes).

## Vault conventions (shared by both layers)

Match what the authored course already uses (see
[`prompts/vault-teaching-engine.md`](prompts/vault-teaching-engine.md)):

- **YAML frontmatter** on every note: `title`, `area`, `topic`, `tags` (4–6 lowercase).
- **Wikilinks**: `[[slug|Display Text]]`.
- **Diagrams**: native ```mermaid``` blocks (render in Obsidian desktop + mobile).

## Safety

- `.vault-meta/auto-commit.disabled` is present → the plugin's auto-commit hook is **off**.
  Commits are always deliberate and human-reviewed.
- Vendored copy is pinned (`v1.9.2`); see [`vendor/claude-obsidian/NOTICE.md`](vendor/claude-obsidian/NOTICE.md).
