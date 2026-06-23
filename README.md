# learning-data-engineering-concepts

A small toolkit that turns your data-engineering study notes into a linked
**Obsidian vault** — one Markdown note per concept, wired together with
wikilinks, Maps-of-Content (MOCs) and a `Home.md` entry point, so the Obsidian
graph view shows how everything connects.

The Obsidian-vault connection mirrors the approach used in
[knowledge-toolkit](https://github.com/syedamber91/knowledge-toolkit): notes are
written as plain Markdown with YAML frontmatter into a `vault/` folder (or
straight into your real vault via `--vault-path`) that you open directly in
Obsidian.

## How it connects to Obsidian

There is no plugin or API — "connecting" means writing a folder of Markdown
notes that Obsidian opens natively as a vault:

- **YAML frontmatter** on every note: `title`, `area`, `topic`, `source_url`,
  `tags`.
- **Structural wikilinks**: each concept links up to its Topic MOC → Area MOC →
  `Home.md`, and the MOCs link back down.
- **Sequential navigation**: prev/next links across concepts within a topic.
- **Content-based links**: a "Related" section surfaces concepts that share
  keywords, and derived `tags` cluster topics in the graph view.

## Install

```bash
pip install -e .
```

## Usage

```bash
# 1. Scaffold a starter data/content.json (sample concepts)
de-toolkit init

# 2. Build the vault under ./vault
de-toolkit build-vault

# …or write straight into your real Obsidian vault
de-toolkit build-vault --vault-path ~/Obsidian/DataEngineering

# Show where the catalog and vault live
de-toolkit status
```

Then open the target folder in Obsidian (*Open folder as vault*) and turn on the
graph view (Ctrl/Cmd+G).

## Learning from the vault

Building the vault gives you notes; the **Vault Teaching Engine** turns those notes
into one **flowing, illustrated course**. It is a reusable prompt that teaches the
vault's data-engineering and software-engineering concepts as a connected path —
each lesson recaps the previous one and points to the next — pitched so a 15-year-old
can follow.

- Prompt: [`prompts/vault-teaching-engine.md`](prompts/vault-teaching-engine.md)
- Each lesson climbs a **ladder of levels** — Level 1 (first intuition) up to an
  expert level (more levels for harder concepts) — so you can stop where you like or
  push to mastery.
- It uses a teaching panel plus an **editorial board** (a prolific author, a
  voracious expert reader, and a professor who teaches rocket science to teenagers)
  that reviews every note for accuracy, flow, and clarity.
- Every lesson carries several **simple diagrams** (ByteByteGo-style boxes-and-arrows)
  rendered to real SVG images from Mermaid, so flow is *seen*, not just read.
- Lessons come out as the same Markdown + frontmatter + `[[wikilink]]` format this
  toolkit produces, so they save straight into your Obsidian vault.

### The ready-made learning vault

The repo ships a ready-to-open vault at **`learning-vault/`** — the starter syllabus
taught as one continuous course. Each concept is a leveled lesson with a recap that
bridges from the previous concept, several embedded diagrams (in `assets/`), a worked
example with real numbers and a code/SQL snippet, common misconceptions, a "how it
relates to and differs from" comparison, self-check questions, and a "coming up next"
pointer — wired together with wikilinks and Maps-of-Content. Open that folder directly
in Obsidian (*Open folder as vault*) and start at `Home.md`.

> **Diagram rendering.** `de-toolkit teach` renders each lesson's Mermaid diagrams to
> SVG using a local `mermaid-cli` (installed under `.toolcache/`, which is
> git-ignored). If that renderer isn't available, lessons keep native ` ```mermaid `
> blocks instead — Obsidian still renders those on desktop and mobile.

### Generating more lessons with `de-toolkit teach`

`de-toolkit teach` expands any concept in `data/content.json` into a full lesson
using your **Claude Code subscription** — it shells out to the local `claude` CLI,
so no API key is required (you just need Claude Code installed and logged in).

```bash
# Preview the exact prompt for one concept without calling Claude
de-toolkit teach --dry-run --concept "Indexing"

# Generate one lesson into ./learning-vault
de-toolkit teach --concept "Indexing"

# Generate a whole area, plus a roadmap/Home note
de-toolkit teach --area "Databases" --roadmap

# Generate every concept into a custom vault folder
de-toolkit teach --vault-path ~/Obsidian/Learning
```

Filters (`--area`, `--topic`, `--concept`) are optional and case-insensitive; with
none, every concept is generated. Use `--model` to pick the Claude model.

## PKM second-brain skills (claude-obsidian)

The repo ships with the **[claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)**
PKM plugin (MIT, pinned `v1.9.2`) vendored at `vendor/claude-obsidian/` and registered via
`.claude/settings.json`. It adds a *complementary second-brain layer* on top of the course:
when you run Claude Code from the repo root, skills/commands like `/wiki`, `/save`,
`/autoresearch`, `wiki-query`, and `wiki-lint` become available.

How the two layers relate (full contract in [`WIKI.md`](WIKI.md) and [`CLAUDE.md`](CLAUDE.md)):

- **`learning-vault/`** — the authored course. The plugin **reads** it for context but never
  edits it.
- **`wiki/`** — where the plugin **writes** synthesized knowledge (`/save` conversations,
  ingested sources, `/autoresearch` output) in **LYT mode** (`wiki/mocs/`, `wiki/notes/`),
  cross-referencing the course.

Useful from the repo root:

```text
what is dbt incremental materialization?   # wiki-query: answers from learning-vault/
lint the wiki                              # wiki-lint: orphans + dead links
/save                                      # file the current conversation into wiki/
/autoresearch <topic>                      # autonomous research loop → wiki/
```

> **Headless vs. local Obsidian.** The file-based skills (`wiki-query`, `wiki-lint`,
> `autoresearch`, `save`) work anywhere. The `wiki-cli` transport, hybrid retrieval
> (`vendor/claude-obsidian/bin/setup-retrieve.sh`), and the `canvas` layer need a running
> Obsidian on your machine and degrade gracefully without it. Auto-commit is **disabled**
> (`.vault-meta/auto-commit.disabled`) — commits stay deliberate.
>
> Prefer to install it yourself instead of using the vendored copy? On a machine where
> Obsidian runs: `/plugin marketplace add AgriciDaniel/claude-obsidian` then
> `/plugin install claude-obsidian@agricidaniel-claude-obsidian`.

## Configuration

Copy `.env.example` to `.env` to set a default vault path (`DE_VAULT_PATH`) and
tune `DE_MAX_TAGS` / `DE_MAX_RELATED`. The `build-vault` render (`vault/`) and
scratch `output/` stay local (gitignored), while the curated `data/content.json`
syllabus and the authored `learning-vault/` are committed.

## Content format

`data/content.json` is a `Catalog` of `Area → Topic → Concept`:

```json
{
  "title": "Data Engineering Concepts",
  "areas": [
    {
      "title": "Pipelines",
      "topics": [
        {
          "title": "Processing Paradigms",
          "concepts": [
            {
              "title": "Batch vs Streaming",
              "body_text": "Batch handles bounded data; streaming is continuous.",
              "key_points": ["Batch favours throughput", "Streaming favours latency"],
              "source_url": "https://example.com"
            }
          ]
        }
      ]
    }
  ]
}
```

## Development

```bash
pip install -e ".[dev]"
pytest
```
