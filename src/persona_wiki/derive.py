"""Turn a DerivativeBundle into atomic entity/concept notes plus a topic note,
deduplicating shared atomics and wiring wikilinks."""

from __future__ import annotations

from pathlib import Path
from typing import List

from .index import atomic_dir, register_atomic, register_topic
from .models import DerivativeBundle, NoteFrontmatter, WikiIndex
from .storage import write_note


def render_topic_body(bundle: DerivativeBundle) -> str:
    refs = [f"[[{e.slug}]]" for e in bundle.entities] + [f"[[{c.slug}]]" for c in bundle.concepts]
    ref_line = ("Related: " + " · ".join(refs) + "\n\n") if refs else ""
    return (
        ref_line
        + "## Comparisons\n" + (bundle.comparisons.strip() or "_none yet_") + "\n\n"
        + "## Open questions\n" + (bundle.open_questions.strip() or "_none yet_") + "\n\n"
        + "## Synthesis\n" + (bundle.synthesis.strip() or "_none yet_") + "\n"
    )


def apply_bundle(
    root: Path,
    persona: str,
    topic: str,
    bundle: DerivativeBundle,
    sources: List[str],
    index: WikiIndex,
    stamp: str,
) -> List[Path]:
    written: List[Path] = []

    for kind, items in (("entity", bundle.entities), ("concept", bundle.concepts)):
        for item in items:
            fm = NoteFrontmatter(
                persona=persona, kind=kind, slug=item.slug, sources=sources,
                last_updated=stamp, topics=[topic],
            )
            written.append(write_note(root, f"{atomic_dir(kind)}/{item.slug}.md", fm, item.body))
            register_atomic(index, kind, item.slug, topic, stamp)

    topic_fm = NoteFrontmatter(
        persona=persona, kind="topic", topic=topic, sources=sources, last_updated=stamp,
    )
    written.append(write_note(root, f"topics/{topic}.md", topic_fm, render_topic_body(bundle)))
    register_topic(index, topic, len(sources), stamp)
    return written
