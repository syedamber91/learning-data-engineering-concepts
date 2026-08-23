import pytest

from persona_wiki.udemy import parse_lecture

LECTURE = '''---
title: "Adapter Pattern (Structural Design Pattern)"
course: "System Design (LLD + HLD) from Basics to Advanced"
section: "LLD (Low Level Design)"
url: "https://www.udemy.com/course/draft/5776816/learn/lecture/41932990"
duration: "00:16:44"
captured_at: 2026-08-22T06:02:45.870634+00:00
topics: [Career, Education]
tags: [tooling, architecture]
---

# Adapter Pattern (Structural Design Pattern)

Part of [[courses/system-design|System Design]] → [[courses/system-design/1-lld|LLD]]

[Open on Udemy](https://www.udemy.com/course/draft/5776816/learn/lecture/41932990)

## Transcript

[00:00:00] Hey guys. Welcome to Concept and Coding.

[00:01:00] Existing interface. And another is. Expected interface.
'''


def test_parse_lecture_extracts_frontmatter_and_transcript():
    fm, body = parse_lecture(LECTURE)
    assert fm["title"] == "Adapter Pattern (Structural Design Pattern)"
    assert fm["section"] == "LLD (Low Level Design)"
    assert fm["duration"] == "00:16:44"
    assert body.startswith("[00:00:00] Hey guys.")
    assert "[00:01:00] Existing interface." in body


def test_parse_lecture_drops_vault_local_link_lines():
    _, body = parse_lecture(LECTURE)
    assert "Part of [[courses" not in body
    assert "[Open on Udemy]" not in body
    assert "# Adapter Pattern" not in body


def test_parse_lecture_rejects_missing_transcript():
    no_transcript = LECTURE.split("## Transcript")[0]
    with pytest.raises(ValueError, match="Transcript"):
        parse_lecture(no_transcript)


import os
from pathlib import Path

from persona_wiki.udemy import lecture_id_from_filename, load_group_map

GROUP_MAP = Path(__file__).resolve().parents[2] / "data" / "sj_lecture_groups.yaml"
UDEMY_DIR = Path(
    os.path.expanduser(
        "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Udemy Vault/"
        "lectures/system-design-lld-hld-from-basics-to-advanced"
    )
)


def test_lecture_id_from_filename():
    assert lecture_id_from_filename(
        "1-adapter-pattern-structural-design-pattern-41932990.md") == "41932990"


def test_lecture_id_from_filename_rejects_unnumbered():
    with pytest.raises(ValueError):
        lecture_id_from_filename("notes.md")


def test_load_group_map_flattens_groups(tmp_path):
    f = tmp_path / "m.yaml"
    f.write_text(
        'course_dir: "x"\ngroups:\n'
        "  databases:\n    - 111   # SQL vs NoSQL\n    - 222\n"
        "  case-studies:\n    - 333\n",
        encoding="utf-8")
    assert load_group_map(f) == {"111": "databases", "222": "databases",
                                 "333": "case-studies"}


def test_load_group_map_rejects_duplicate_id(tmp_path):
    f = tmp_path / "m.yaml"
    f.write_text('groups:\n  a:\n    - 111\n  b:\n    - 111\n', encoding="utf-8")
    with pytest.raises(ValueError, match="111"):
        load_group_map(f)


@pytest.mark.skipif(not UDEMY_DIR.exists(), reason="Udemy Vault not present on this machine")
def test_group_map_covers_every_lecture_exactly_once():
    """The union of all group id-lists == the ids in the real course directory."""
    mapped = set(load_group_map(GROUP_MAP))
    on_disk = {lecture_id_from_filename(p.name) for p in UDEMY_DIR.glob("*.md")}
    assert mapped - on_disk == set(), f"map lists unknown ids: {mapped - on_disk}"
    assert on_disk - mapped == set(), f"lectures missing from map: {on_disk - mapped}"
    assert len(on_disk) == 75
