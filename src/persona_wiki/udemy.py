"""Stage A feeder for Udemy lecture notes: transform a captured lecture into the
persona wiki's immutable raw/<group>/ layer, routed by a checked-in
lecture_id -> group map. Append-only, like ingest.py, but transforming rather
than copying (ingest.py is a byte-for-byte shutil.copyfile and has no seam for
this)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Tuple

import yaml

TRANSCRIPT_HEADING = "## Transcript"


def parse_lecture(text: str) -> Tuple[dict, str]:
    """(frontmatter dict, transcript body) for one captured Udemy lecture note.

    Everything before the ``## Transcript`` heading is discarded: it is the H1,
    a ``Part of [[courses/...]]`` breadcrumb and an ``[Open on Udemy]`` link,
    all of which point into a different Obsidian vault.
    """
    if not text.startswith("---"):
        raise ValueError("lecture note has no frontmatter")
    _, front, rest = text.split("---", 2)
    fm = yaml.safe_load(front) or {}
    if TRANSCRIPT_HEADING not in rest:
        raise ValueError(f"lecture note has no '{TRANSCRIPT_HEADING}' section")
    body = rest.split(TRANSCRIPT_HEADING, 1)[1]
    return fm, body.strip()


_LECTURE_ID_RE = re.compile(r"-(\d+)\.md$")


def lecture_id_from_filename(name: str) -> str:
    """The trailing numeric Udemy lecture id: '1-adapter-...-41932990.md' -> '41932990'."""
    m = _LECTURE_ID_RE.search(name)
    if not m:
        raise ValueError(f"no lecture id in filename: {name}")
    return m.group(1)


def load_group_map(path: Path) -> Dict[str, str]:
    """lecture_id -> group slug, flattened from the YAML's nested ``groups:`` block."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out: Dict[str, str] = {}
    for group, ids in (data.get("groups") or {}).items():
        for lecture_id in ids or []:
            key = str(lecture_id)
            if key in out:
                raise ValueError(
                    f"lecture id {key} listed in both '{out[key]}' and '{group}'")
            out[key] = group
    return out
