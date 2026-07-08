"""Orchestrate the 7-step persona-wiki update over a batch of sources.

Candidate notes are QC'd in memory and only written to their canonical path
once the whole bundle passes, so the canonical tree only ever holds QC-passed
content — a failing revise can no longer clobber a good note. Rejected bundles
are written under ``_rejected/`` (with ``qc: failed`` and the reason) for
inspection. A source already recorded in a topic note is skipped, so re-runs
neither re-invoke the LLM nor rewrite notes.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import BaseModel

from .cdc import decide_topic, load_existing_topic_body
from .derive import RenderedNote, register_rendered, render_bundle, write_rendered
from .index import load_index, save_index
from .llm import LLMFn, build_derive_prompt
from .log import log_ingest
from .models import DerivativeBundle
from .qc import qc_check
from .storage import dump_note, parse_note, write_note
from .topics import match_topics


class Source(BaseModel):
    id: str
    text: str


def _topic_sources(root: Path, topic: str) -> List[str]:
    """Source ids already recorded in a topic note (empty if it doesn't exist)."""
    path = root / "topics" / f"{topic}.md"
    if not path.exists():
        return []
    fm, _ = parse_note(path.read_text(encoding="utf-8"))
    return fm.sources


def _quarantine(root: Path, note: RenderedNote, reason: str) -> None:
    """Write a rejected candidate under _rejected/ with qc: failed — never canonical."""
    fm = note.fm.model_copy(update={"qc": "failed", "qc_reason": reason})
    write_note(root, f"_rejected/{note.rel_path}", fm, note.body)


def update(root: Path, persona: str, sources: List[Source], llm: LLMFn, stamp: str) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    index = load_index(root)
    written = 0
    failed = 0
    skipped = 0

    for src in sources:
        for topic in match_topics(src.text):
            decision = decide_topic(index, topic)
            if decision == "revise" and src.id in _topic_sources(root, topic):
                skipped += 1  # already ingested — no LLM call, no rewrite
                continue

            existing = load_existing_topic_body(root, topic) if decision == "revise" else ""
            known = sorted(index.entities) + sorted(index.concepts)
            try:
                raw = llm(build_derive_prompt(persona, topic, src.text, existing, known_slugs=known))
                bundle = DerivativeBundle.parse_raw_json(raw)
            except ValueError:
                failed += 1
                continue

            candidates = render_bundle(persona, topic, bundle, [src.id], stamp)
            verdicts = [
                (note, qc_check(dump_note(note.fm, note.body), src.text, llm))
                for note in candidates
            ]
            if all(passed for _, (passed, _) in verdicts):
                for note, _ in verdicts:
                    write_rendered(root, note)
                    register_rendered(index, note, stamp)
                written += len(candidates)
            else:
                failed += 1
                for note, (passed, reason) in verdicts:
                    _quarantine(root, note, reason if not passed else "bundle rejected")

    save_index(root, index)
    logged = log_ingest(root / "log.md", index.total(), f"{written} note(s) written", stamp)
    return {"written": written, "failed": failed, "skipped": skipped, "logged": logged}
