"""Stage A feeder for Udemy lecture notes: transform a captured lecture into the
persona wiki's immutable raw/<group>/ layer, routed by a checked-in
lecture_id -> group map. Append-only, like ingest.py, but transforming rather
than copying (ingest.py is a byte-for-byte shutil.copyfile and has no seam for
this)."""

from __future__ import annotations

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
