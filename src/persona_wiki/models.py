"""Pydantic models for the persona wiki: note frontmatter, the LLM's derivative
output bundle, and the on-disk index."""

from __future__ import annotations

import json
import re
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n(.*)\n```$", re.DOTALL)


class NoteFrontmatter(BaseModel):
    persona: str
    kind: str                      # "topic" | "entity" | "concept"
    sources: List[str] = Field(default_factory=list)
    last_updated: str
    qc: str = "passed"             # "passed" | "failed"
    qc_reason: Optional[str] = None
    topic: Optional[str] = None    # topic notes
    slug: Optional[str] = None     # atomic notes
    topics: List[str] = Field(default_factory=list)  # atomic back-refs
    learner: Optional[str] = None       # learner-persona notes (Alex)
    source_note: Optional[str] = None   # the vutr slug this understanding came from
    mastery: Optional[str] = None       # "learning" | "familiar" | "mastered"


class EntityOut(BaseModel):
    slug: str
    body: str = ""


class ConceptOut(BaseModel):
    slug: str
    body: str = ""


class DerivativeBundle(BaseModel):
    entities: List[EntityOut] = Field(default_factory=list)
    concepts: List[ConceptOut] = Field(default_factory=list)
    comparisons: str = ""
    open_questions: str = ""
    synthesis: str = ""

    @classmethod
    def parse_raw_json(cls, text: str) -> "DerivativeBundle":
        """Parse the LLM's JSON output, tolerating a ```json fence."""
        stripped = text.strip()
        m = _FENCE_RE.match(stripped)
        if m:
            stripped = m.group(1).strip()
        try:
            data = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"LLM did not return valid JSON: {exc}") from exc
        return cls.model_validate(data)


class TopicEntry(BaseModel):
    file: str
    sources: int = 0
    last_updated: str


class AtomicEntry(BaseModel):
    file: str
    topics: List[str] = Field(default_factory=list)
    last_updated: str


class WikiIndex(BaseModel):
    topics: Dict[str, TopicEntry] = Field(default_factory=dict)
    entities: Dict[str, AtomicEntry] = Field(default_factory=dict)
    concepts: Dict[str, AtomicEntry] = Field(default_factory=dict)

    def total(self) -> int:
        return len(self.topics) + len(self.entities) + len(self.concepts)
