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
