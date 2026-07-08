"""One-time bootstrap: split the authored ``vutr.md`` snapshot's TECHNICAL
POSITIONS sections into the atomic note layout so existing knowledge is kept.

Sections that map to the same topic slug are grouped and derived together into a
single topic note (so neither clobbers the other), each group is processed under
its own error boundary, and the index is saved after every group so one failed
``claude`` call cannot lose the work already done.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

from .derive import apply_bundle
from .index import load_index, save_index
from .llm import LLMFn, build_bootstrap_prompt
from .log import log_ingest
from .models import DerivativeBundle
from .storage import slugify
from .topics import match_topics

_H2_RE = re.compile(r"^## (.+)$", re.MULTILINE)
_H3_RE = re.compile(r"^### (.+)$", re.MULTILINE)


def parse_persona_sections(md: str) -> List[Tuple[str, str]]:
    """Return (title, body) for each ``###`` under ``## TECHNICAL POSITIONS``."""
    h2s = list(_H2_RE.finditer(md))
    start = end = None
    for i, m in enumerate(h2s):
        if m.group(1).strip().upper().startswith("TECHNICAL POSITIONS"):
            start = m.end()
            end = h2s[i + 1].start() if i + 1 < len(h2s) else len(md)
            break
    if start is None:
        return []
    block = md[start:end]
    heads = list(_H3_RE.finditer(block))
    sections: List[Tuple[str, str]] = []
    for i, m in enumerate(heads):
        title = m.group(1).strip()
        body_start = m.end()
        body_end = heads[i + 1].start() if i + 1 < len(heads) else len(block)
        sections.append((title, block[body_start:body_end].strip()))
    return sections


def _topic_slug(title: str) -> str:
    """Map a section title to a topic slug via the vocabulary, else slugify."""
    hits = match_topics(title)
    return hits[0] if hits else slugify(title)


def _group_by_slug(sections: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Collapse sections sharing a topic slug into one combined (slug, text)."""
    order: List[str] = []
    grouped: Dict[str, List[str]] = {}
    for title, text in sections:
        slug = _topic_slug(title)
        if slug not in grouped:
            grouped[slug] = []
            order.append(slug)
        grouped[slug].append(f"### {title}\n{text}")
    return [(slug, "\n\n".join(grouped[slug])) for slug in order]


def bootstrap(root: Path, persona: str, persona_md: str, llm: LLMFn, stamp: str) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    index = load_index(root)
    groups = _group_by_slug(parse_persona_sections(persona_md))

    done = 0
    skipped: List[str] = []
    for slug, text in groups:
        try:
            raw = llm(build_bootstrap_prompt(persona, slug, text))
            bundle = DerivativeBundle.parse_raw_json(raw)
            apply_bundle(root, persona, slug, bundle, ["persona-snapshot"], index, stamp)
        except Exception:  # one bad section must not abort the whole bootstrap
            skipped.append(slug)
            continue
        save_index(root, index)  # incremental: never lose completed groups
        done += 1

    summary = (
        f"{len(index.topics)} topic notes, {len(index.entities)} entities, "
        f"{len(index.concepts)} concepts already synthesized"
    )
    logged = log_ingest(root / "log.md", index.total(), summary, stamp)
    return {"topics": done, "skipped": len(skipped), "logged": logged}
