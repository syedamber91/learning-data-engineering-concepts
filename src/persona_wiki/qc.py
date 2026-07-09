"""Single-pass QC: ask the LLM whether every claim in a note traces to its
source. Fails closed on any unparseable verdict.

Also home to the Stage A structural gates: provenance (receipts down to
raw/ sources) and resolution (no dangling wikilinks)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List, Tuple

from .llm import LLMFn, build_qc_prompt
from .models import NoteFrontmatter

_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n(.*)\n```$", re.DOTALL)


def qc_check(note_text: str, source_text: str, llm: LLMFn) -> Tuple[bool, str]:
    raw = llm(build_qc_prompt(note_text, source_text)).strip()
    m = _FENCE_RE.match(raw)
    if m:
        raw = m.group(1).strip()
    try:
        verdict = json.loads(raw)
    except json.JSONDecodeError:
        return False, "unparseable QC verdict"
    return bool(verdict.get("passed", False)), str(verdict.get("reason", ""))


# --- structural gates (Stage A) -------------------------------------------

_WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")


def wikilinks(text: str) -> List[str]:
    """Wikilink targets in order of first appearance, aliases/anchors stripped."""
    seen, out = set(), []
    for m in _WIKILINK_RE.finditer(text):
        slug = m.group(1).strip()
        if slug and slug not in seen:
            seen.add(slug)
            out.append(slug)
    return out


def provenance_gate(fm: NoteFrontmatter) -> Tuple[bool, str]:
    """A concept note must cite at least one raw/ source. 'persona-snapshot'
    alone is the exact failure that hollowed the Spark wiki — reject it."""
    if any(s.startswith("raw/") for s in fm.sources):
        return True, ""
    return False, "no raw/ source cited (persona-snapshot alone is invalid)"


def resolution_gate(body: str, root: Path) -> Tuple[bool, List[str]]:
    """Every wikilink in `body` must resolve to an existing note under root."""
    dangling = []
    for slug in wikilinks(body):
        if not any((root / d / f"{slug}.md").exists()
                   for d in ("concepts", "entities", "topics")):
            dangling.append(slug)
    return (not dangling), dangling
