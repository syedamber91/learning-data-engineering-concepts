"""Tests for the Claude-Code-powered teaching engine (offline / dry-run only)."""

from __future__ import annotations

from pathlib import Path

import pytest

from de_toolkit.cli import _sample_catalog
from de_toolkit.diagrams import MERMAID_RE, rasterize_lesson
from de_toolkit.teach import (
    _inject_breadcrumb,
    _inject_nav,
    _one_liner,
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


def test_inject_breadcrumb_after_h1():
    md = "---\ntitle: Indexing\n---\n\n# Indexing\n\n## In one line\nAn index..."
    out = _inject_breadcrumb(md, "Databases", "Relational Databases")
    assert "[[relational-databases-moc|Relational Databases]]" in out
    assert "[[databases-moc|Databases]]" in out
    # breadcrumb sits immediately under the H1, before the first section
    assert out.index("*Part of") < out.index("## In one line")
    # idempotent
    assert _inject_breadcrumb(out, "Databases", "Relational Databases") == out


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
    # ...and the specific concept payload + the leveled, illustrated requirements.
    assert "Indexing" in prompt
    assert "Level 1 — The big idea" in prompt
    assert "mermaid" in prompt
    assert "Coming up next" in prompt
    assert "Check yourself" in prompt


def test_lesson_prompt_threads_prerequisite_context():
    catalog = _sample_catalog()
    sel = next(iter_selections(catalog, concept="Indexing"))
    prompt = build_lesson_prompt(
        sel, catalog,
        story_so_far="- Tables, Keys & SQL Basics: rows and columns",
        prev_lesson_md="# Tables\n\n## Level 1\nA table stores rows.",
        prev_title="Tables, Keys & SQL Basics",
        next_title="Transactions & ACID",
    )
    assert "STORY SO FAR" in prompt
    assert "Tables, Keys & SQL Basics" in prompt
    assert "PREVIOUS_LESSON" in prompt
    assert "Transactions & ACID" in prompt


def test_inject_nav_adds_prev_next():
    catalog = _sample_catalog()
    course = list(iter_selections(catalog))
    i = next(k for k, s in enumerate(course) if s.concept.title == "Indexing")
    md = (
        "---\ntitle: Indexing\n---\n\n# Indexing\n\n"
        "*Part of [[x-moc|X]]*\n\n## Level 1 — The big idea\nstuff"
    )
    out = _inject_nav(md, course[i - 1], course[i + 1])
    assert "← Prev: [[" in out and "Next: [[" in out
    # nav sits between the breadcrumb and the first level
    assert out.index("*Part of") < out.index("Prev:") < out.index("## Level 1")


def test_one_liner_extracts_first_prose_sentence():
    md = (
        "---\ntitle: X\n---\n\n# X\n\n*Part of [[a]]*\n\n"
        "## Level 1 — The big idea\n"
        "An index is a sorted lookup structure. It makes reads fast."
    )
    assert _one_liner(md) == "An index is a sorted lookup structure"


def test_rasterize_lesson_without_renderer_keeps_mermaid(tmp_path, monkeypatch):
    # When mmdc is unavailable, blocks are left intact so Obsidian still renders them.
    monkeypatch.setattr("de_toolkit.diagrams.mmdc_available", lambda: False)
    md = "# X\n\n```mermaid\ngraph LR\n  A-->B\n```\n\nbody"
    out, svgs, failures = rasterize_lesson(md, "x", tmp_path / "assets")
    assert out == md
    assert svgs == []
    assert failures == 1
    assert len(MERMAID_RE.findall(md)) == 1


def test_lesson_prompt_link_guide_uses_real_targets():
    catalog = _sample_catalog()
    sel = next(iter_selections(catalog, concept="Indexing"))
    prompt = build_lesson_prompt(sel, catalog)
    assert "VAULT LINK TARGETS" in prompt
    # a real sibling concept appears as a proper slug wikilink target
    assert "[[transactions-acid|Transactions & ACID]]" in prompt
    # the current concept is excluded from its own link guide
    assert "[[indexing|Indexing]]" not in prompt


def test_roadmap_prompt_lists_areas():
    catalog = _sample_catalog()
    prompt = build_roadmap_prompt(catalog)
    assert "ROADMAP" in prompt
    assert "Databases" in prompt


def test_iter_selections_empty_for_unknown_concept():
    catalog = _sample_catalog()
    assert list(iter_selections(catalog, concept="Nonexistent")) == []
