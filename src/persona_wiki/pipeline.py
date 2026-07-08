"""Orchestrate the 7-step persona-wiki update over a batch of sources."""

from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import BaseModel

from .cdc import decide_topic, load_existing_topic_body
from .derive import apply_bundle
from .index import load_index, save_index
from .llm import LLMFn, build_derive_prompt
from .log import log_ingest
from .models import DerivativeBundle, WikiIndex
from .qc import qc_check
from .storage import parse_note
from .topics import match_topics


class Source(BaseModel):
    id: str
    text: str


def _demote_failed(path: Path, reason: str) -> None:
    """Rewrite a note's frontmatter to qc: failed (kept on disk, not indexed)."""
    fm, body = parse_note(path.read_text(encoding="utf-8"))
    fm.qc = "failed"
    fm.qc_reason = reason
    from .storage import dump_note  # local import avoids cycle at module load
    path.write_text(dump_note(fm, body), encoding="utf-8")


def update(root: Path, persona: str, sources: List[Source], llm: LLMFn, stamp: str) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    index = load_index(root)
    written = 0
    failed = 0

    for src in sources:
        for topic in match_topics(src.text):
            decision = decide_topic(index, topic)
            existing = load_existing_topic_body(root, topic) if decision == "revise" else ""
            try:
                raw = llm(build_derive_prompt(persona, topic, src.text, existing))
                bundle = DerivativeBundle.parse_raw_json(raw)
            except ValueError:
                failed += 1
                continue

            # Derive into a throwaway index first so a QC failure doesn't leak
            # registrations; merge only the blessed notes back.
            staging = WikiIndex(**index.model_dump())
            paths = apply_bundle(root, persona, topic, bundle, [src.id], staging, stamp)

            all_passed = True
            for path in paths:
                passed, reason = qc_check(path.read_text(encoding="utf-8"), src.text, llm)
                if not passed:
                    _demote_failed(path, reason)
                    all_passed = False
            if all_passed:
                index = staging
                written += len(paths)

    save_index(root, index)
    logged = log_ingest(root / "log.md", index.total(), f"{written} note(s) written", stamp)
    return {"written": written, "failed": failed, "logged": logged}
