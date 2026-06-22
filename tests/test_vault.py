"""Tests for the Obsidian vault builder."""

from __future__ import annotations

from de_toolkit.models import Area, Catalog, Concept, Topic
from de_toolkit.vault import _plan_notes, _render_note, build_vault, slugify


def _catalog() -> Catalog:
    return Catalog(
        title="DE",
        areas=[
            Area(
                title="Pipelines",
                topics=[
                    Topic(
                        title="Paradigms",
                        concepts=[
                            Concept(
                                title="Batch vs Streaming",
                                body_text="Batch processing handles bounded data.",
                                key_points=["throughput"],
                                source_url="https://example.com/batch",
                            ),
                            Concept(
                                title="Idempotency",
                                body_text="Idempotent processing makes retries safe.",
                            ),
                        ],
                    )
                ],
            )
        ],
    )


def test_slugify():
    assert slugify("Batch vs Streaming!") == "batch-vs-streaming"
    assert slugify("   ") == "untitled"


def test_plan_notes_links_prev_next():
    notes = _plan_notes(_catalog())
    assert len(notes) == 2
    first, second = notes
    assert first.prev is None
    assert first.next == second.basename
    assert second.prev == first.basename
    assert second.next is None
    # Both share the same topic and area MOCs.
    assert first.topic_moc == second.topic_moc
    assert first.area_moc == second.area_moc


def test_render_note_has_frontmatter_and_wikilinks():
    note = _plan_notes(_catalog())[0]
    rendered = _render_note(note)
    assert rendered.startswith("---\n")
    assert 'title: "Batch vs Streaming"' in rendered
    assert 'area: "Pipelines"' in rendered
    assert "source_url: https://example.com/batch" in rendered
    assert f"[[{note.topic_moc}" in rendered  # breadcrumb wikilink


def test_build_vault_writes_files(tmp_path):
    target = tmp_path / "vault"
    out = build_vault(_catalog(), vault_path=str(target))
    assert out == target.resolve()
    assert (target / "Home.md").exists()
    home = (target / "Home.md").read_text(encoding="utf-8")
    assert "[[pipelines-moc|Pipelines]]" in home
    # One note file per concept under area/topic folders.
    md_files = list(target.rglob("*.md"))
    assert (target / "pipelines" / "paradigms" / "batch-vs-streaming.md") in md_files
