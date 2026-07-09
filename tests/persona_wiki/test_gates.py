from pathlib import Path

from persona_wiki.models import NoteFrontmatter
from persona_wiki.qc import provenance_gate, resolution_gate, wikilinks


def fm(sources):
    return NoteFrontmatter(persona="vutr", kind="concept",
                           sources=sources, last_updated="2026-07-10")


def test_wikilinks_dedup_alias_anchor():
    text = "See [[rdd]] and [[rdd|the RDD]] plus [[photon#jni]] and [[aqe]]."
    assert wikilinks(text) == ["rdd", "photon", "aqe"]


def test_provenance_gate_rejects_snapshot_only():
    ok, reason = provenance_gate(fm(["persona-snapshot"]))
    assert not ok and "raw/" in reason


def test_provenance_gate_accepts_raw_source():
    ok, _ = provenance_gate(fm(["raw/kafka/apache-kafka-producer.md", "persona-snapshot"]))
    assert ok


def test_provenance_gate_rejects_empty_sources():
    ok, _ = provenance_gate(fm([]))
    assert not ok


def test_resolution_gate_flags_dangling(tmp_path):
    root = tmp_path
    (root / "concepts").mkdir()
    (root / "concepts" / "rdd.md").write_text("x", encoding="utf-8")
    ok, dangling = resolution_gate("Related: [[rdd]] · [[catalyst-optimizer]]", root)
    assert not ok
    assert dangling == ["catalyst-optimizer"]


def test_resolution_gate_passes_when_all_resolve(tmp_path):
    root = tmp_path
    (root / "concepts").mkdir()
    (root / "topics").mkdir()
    (root / "concepts" / "rdd.md").write_text("x", encoding="utf-8")
    (root / "topics" / "spark.md").write_text("x", encoding="utf-8")
    ok, dangling = resolution_gate("[[rdd]] in [[spark]]", root)
    assert ok and dangling == []
