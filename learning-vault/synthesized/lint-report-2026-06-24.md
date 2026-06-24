---
title: "Vault Lint Report — 2026-06-24"
tags: [meta, lint]
---

# Vault Lint Report — 2026-06-24

*Up: [[synthesized-moc|Synthesized Notes]]*

Health check of the authored course in `learning-vault/`, produced by the `wiki-lint` check.

## Summary

| Check | Result |
|---|---|
| Pages scanned | 46 |
| 🔗 Dead links (a `[[link]]` whose target note doesn't exist) | **0** ✅ |
| 🏝️ Orphan notes (no inbound links) | **0** after wiring (was 1) |

The vault is clean: every wikilink resolves to a real note. The one orphan found in the
scan — `synthesized/dbt-materializations-when-to-use-which.md` — was the newly generated
synthesized note; it is now linked from [[synthesized-moc|Synthesized Notes]] and the
[[dbt-data-build-tool-moc|dbt roadmap]], so it is reachable.

## How links were checked

So the numbers are trustworthy, the scan resolves links exactly the way Obsidian does:

- Wikilinks are matched by **filename** (`[[materializations]]` → `materializations.md`),
  regardless of which folder the note lives in.
- **Code and `mermaid` blocks are ignored** — text inside fenced code isn't a real link.
- **Escaped table pipes** (`[[star-schema\|Star Schema]]`, common inside Markdown tables)
  are un-escaped before matching. *Note:* the first pass missed this and reported 21 false
  "dead links"; after the fix the true count is **0**.

## How to re-run

From the repo root (where the claude-obsidian skills are available):

```text
lint the wiki
```

…or run the standalone filename-resolution scan over `learning-vault/` that produced this
report. Re-run after adding a batch of new notes, or whenever the graph view shows a stray
disconnected node.
