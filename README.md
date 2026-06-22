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

## Configuration

Copy `.env.example` to `.env` to set a default vault path (`DE_VAULT_PATH`) and
tune `DE_MAX_TAGS` / `DE_MAX_RELATED`. The `vault/`, `output/` and your
generated `data/content.json` are gitignored so your notes stay local.

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
