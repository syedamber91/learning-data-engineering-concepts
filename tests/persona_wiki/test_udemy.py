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
