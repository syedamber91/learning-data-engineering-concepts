"""Tests for the Claude-Code-powered teaching engine (offline / dry-run only)."""

from __future__ import annotations

from pathlib import Path

import pytest

from de_toolkit.cli import _sample_catalog
from de_toolkit.teach import (
    _strip_code_fence,
    build_lesson_prompt,
    build_roadmap_prompt,
    iter_selections,
)


def test_strip_code_fence():
    fenced = "```markdown\n---\ntitle: X\n---\nbody\n```"
    assert _strip_code_fence(fenced) == "---\ntitle: X\n---\nbody"
    plain = "---\ntitle: X\n---\nbody"
    assert _strip_code_fence(plain) == plain


def test_sample_catalog_is_a_full_syllabus():
    catalog = _sample_catalog()
    titles = {a.title for a in catalog.areas}
    assert {"Software Engineering Foundations", "Databases",
            "Data Pipelines"} <= titles
    n_concepts = sum(len(t.concepts) for a in catalog.areas for t in a.topics)
    assert n_concepts >= 14  # the expanded syllabus, not the old 4-concept sample


def test_iter_selections_filters_by_concept():
    catalog = _sample_catalog()
    sels = list(iter_selections(catalog, concept="Indexing"))
    assert len(sels) == 1
    assert sels[0].concept.title == "Indexing"
    assert sels[0].area.title == "Databases"


def test_selection_target_path():
    catalog = _sample_catalog()
    sel = next(iter_selections(catalog, concept="Indexing"))
    target = sel.target(Path("/tmp/learning-vault"))
    assert target == Path(
        "/tmp/learning-vault/databases/relational-databases/indexing.md"
    )


def test_lesson_prompt_includes_engine_and_concept():
    catalog = _sample_catalog()
    sel = next(iter_selections(catalog, concept="Indexing"))
    prompt = build_lesson_prompt(sel)
    # Pulls in the reusable teaching mega-prompt...
    assert "Vault Teaching Engine" in prompt
    assert "PRESENTATION CONTRACT" in prompt
    # ...and the specific concept payload + mandatory-use-case reminder.
    assert "Indexing" in prompt
    assert "real-world use case is mandatory" in prompt


def test_roadmap_prompt_lists_areas():
    catalog = _sample_catalog()
    prompt = build_roadmap_prompt(catalog)
    assert "ROADMAP" in prompt
    assert "Databases" in prompt


def test_iter_selections_empty_for_unknown_concept():
    catalog = _sample_catalog()
    assert list(iter_selections(catalog, concept="Nonexistent")) == []
