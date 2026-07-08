from persona_wiki.index import (
    has_atomic,
    has_topic,
    load_index,
    register_atomic,
    register_topic,
    save_index,
)
from persona_wiki.models import WikiIndex


def test_register_and_lookup_topic():
    idx = WikiIndex()
    register_topic(idx, "kafka", 2, "2026-07-08")
    assert has_topic(idx, "kafka")
    assert idx.topics["kafka"].file == "topics/kafka.md"
    assert idx.topics["kafka"].sources == 2


def test_register_atomic_merges_topic_backrefs():
    idx = WikiIndex()
    register_atomic(idx, "entity", "lsm-tree", "kafka", "2026-07-08")
    register_atomic(idx, "entity", "lsm-tree", "spark", "2026-07-09")
    assert has_atomic(idx, "entity", "lsm-tree")
    assert idx.entities["lsm-tree"].topics == ["kafka", "spark"]  # deduped, ordered


def test_index_roundtrip_on_disk(tmp_path):
    idx = WikiIndex()
    register_topic(idx, "kafka", 1, "2026-07-08")
    save_index(tmp_path, idx)
    reloaded = load_index(tmp_path)
    assert has_topic(reloaded, "kafka")


def test_load_missing_index_is_empty(tmp_path):
    assert load_index(tmp_path).total() == 0
