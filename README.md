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
into beginner-proof lessons. It is a reusable prompt that teaches the vault's
data-engineering and software-engineering concepts **topic-by-topic and
sub-topic-by-sub-topic**, pitched so a 15-year-old can follow, with an everyday
analogy and a real-world example for every idea.

- Prompt: [`prompts/vault-teaching-engine.md`](prompts/vault-teaching-engine.md)
- It uses a five-lens teaching panel (Master Teacher, Working Engineer, Honest
  Skeptic, Curriculum Architect, and a 15-Year-Old comprehension gate), produces a
  learning **roadmap first**, then one lesson file per topic.
- Lessons come out as the same Markdown + frontmatter + `[[wikilink]]` format this
  toolkit produces, so they paste straight back into your Obsidian vault.

### The ready-made learning vault

The repo ships a ready-to-open vault at **`learning-vault/`** — one deep lesson per
concept in the starter syllabus. Every lesson includes a worked example with real
numbers and a code/SQL snippet, common misconceptions, a "how it relates to and
differs from" comparison with neighbouring concepts, and self-check questions —
wired together with wikilinks and Maps-of-Content. Open
that folder directly in Obsidian (*Open folder as vault*) and start at `Home.md`.

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
