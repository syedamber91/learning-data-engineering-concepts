"""Build an Obsidian vault of linked notes from the concept catalog.

This is the "connect to Obsidian" step: it turns ``data/content.json`` into a
folder of Markdown notes — one per concept — wired together with wikilinks,
Maps-of-Content (MOCs) and a ``Home.md`` entry point. Open the resulting folder
as a vault in Obsidian and the graph view shows how everything relates.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from rich.console import Console

from .config import CONTENT_PATH, resolve_vault_dir, settings
from .models import Catalog, Concept

console = Console()

# Common words filtered out before deriving tags / "Related" keywords.
_STOPWORDS = {
    "about", "above", "after", "again", "against", "because", "before", "being",
    "below", "between", "could", "doing", "during", "each", "from", "further",
    "have", "having", "into", "more", "most", "other", "over", "same", "should",
    "some", "such", "than", "that", "their", "them", "then", "there", "these",
    "they", "this", "those", "through", "under", "until", "very", "were", "what",
    "when", "where", "which", "while", "with", "would", "your", "data", "using",
}
_WORD_RE = re.compile(r"[a-z][a-z0-9]{3,}")


@dataclass
class Note:
    concept: Concept
    area_title: str
    topic_title: str
    basename: str                              # wikilink identifier (stem)
    rel_path: Path                             # path relative to the vault root
    keywords: Counter = field(default_factory=Counter)
    tags: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    prev: str | None = None
    next: str | None = None
    topic_moc: str = ""
    area_moc: str = ""


def slugify(text: str) -> str:
    """Turn arbitrary text into a safe, lowercase, hyphenated filename stem."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text or "untitled"


def _keywords(text: str) -> list[str]:
    """Extract candidate keywords (4+ char words, stopwords removed)."""
    return [w for w in _WORD_RE.findall(text.lower()) if w not in _STOPWORDS]


def _unique(basename: str, taken: set[str]) -> str:
    """Ensure a basename is unique by appending -2, -3, ... on collision."""
    if basename not in taken:
        taken.add(basename)
        return basename
    i = 2
    while f"{basename}-{i}" in taken:
        i += 1
    unique = f"{basename}-{i}"
    taken.add(unique)
    return unique


def _yaml_list(items: Iterable[str]) -> str:
    """Render a YAML inline list. Empty -> ``[]``."""
    items = [str(i) for i in items]
    if not items:
        return "[]"
    return "[" + ", ".join(items) + "]"


def _plan_notes(catalog: Catalog) -> list[Note]:
    """Build the full set of Note objects with paths, tags and links."""
    notes: list[Note] = []
    taken: set[str] = set()

    for area in catalog.areas:
        area_moc = _unique(slugify(area.title) + "-moc", taken)
        for topic in area.topics:
            topic_moc = _unique(slugify(topic.title) + "-moc", taken)
            topic_notes: list[Note] = []
            for concept in topic.concepts:
                basename = _unique(slugify(concept.title), taken)
                rel_path = (
                    Path(slugify(area.title))
                    / slugify(topic.title)
                    / f"{basename}.md"
                )
                blob = " ".join(
                    [concept.title, concept.body_text, *concept.key_points]
                )
                keywords = Counter(_keywords(blob))
                tags = [w for w, _ in keywords.most_common(settings.max_tags)]
                note = Note(
                    concept=concept,
                    area_title=area.title,
                    topic_title=topic.title,
                    basename=basename,
                    rel_path=rel_path,
                    keywords=keywords,
                    tags=tags,
                    topic_moc=topic_moc,
                    area_moc=area_moc,
                )
                topic_notes.append(note)
                notes.append(note)

            # Sequential prev/next navigation within the topic.
            for i, note in enumerate(topic_notes):
                if i > 0:
                    note.prev = topic_notes[i - 1].basename
                if i < len(topic_notes) - 1:
                    note.next = topic_notes[i + 1].basename

    _compute_related(notes)
    return notes


def _compute_related(notes: list[Note]) -> None:
    """Fill each note's ``related`` list by keyword-overlap scoring."""
    for note in notes:
        scores: list[tuple[int, str]] = []
        for other in notes:
            if other is note:
                continue
            shared = sum((note.keywords & other.keywords).values())
            if shared:
                scores.append((shared, other.basename))
        scores.sort(key=lambda s: (-s[0], s[1]))
        note.related = [name for _, name in scores[: settings.max_related]]


