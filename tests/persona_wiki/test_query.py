from persona_wiki.index import load_index, save_index
from persona_wiki.models import NoteFrontmatter, WikiIndex
from persona_wiki.index import register_atomic, register_topic
from persona_wiki.query import query
from persona_wiki.storage import write_note


def _seed(tmp_path):
    idx = WikiIndex()
    register_topic(idx, "kafka", 1, "2026-07-08")
    register_atomic(idx, "entity", "lsm-tree", "kafka", "2026-07-08")
    save_index(tmp_path, idx)
    write_note(tmp_path, "topics/kafka.md",
               NoteFrontmatter(persona="vutr", kind="topic", topic="kafka",
                               sources=["s1"], last_updated="2026-07-08"),
               "## Synthesis\nKafka is write-optimized. Related: [[lsm-tree]]")
    write_note(tmp_path, "entities/lsm-tree.md",
               NoteFrontmatter(persona="vutr", kind="entity", slug="lsm-tree",
                               sources=["s1"], last_updated="2026-07-08", topics=["kafka"]),
               "LSM-trees batch writes.")


def test_query_returns_topic_and_linked_atomic(tmp_path):
    _seed(tmp_path)
    out = query(tmp_path, "how does kafka handle writes?")
    assert "write-optimized" in out
    assert "LSM-trees batch writes." in out  # followed the [[lsm-tree]] link


def test_query_no_match_sentinel(tmp_path):
    _seed(tmp_path)
    assert "no matching" in query(tmp_path, "gardening").lower()


def test_query_skips_qc_failed(tmp_path):
    _seed(tmp_path)
    # demote the topic note to failed
    p = tmp_path / "topics/kafka.md"
    p.write_text(p.read_text().replace("qc: passed", "qc: failed")
                 if "qc: passed" in p.read_text() else
                 p.read_text().replace("kind: topic", "kind: topic\nqc: failed"),
                 encoding="utf-8")
    out = query(tmp_path, "kafka writes")
    assert "write-optimized" not in out
