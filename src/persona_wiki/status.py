"""Stage-skip probe for the /learn-topic orchestrator: report whether each
pipeline stage's output is current, stale, or missing."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from .qc import provenance_gate, resolution_gate, wikilinks
from .storage import parse_note


def _synthesize_status(root: Path, topic: str) -> str:
    tpath = root / "topics" / f"{topic}.md"
    if not tpath.exists():
        return "missing"
    _, body = parse_note(tpath.read_text(encoding="utf-8"))
    ok, _ = resolution_gate(body, root)
    if not ok:
        return "stale"
    for slug in wikilinks(body):
        cpath = root / "concepts" / f"{slug}.md"
        if cpath.exists():
            fm, _ = parse_note(cpath.read_text(encoding="utf-8"))
            passed, _ = provenance_gate(fm)
            if not passed:
                return "stale"
    return "current"


def stage_status(root: Path, learner_root: Path, topic: str) -> Dict[str, str]:
    raw = root / "raw" / topic
    has_raw = raw.exists() and any(
        p.suffix == ".md" and not p.name.startswith("_") for p in raw.iterdir())
    mastery = learner_root / topic / "mastery.md"
    if not mastery.exists():
        learn = "missing"
    elif "100%" in mastery.read_text(encoding="utf-8"):
        learn = "current"
    else:
        learn = "stale"
    return {
        "ingest": "current" if has_raw else "missing",
        "synthesize": _synthesize_status(root, topic),
        "learn": learn,
    }