def _render_note(note: Note) -> str:
    """Render a single concept note as Obsidian-flavoured Markdown."""
    c = note.concept
    lines: list[str] = ["---"]
    lines.append(f'title: "{c.title}"')
    lines.append(f'area: "{note.area_title}"')
    lines.append(f'topic: "{note.topic_title}"')
    if c.source_url:
        lines.append(f"source_url: {c.source_url}")
    if c.updated_at:
        lines.append(f"updated_at: {c.updated_at.isoformat()}")
    lines.append(f"tags: {_yaml_list(note.tags)}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {c.title}")
    lines.append("")
    lines.append(
        f"*Part of [[{note.topic_moc}|{note.topic_title}]] · "
        f"[[{note.area_moc}|{note.area_title}]]*"
    )
    lines.append("")
    if c.source_url:
        lines.append(f"> Source: [Open reference]({c.source_url})")
        lines.append("")
    if c.body_text.strip():
        lines.append(c.body_text.strip())
        lines.append("")
    if c.key_points:
        lines.append("## Key points")
        lines.extend(f"- {kp}" for kp in c.key_points)
        lines.append("")
    if c.resource_links:
        lines.append("## Resources")
        lines.extend(f"- {link}" for link in c.resource_links)
        lines.append("")
    if note.related:
        lines.append("## Related")
        lines.extend(f"- [[{name}]]" for name in note.related)
        lines.append("")

    nav: list[str] = []
    if note.prev:
        nav.append(f"[[{note.prev}|← Previous]]")
    if note.next:
        nav.append(f"[[{note.next}|Next →]]")
    if nav:
        lines.append("---")
        lines.append(" · ".join(nav))
        lines.append("")

    return "\n".join(lines)


def _render_topic_moc(topic_title: str, area_moc: str, area_title: str,
                      notes: list[Note]) -> str:
    """Render a topic-level Map-of-Content."""
    lines = ["---", f'title: "{topic_title} (MOC)"', "tags: [moc]", "---", ""]
    lines.append(f"# {topic_title}")
    lines.append("")
    lines.append(f"*Up: [[{area_moc}|{area_title}]]*")
    lines.append("")
    lines.append("## Concepts")
    lines.extend(f"- [[{n.basename}|{n.concept.title}]]" for n in notes)
    lines.append("")
    return "\n".join(lines)


def _render_area_moc(area_title: str, topics: list[tuple[str, str]]) -> str:
    """Render an area-level Map-of-Content listing its topic MOCs."""
    lines = ["---", f'title: "{area_title} (MOC)"', "tags: [moc]", "---", ""]
    lines.append(f"# {area_title}")
    lines.append("")
    lines.append("*Up: [[Home]]*")
    lines.append("")
    lines.append("## Topics")
    lines.extend(f"- [[{moc}|{title}]]" for title, moc in topics)
    lines.append("")
    return "\n".join(lines)


def _render_home(areas: list[tuple[str, str]], catalog_title: str) -> str:
    """Render the ``Home.md`` entry point."""
    lines = ["---", f'title: "{catalog_title}"', "tags: [moc, home]", "---", ""]
    lines.append(f"# {catalog_title}")
    lines.append("")
    lines.append("Welcome to your data-engineering knowledge vault.")
    lines.append("")
    lines.append("## Areas")
    lines.extend(f"- [[{moc}|{title}]]" for title, moc in areas)
    lines.append("")
    lines.append(
        "> Tip: open the graph view (Ctrl/Cmd+G) to explore how concepts connect."
    )
    lines.append("")
    return "\n".join(lines)


def _write(path: Path, content: str) -> None:
    """Write ``content`` to ``path``, creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_vault(catalog: Catalog, vault_path: str | None = None) -> Path:
    """Build the whole Obsidian vault from an in-memory catalog.

    Returns the vault directory that was written.
    """
    vault_dir = resolve_vault_dir(vault_path)
    vault_dir.mkdir(parents=True, exist_ok=True)

    notes = _plan_notes(catalog)

    # 1) Concept notes.
    for note in notes:
        _write(vault_dir / note.rel_path, _render_note(note))

    # 2) Topic & area MOCs, tracked for the parent listings.
    area_entries: list[tuple[str, str]] = []
    for area in catalog.areas:
        topic_entries: list[tuple[str, str]] = []
        area_moc = ""
        for topic in area.topics:
            topic_notes = [
                n for n in notes
                if n.area_title == area.title and n.topic_title == topic.title
            ]
            if not topic_notes:
                continue
            topic_moc = topic_notes[0].topic_moc
            area_moc = topic_notes[0].area_moc
            _write(
                vault_dir / slugify(area.title) / f"{topic_moc}.md",
                _render_topic_moc(topic.title, area_moc, area.title, topic_notes),
            )
            topic_entries.append((topic.title, topic_moc))
        if not topic_entries:
            continue
        _write(
            vault_dir / f"{area_moc}.md",
            _render_area_moc(area.title, topic_entries),
        )
        area_entries.append((area.title, area_moc))

    # 3) Home.
    _write(vault_dir / "Home.md", _render_home(area_entries, catalog.title))

    console.print(
        f"[green]✓[/green] Wrote {len(notes)} concept notes to "
        f"[bold]{vault_dir}[/bold]"
    )
    console.print("Open that folder as a vault in Obsidian to explore it.")
    return vault_dir


def build_vault_from_disk(vault_path: str | None = None) -> Path:
    """Load ``data/content.json`` and build the vault from it."""
    if not CONTENT_PATH.exists():
        raise RuntimeError(
            f"No catalog found at {CONTENT_PATH}. Create it (see data/content.json) "
            "or run `de-toolkit init` to scaffold a sample."
        )
    raw = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    catalog = Catalog.model_validate(raw)
    return build_vault(catalog, vault_path=vault_path)
