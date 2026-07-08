from pathlib import Path

from persona_wiki.config import WIKI_SUBDIR, persona_root


def test_persona_root_is_under_wiki_personas():
    root = persona_root(Path("/tmp/lv"), "vutr")
    assert root == Path("/tmp/lv/wiki/personas/vutr")
    assert WIKI_SUBDIR == "wiki/personas"
