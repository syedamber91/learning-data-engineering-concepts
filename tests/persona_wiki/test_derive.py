from persona_wiki.derive import apply_bundle, render_topic_body
from persona_wiki.index import has_atomic, has_topic
from persona_wiki.models import ConceptOut, DerivativeBundle, EntityOut, WikiIndex


def _bundle():
    return DerivativeBundle(
        entities=[EntityOut(slug="lsm-tree", body="LSM body")],
        concepts=[ConceptOut(slug="log-compaction", body="Compaction body")],
        comparisons="SMJ vs SHJ",
        open_questions="- why?",
        synthesis="Kafka is write-optimized.",
    )


def test_render_topic_body_links_atomics():
    body = render_topic_body(_bundle())
    assert "[[lsm-tree]]" in body and "[[log-compaction]]" in body
    assert "## Comparisons" in body and "## Synthesis" in body


def test_apply_bundle_writes_notes_and_registers(tmp_path):
    idx = WikiIndex()
    written = apply_bundle(tmp_path, "vutr", "kafka", _bundle(), ["s1"], idx, "2026-07-08")
    assert (tmp_path / "topics/kafka.md").exists()
    assert (tmp_path / "entities/lsm-tree.md").exists()
    assert (tmp_path / "concepts/log-compaction.md").exists()
    assert has_topic(idx, "kafka") and has_atomic(idx, "entity", "lsm-tree")
    assert len(written) == 3


def test_shared_entity_written_once_two_topics(tmp_path):
    idx = WikiIndex()
    b1 = DerivativeBundle(entities=[EntityOut(slug="lsm-tree", body="b")], synthesis="k")
    b2 = DerivativeBundle(entities=[EntityOut(slug="lsm-tree", body="b")], synthesis="s")
    apply_bundle(tmp_path, "vutr", "kafka", b1, ["s1"], idx, "2026-07-08")
    apply_bundle(tmp_path, "vutr", "spark", b2, ["s2"], idx, "2026-07-09")
    # one entity file, referenced from both topics
    assert idx.entities["lsm-tree"].topics == ["kafka", "spark"]
    assert (tmp_path / "topics/kafka.md").exists()
    assert (tmp_path / "topics/spark.md").exists()
    # the entity note's own frontmatter must agree with the index (union, not clobber)
    from persona_wiki.storage import parse_note
    fm, _ = parse_note((tmp_path / "entities/lsm-tree.md").read_text(encoding="utf-8"))
    assert fm.topics == ["kafka", "spark"]
    assert fm.sources == ["s1", "s2"]


def test_slug_is_normalized_so_wikilink_matches_file(tmp_path):
    idx = WikiIndex()
    # LLM emits a non-normalized slug; the file, the [[link]], and the index must agree
    b = DerivativeBundle(entities=[EntityOut(slug="LSM Tree", body="b")], synthesis="s")
    apply_bundle(tmp_path, "vutr", "kafka", b, ["s1"], idx, "2026-07-08")
    assert (tmp_path / "entities/lsm-tree.md").exists()
    assert "[[lsm-tree]]" in (tmp_path / "topics/kafka.md").read_text(encoding="utf-8")
    assert "lsm-tree" in idx.entities
