"""Pydantic models describing the data-engineering concept catalog.

The shape mirrors how study material is usually organised: an ``Area`` (e.g.
"Data Modeling") groups ``Topic`` s, and each ``Topic`` groups individual
``Concept`` notes. Only your own text is stored here.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field


class Concept(BaseModel):
    title: str
    # Free-text body / explanation in your own words (Markdown is fine).
    body_text: str = ""
    # Optional reference URL (docs, blog post, paper) for the concept.
    source_url: Optional[str] = None
    # Optional links to further reading / resources.
    resource_links: List[str] = Field(default_factory=list)
    # Optional short bullet "key points" surfaced in the note and graph.
    key_points: List[str] = Field(default_factory=list)
    updated_at: Optional[datetime] = None


class Topic(BaseModel):
    title: str
    concepts: List[Concept] = Field(default_factory=list)


class Area(BaseModel):
    title: str
    topics: List[Topic] = Field(default_factory=list)


class Catalog(BaseModel):
    """Top-level container persisted to ``data/content.json``."""

    title: str = "Data Engineering Concepts"
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    areas: List[Area] = Field(default_factory=list)

    def concept_titles(self) -> set[str]:
        """All concept titles already captured — handy for de-duplication."""
        titles: set[str] = set()
        for area in self.areas:
            for topic in area.topics:
                for concept in topic.concepts:
                    titles.add(concept.title)
        return titles
