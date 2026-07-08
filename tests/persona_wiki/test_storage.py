from pathlib import Path

import pytest

from persona_wiki.models import NoteFrontmatter
from persona_wiki.storage import dump_note, parse_note, write_note


def _fm():
    return NoteFrontmatter(
        persona="vutr", kind="entity", slug="lsm-tree",
        sources=["substack/vutr/kafka-internals"], last_updated="2026-07-08",
        topics=["kafka"],
    )


def test_dump_then_parse_roundtrip():
    text = dump_note(_fm(), "Vu Trinh on LSM-trees.")
    fm, body = parse_note(text)
    assert fm.slug == "lsm-tree"
    assert fm.topics == ["kafka"]
    assert body.strip() == "Vu Trinh on LSM-trees."


def test_write_note_creates_file_under_root(tmp_path):
    p = write_note(tmp_path, "entities/lsm-tree.md", _fm(), "body")
    assert p == tmp_path / "entities/lsm-tree.md"
    assert p.read_text(encoding="utf-8").startswith("---")


def test_write_note_rejects_path_outside_root(tmp_path):
    with pytest.raises(ValueError):
        write_note(tmp_path, "../escape.md", _fm(), "body")
