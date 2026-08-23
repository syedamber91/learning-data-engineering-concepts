from pathlib import Path

from persona_wiki.crosslink import find_matches, normalize


def make_hub(tmp_path: Path, topics_by_persona: dict) -> Path:
    """A miniature hub: wiki/personas/<persona>/topics/<slug>.md"""
    for persona, slugs in topics_by_persona.items():
        d = tmp_path / "wiki" / "personas" / persona / "topics"
        d.mkdir(parents=True, exist_ok=True)
        for slug in slugs:
            (d / f"{slug}.md").write_text("---\nkind: topic\n---\n\nbody\n",
                                          encoding="utf-8")
    return tmp_path


def test_normalize_expands_abbreviations_and_strips_noise():
    assert normalize("hld") == normalize("high-level-design")
    assert normalize("lld") == normalize("Low_Level_Design.md")
    assert normalize("resilience-patterns") == normalize("resilience-pattern")
    assert normalize("authentication-and-security") == frozenset(
        {"authentication", "security"})


def test_normalize_keeps_unrelated_topics_apart():
    assert normalize("structural-patterns") != normalize("resilience-patterns")
    assert normalize("caching-and-rate-limiting") != normalize("storage-tiering-and-caching")


def test_find_matches_returns_persona_and_their_slug(tmp_path):
    hub = make_hub(tmp_path, {
        "sj": ["databases"],
        "lucsystemdesign": ["databases", "api-architecture"],
        "sdcourse": ["bloom-filters"],
    })
    assert find_matches("databases", hub, ["lucsystemdesign", "sdcourse"]) == [
        ("lucsystemdesign", "databases")]


def test_find_matches_returns_nothing_when_no_match(tmp_path):
    hub = make_hub(tmp_path, {
        "sj": ["structural-patterns"],
        "lucsystemdesign": ["resilience-patterns"],
    })
    assert find_matches("structural-patterns", hub, ["lucsystemdesign"]) == []


def test_find_matches_is_deterministically_ordered(tmp_path):
    hub = make_hub(tmp_path, {
        "sj": ["databases"],
        "lucsystemdesign": ["databases"],
        "sdcourse": ["databases"],
    })
    assert find_matches("databases", hub, ["lucsystemdesign", "sdcourse"]) == [
        ("lucsystemdesign", "databases"), ("sdcourse", "databases")]


def test_find_matches_skips_absent_persona(tmp_path):
    hub = make_hub(tmp_path, {"sj": ["databases"]})
    assert find_matches("databases", hub, ["lucsystemdesign"]) == []


from persona_wiki.crosslink import apply_backlinks, backlink_line

BODY = ("Related: [[a]]\n\n## Comparisons\nx\n\n## Open questions\n\n"
        "## Synthesis\nA paragraph.")


def seed_topic(hub: Path, persona: str, slug: str, body: str = BODY) -> Path:
    d = hub / "wiki" / "personas" / persona / "topics"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{slug}.md"
    p.write_text(f"---\npersona: {persona}\nkind: topic\n---\n\n{body}\n",
                 encoding="utf-8")
    return p


def test_backlink_line_is_path_qualified():
    assert backlink_line("lucsystemdesign", "databases") == (
        "**Also covered by:** "
        "[[wiki/personas/lucsystemdesign/topics/databases|lucsystemdesign]]")


def test_backlink_added_on_match(tmp_path):
    note = seed_topic(tmp_path, "sj", "databases")
    seed_topic(tmp_path, "lucsystemdesign", "databases")
    got = apply_backlinks(tmp_path, "sj", ["lucsystemdesign", "sdcourse"])
    assert got == {"databases": [backlink_line("lucsystemdesign", "databases")]}
    text = note.read_text(encoding="utf-8")
    assert text.rstrip().endswith(backlink_line("lucsystemdesign", "databases"))
    assert "## Synthesis\nA paragraph." in text      # existing body preserved


def test_no_backlink_when_no_match_leaves_file_untouched(tmp_path):
    note = seed_topic(tmp_path, "sj", "structural-patterns")
    seed_topic(tmp_path, "lucsystemdesign", "resilience-patterns")
    before = note.read_text(encoding="utf-8")
    assert apply_backlinks(tmp_path, "sj", ["lucsystemdesign"]) == {}
    assert note.read_text(encoding="utf-8") == before


def test_backlink_is_idempotent(tmp_path):
    note = seed_topic(tmp_path, "sj", "databases")
    seed_topic(tmp_path, "lucsystemdesign", "databases")
    apply_backlinks(tmp_path, "sj", ["lucsystemdesign"])
    first = note.read_text(encoding="utf-8")
    assert apply_backlinks(tmp_path, "sj", ["lucsystemdesign"]) == {}
    assert note.read_text(encoding="utf-8") == first


def test_backlink_lists_both_personas_in_order(tmp_path):
    note = seed_topic(tmp_path, "sj", "databases")
    seed_topic(tmp_path, "lucsystemdesign", "databases")
    seed_topic(tmp_path, "sdcourse", "databases")
    apply_backlinks(tmp_path, "sj", ["lucsystemdesign", "sdcourse"])
    lines = [ln for ln in note.read_text(encoding="utf-8").splitlines()
             if ln.startswith("**Also covered by:**")]
    assert lines == [backlink_line("lucsystemdesign", "databases"),
                     backlink_line("sdcourse", "databases")]
