import pytest

from persona_wiki.models import (
    AtomicEntry,
    DerivativeBundle,
    NoteFrontmatter,
    TopicEntry,
    WikiIndex,
)


def test_bundle_parses_json_with_fence():
    raw = '```json\n{"entities": [{"slug": "lsm-tree", "body": "x"}], "synthesis": "s"}\n```'
    bundle = DerivativeBundle.parse_raw_json(raw)
    assert bundle.entities[0].slug == "lsm-tree"
    assert bundle.synthesis == "s"
    assert bundle.concepts == []


def test_bundle_parse_raises_on_garbage():
    with pytest.raises(ValueError):
        DerivativeBundle.parse_raw_json("not json at all")


def test_index_total_counts_all_kinds():
    idx = WikiIndex(
        topics={"kafka": TopicEntry(file="topics/kafka.md", sources=2, last_updated="2026-07-08")},
        entities={"lsm-tree": AtomicEntry(file="entities/lsm-tree.md", topics=["kafka"], last_updated="2026-07-08")},
        concepts={"log-compaction": AtomicEntry(file="concepts/log-compaction.md", last_updated="2026-07-08")},
    )
    assert idx.total() == 3


def test_frontmatter_defaults_qc_passed():
    fm = NoteFrontmatter(persona="vutr", kind="topic", sources=["s1"], last_updated="2026-07-08", topic="kafka")
    assert fm.qc == "passed"
    assert fm.topics == []
