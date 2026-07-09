from pathlib import Path

import yaml

from persona_wiki.ingest import ingest, load_include, propose_include


def make_posts(tmp_path: Path) -> Path:
    posts = tmp_path / "posts"
    posts.mkdir()
    (posts / "apache-kafka-producer.md").write_text(
        "# Producer\nKafka producers batch records.", encoding="utf-8")
    (posts / "warpstream-notes.md").write_text(
        "WarpStream reimplements the Kafka protocol on S3.", encoding="utf-8")
    (posts / "50-off-promo.md").write_text("Subscribe now!", encoding="utf-8")
    return posts


def test_propose_include_matches_name_and_body(tmp_path):
    posts = make_posts(tmp_path)
    got = propose_include(posts, ["kafka"])
    assert got == ["apache-kafka-producer.md", "warpstream-notes.md"]


def test_load_include_skips_comments_and_blanks(tmp_path):
    f = tmp_path / "inc.txt"
    f.write_text("# kafka picks\napache-kafka-producer.md\n\nwarpstream-notes.md\n", encoding="utf-8")
    assert load_include(f) == ["apache-kafka-producer.md", "warpstream-notes.md"]


def test_ingest_copies_verbatim_writes_manifest(tmp_path):
    posts = make_posts(tmp_path)
    root = tmp_path / "wiki"
    res = ingest(posts, root, "kafka", ["apache-kafka-producer.md"], "2026-07-10")
    assert res.copied == ["apache-kafka-producer.md"]
    copied = root / "raw" / "kafka" / "apache-kafka-producer.md"
    assert copied.read_text(encoding="utf-8") == (posts / "apache-kafka-producer.md").read_text(encoding="utf-8")
    manifest = yaml.safe_load(res.manifest.read_text(encoding="utf-8"))
    entry = manifest["apache-kafka-producer.md"]
    assert entry["copied"] == "2026-07-10"
    assert entry["source"].endswith("posts/apache-kafka-producer.md")


def test_ingest_is_append_only(tmp_path):
    posts = make_posts(tmp_path)
    root = tmp_path / "wiki"
    ingest(posts, root, "kafka", ["apache-kafka-producer.md"], "2026-07-10")
    # source changes; re-run must NOT overwrite the already-ingested copy
    (posts / "apache-kafka-producer.md").write_text("MUTATED", encoding="utf-8")
    res = ingest(posts, root, "kafka", ["apache-kafka-producer.md"], "2026-07-11")
    assert res.copied == []
    assert res.skipped == ["apache-kafka-producer.md"]
    kept = (root / "raw" / "kafka" / "apache-kafka-producer.md").read_text(encoding="utf-8")
    assert "MUTATED" not in kept


def test_ingest_missing_include_file_errors(tmp_path):
    posts = make_posts(tmp_path)
    root = tmp_path / "wiki"
    try:
        ingest(posts, root, "kafka", ["no-such-post.md"], "2026-07-10")
        assert False, "expected ValueError"
    except ValueError as e:
        assert "no-such-post.md" in str(e)
