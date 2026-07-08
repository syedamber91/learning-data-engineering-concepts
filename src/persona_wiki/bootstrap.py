"""One-time bootstrap: split the authored ``vutr.md`` snapshot's TECHNICAL
POSITIONS sections into the atomic note layout so existing knowledge is kept."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

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


def bootstrap(root: Path, persona: str, persona_md: str, llm: LLMFn, stamp: str) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    index = load_index(root)
    sections = parse_persona_sections(persona_md)
    for title, text in sections:
        topic = _topic_slug(title)
        raw = llm(build_bootstrap_prompt(persona, topic, text))
        bundle = DerivativeBundle.parse_raw_json(raw)
        apply_bundle(root, persona, topic, bundle, ["persona-snapshot"], index, stamp)
    save_index(root, index)
    summary = f"{len(index.topics)} topic notes, {len(index.entities)} entities, {len(index.concepts)} concepts already synthesized"
    logged = log_ingest(root / "log.md", index.total(), summary, stamp)
    return {"topics": len(sections), "logged": logged}
