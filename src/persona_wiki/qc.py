"""Single-pass QC: ask the LLM whether every claim in a note traces to its
source. Fails closed on any unparseable verdict."""

from __future__ import annotations

import json
import re
from typing import Tuple

from .llm import LLMFn, build_qc_prompt

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
