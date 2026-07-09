from pathlib import Path

from persona_wiki.status import stage_status


def note(persona, kind, slug, sources, extra=""):
    src = "\n".join(f"- {s}" for s in sources)
    return (f"---\npersona: {persona}\nkind: {kind}\nslug: {slug}\n"
            f"sources:\n{src}\nlast_updated: '2026-07-10'\n{extra}---\n\nbody")


def test_all_missing(tmp_path):
    s = stage_status(tmp_path / "vutr", tmp_path / "alex", "kafka")
    assert s == {"ingest": "missing", "synthesize": "missing", "learn": "missing"}


def test_current_pipeline(tmp_path):
    root = tmp_path / "vutr"
    (root / "raw" / "kafka").mkdir(parents=True)
    (root / "raw" / "kafka" / "post.md").write_text("x", encoding="utf-8")
    (root / "concepts").mkdir()
    (root / "concepts" / "producer-batching.md").write_text(
        note("vutr", "concept", "producer-batching", ["raw/kafka/post.md"]), encoding="utf-8")
    (root / "topics").mkdir()
    (root / "topics" / "kafka.md").write_text(
        "---\npersona: vutr\nkind: topic\ntopic: kafka\nlast_updated: '2026-07-10'\n---\n\n"
        "Related: [[producer-batching]]", encoding="utf-8")
    learner = tmp_path / "alex"
    (learner / "kafka").mkdir(parents=True)
    (learner / "kafka" / "mastery.md").write_text("Depth mastery: 100% (1/1)", encoding="utf-8")
    s = stage_status(root, learner, "kafka")
    assert s == {"ingest": "current", "synthesize": "current", "learn": "current"}


def test_stale_synthesis_on_snapshot_provenance(tmp_path):
    root = tmp_path / "vutr"
    (root / "raw" / "kafka").mkdir(parents=True)
    (root / "raw" / "kafka" / "post.md").write_text("x", encoding="utf-8")
    (root / "concepts").mkdir()
    (root / "concepts" / "producer-batching.md").write_text(
        note("vutr", "concept", "producer-batching", ["persona-snapshot"]), encoding="utf-8")
    (root / "topics").mkdir()
    (root / "topics" / "kafka.md").write_text(
        "---\npersona: vutr\nkind: topic\ntopic: kafka\nlast_updated: '2026-07-10'\n---\n\n"
        "Related: [[producer-batching]]", encoding="utf-8")
    s = stage_status(root, tmp_path / "alex", "kafka")
    assert s["synthesize"] == "stale"
