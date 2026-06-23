# Vendored: claude-obsidian

This directory is a **vendored, pinned copy** of a third-party Claude Code plugin.

| | |
|---|---|
| **Project** | claude-obsidian — a self-organizing AI second brain for Obsidian + Claude Code |
| **Upstream** | https://github.com/AgriciDaniel/claude-obsidian |
| **Pinned release** | `v1.9.2` |
| **Pinned commit** | `00213b720cdc9bb00ec8b3f88f9cc408721c37f9` |
| **License** | MIT (see `LICENSE`) — © 2026 AgriciDaniel (AI Marketing Hub) |
| **Vendored on** | 2026-06-23 |

## Why it is vendored (not installed from a marketplace)

`git clone github.com` is blocked by this environment's egress policy, and a committed,
pinned copy is reproducible and reviewable. The plugin is registered for this repo via
`/.claude/settings.json` (a local directory marketplace).

## Local modifications vs. upstream

**None to the plugin's skills, agents, commands, hooks, or scripts** — this is an
unmodified `v1.9.2` snapshot, so it stays safe to update by re-vendoring a newer tag.

The only behavioral change is made *outside* this directory, in the repo root, and is a
mechanism the plugin itself supports:

- `/.vault-meta/auto-commit.disabled` is present, which the plugin's `PostToolUse` hook
  honors as a kill switch — so the plugin never auto-commits to git in this repo.
- `/.vault-meta/mode.json` selects **LYT** methodology mode (MOC-driven), matching the
  existing `learning-vault/` structure.

## What was stripped from the upstream snapshot

The upstream repo doubles as a demo Obsidian vault. The demo/sample content was **not**
vendored: its seeded `wiki/`, `.raw/`, `.obsidian/`, `.vault-meta/`, `assets/`, `tests/`,
and editor-specific dirs (`.cursor/`, `.windsurf/`, `.github/`). Only the plugin and its
operational assets are kept here. See the repo-root `WIKI.md` and `CLAUDE.md` for how this
plugin is wired into this project.
