"""Turn a DerivativeBundle into atomic entity/concept notes plus a topic note.

Rendering (pure, no I/O) is separated from writing so the pipeline can QC the
candidate notes in memory and only commit them once they pass — the canonical
tree therefore only ever holds QC-passed notes. Shared atomic notes are merged
(their ``topics``/``sources`` back-refs are unioned) rather than overwritten,
and every slug is normalized so wikilinks always resolve to a file.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from .index import atomic_dir, register_atomic, register_topic
from .models import DerivativeBundle, NoteFrontmatter, WikiIndex
from .storage import parse_note, slugify, write_note


@dataclass
class RenderedNote:
    """A candidate note held in memory before it is committed to disk."""

    rel_path: str
    fm: NoteFrontmatter
    body: str
    kind: str          # "entity" | "concept" | "topic"
    key: str           # slug (atomic) or topic slug
    proc_topic: str    # the topic this bundle is being derived for


def _union(existing: List[str], incoming: List[str]) -> List[str]:
    """Order-preserving union — keep prior entries, append new ones once."""
    out = list(existing)
    for item in incoming:
        if item not in out:
            out.append(item)
    return out


def render_topic_body(bundle: DerivativeBundle) -> str:
    refs = [f"[[{slugify(e.slug)}]]" for e in bundle.entities] + [
        f"[[{slugify(c.slug)}]]" for c in bundle.concepts
    ]
    ref_line = ("Related: " + " · ".join(refs) + "\n\n") if refs else ""
    return (
        ref_line
        + "## Comparisons\n" + (bundle.comparisons.strip() or "_none yet_") + "\n\n"
        + "## Open questions\n" + (bundle.open_questions.strip() or "_none yet_") + "\n\n"
        + "## Synthesis\n" + (bundle.synthesis.strip() or "_none yet_") + "\n"
    )


def render_bundle(
    persona: str,
    topic: str,
    bundle: DerivativeBundle,
    sources: List[str],
    stamp: str,
) -> List[RenderedNote]:
    """Produce the candidate notes for a bundle without touching disk or index."""
    notes: List[RenderedNote] = []
    for kind, items in (("entity", bundle.entities), ("concept", bundle.concepts)):
        for item in items:
            slug = slugify(item.slug)
            fm = NoteFrontmatter(
                persona=persona, kind=kind, slug=slug, sources=list(sources),
                last_updated=stamp, topics=[topic],
            )
            notes.append(
                RenderedNote(f"{atomic_dir(kind)}/{slug}.md", fm, item.body, kind, slug, topic)
            )
    topic_fm = NoteFrontmatter(
        persona=persona, kind="topic", topic=topic, sources=list(sources), last_updated=stamp,
    )
    notes.append(
        RenderedNote(f"topics/{topic}.md", topic_fm, render_topic_body(bundle), "topic", topic, topic)
    )
    return notes


def write_rendered(root: Path, note: RenderedNote) -> Path:
    """Write a candidate note, merging back-refs/sources with any existing file."""
    existing = root / note.rel_path
    if existing.exists():
        old_fm, _ = parse_note(existing.read_text(encoding="utf-8"))
        note.fm.sources = _union(old_fm.sources, note.fm.sources)
        if note.kind != "topic":
            note.fm.topics = _union(old_fm.topics, note.fm.topics)
    return write_note(root, note.rel_path, note.fm, note.body)


def register_rendered(index: WikiIndex, note: RenderedNote, stamp: str) -> None:
    if note.kind == "topic":
        register_topic(index, note.key, len(note.fm.sources), stamp)
    else:
        register_atomic(index, note.kind, note.key, note.proc_topic, stamp)


def apply_bundle(
    root: Path,
    persona: str,
    topic: str,
    bundle: DerivativeBundle,
    sources: List[str],
    index: WikiIndex,
    stamp: str,
) -> List[Path]:
    """Render, write, and index a bundle in one call (used by bootstrap)."""
    written: List[Path] = []
    for note in render_bundle(persona, topic, bundle, sources, stamp):
        written.append(write_rendered(root, note))
        register_rendered(index, note, stamp)
    return written
