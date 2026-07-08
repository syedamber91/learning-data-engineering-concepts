"""Change-data-capture: decide whether a topic note is new (create) or already
exists (revise), and load the prior body to feed the reviser."""

from __future__ import annotations

from pathlib import Path

from .index import has_topic
from .models import WikiIndex
from .storage import parse_note


def decide_topic(index: WikiIndex, topic: str) -> str:
    return "revise" if has_topic(index, topic) else "create"


def load_existing_topic_body(root: Path, topic: str) -> str:
    path = root / "topics" / f"{topic}.md"
    if not path.exists():
        return ""
    _, body = parse_note(path.read_text(encoding="utf-8"))
    return body
