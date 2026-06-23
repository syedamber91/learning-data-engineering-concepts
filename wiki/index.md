---
title: Wiki Index
tags: [moc, wiki, index]
---

# Wiki Index — Synthesized Knowledge Layer

This `wiki/` tree is the **claude-obsidian second-brain layer** for this repo. It is
*separate* from the authored course in `learning-vault/`:

- **`learning-vault/`** — the curated, generated data-engineering course (Home → Area MOCs
  → Topic MOCs → leveled concept lessons). Built by `de-toolkit`. The plugin **reads** it
  but does not modify it.
- **`wiki/`** — where the plugin **writes** new synthesized knowledge: saved conversations
  (`/save`), ingested sources (`ingest`), autoresearch output (`/autoresearch`), and the
  `hot.md` context cache. Organized in **LYT mode** (`wiki/mocs/`, `wiki/notes/`).

## Maps of Content
*(none yet — created as you `/save`, `ingest`, or `/autoresearch`)*

## How to use
- Ask **"what is X?"** → `wiki-query` answers from `learning-vault/` (the course) first,
  then this layer. See `CLAUDE.md` → "Wiki Knowledge Base".
- **`lint the wiki`** → health check (orphans, dead links).
- **`/save`** → file the current conversation here as an atomic note.
