from persona_wiki.cdc import decide_topic, load_existing_topic_body
from persona_wiki.index import register_topic
from persona_wiki.models import NoteFrontmatter, WikiIndex
from persona_wiki.storage import write_note


def test_decide_create_when_absent():
    assert decide_topic(WikiIndex(), "kafka") == "create"


def test_decide_revise_when_present():
    idx = WikiIndex()
    register_topic(idx, "kafka", 1, "2026-07-08")
    assert decide_topic(idx, "kafka") == "revise"


def test_load_existing_topic_body(tmp_path):
    fm = NoteFrontmatter(persona="vutr", kind="topic", topic="kafka",
                         sources=["s1"], last_updated="2026-07-08")
    write_note(tmp_path, "topics/kafka.md", fm, "## Synthesis\nold body")
    assert "old body" in load_existing_topic_body(tmp_path, "kafka")


def test_load_missing_topic_body_is_empty(tmp_path):
    assert load_existing_topic_body(tmp_path, "kafka") == ""
