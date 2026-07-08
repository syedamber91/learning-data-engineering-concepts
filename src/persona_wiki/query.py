"""Answer-routing over the persona wiki: index -> topic note -> linked atomics.

This is deliberately mechanical retrieval (the cheap 'routing' half). It returns
the relevant note bodies; a caller/agent does the final synthesis.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

from .index import load_index
from .storage import parse_note
from .topics import match_topics

_WIKILINK_RE = re.compile(r"\[\[([a-z0-9-]+)\]\]")
_NO_MATCH = "No matching notes in the persona wiki."


def _read_if_passed(path: Path) -> str:
    if not path.exists():
        return ""
    fm, body = parse_note(path.read_text(encoding="utf-8"))
    return "" if fm.qc == "failed" else body


def query(root: Path, question: str) -> str:
    index = load_index(root)
    parts: List[str] = []
    seen: set = set()  # each atomic is emitted at most once across the whole answer
    for topic in match_topics(question):
        if topic not in index.topics:
            continue
        body = _read_if_passed(root / "topics" / f"{topic}.md")
        if not body:
            continue
        parts.append(f"# {topic}\n{body}")
        for slug in dict.fromkeys(_WIKILINK_RE.findall(body)):  # dedupe, keep order
            if slug in seen:
                continue
            for kind in ("entities", "concepts"):
                atomic = _read_if_passed(root / kind / f"{slug}.md")
                if atomic:
                    parts.append(f"## {slug}\n{atomic}")
                    seen.add(slug)
                    break
    return "\n\n".join(parts) if parts else _NO_MATCH
