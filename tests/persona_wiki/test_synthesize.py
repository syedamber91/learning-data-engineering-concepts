import json
from pathlib import Path

from persona_wiki.storage import parse_note
from persona_wiki.synthesize import (SynthesisResult, build_concept_prompt,
                                     load_raw, synthesize)


def seed_raw(root: Path):
    d = root / "raw" / "kafka"
    d.mkdir(parents=True)
    (d / "apache-kafka-producer.md").write_text(
        "Producers batch records per partition; acks=all waits for ISR.",
        encoding="utf-8")
    (d / "apache-kafka-consumer.md").write_text(
        "Consumers pull; offsets are per group.", encoding="utf-8")
    (d / "_manifest.yaml").write_text("{}", encoding="utf-8")


def scripted_llm(root: Path):
    """Stub LLM keyed on prompt markers, mirroring the real prompt contract."""
    def llm(prompt: str) -> str:
        if "CONCEPT-LIST" in prompt:
            return json.dumps([
                {"slug": "producer-batching", "sources": ["apache-kafka-producer.md"]},
                {"slug": "consumer-pull", "sources": ["apache-kafka-consumer.md"]},
                {"slug": "broken-one", "sources": ["apache-kafka-consumer.md"]},
            ])
        if "CONCEPT-NOTE" in prompt and "broken-one" in prompt:
            return "NOT JSON"                      # per-concept failure path
        if "CONCEPT-NOTE" in prompt:
            return json.dumps({"body": "Mechanism: producers accumulate a batch per partition because ..."})
        if "DEPTH-CHECK" in prompt and "producer-batching" in prompt:
            return json.dumps({"passed": True, "gaps": []})
        if "DEPTH-CHECK" in prompt:
            return json.dumps({"passed": False, "gaps": ["no rebalance mechanism in source"]})
        if "TOPIC-NOTE" in prompt:
            return json.dumps({"comparisons": "push vs pull", "open_questions": "", "synthesis": "Kafka in one thread."})
        raise AssertionError("unexpected prompt")
    return llm


def test_synthesize_end_to_end(tmp_path):
    root = tmp_path
    seed_raw(root)
    res = synthesize(root, "kafka", scripted_llm(root), "2026-07-10")
    assert isinstance(res, SynthesisResult)
    assert sorted(res.written) == ["consumer-pull", "producer-batching"]
    assert res.skipped == ["broken-one"]

    fm, body = parse_note((root / "concepts" / "producer-batching.md").read_text(encoding="utf-8"))
    assert fm.sources == ["raw/kafka/apache-kafka-producer.md"]   # receipt
    assert fm.topics == ["kafka"]
    assert "Mechanism" in body

    tfm, tbody = parse_note((root / "topics" / "kafka.md").read_text(encoding="utf-8"))
    assert "[[producer-batching]]" in tbody and "[[consumer-pull]]" in tbody
    assert "[[broken-one]]" not in tbody                          # no dangling link
    assert "**source gap** ([[consumer-pull]])" in tbody          # depth gap logged
    assert res.source_gaps == {"consumer-pull": ["no rebalance mechanism in source"]}

    assert (root / "log.md").exists()
    assert (root / "index.yaml").exists()


def test_synthesize_quarantines_gate_failure(tmp_path):
    root = tmp_path
    seed_raw(root)

    def bad_sources_llm(prompt: str) -> str:
        if "CONCEPT-LIST" in prompt:
            return json.dumps([{"slug": "ghost", "sources": ["not-a-real-file.md"]}])
        if "TOPIC-NOTE" in prompt:
            return json.dumps({"comparisons": "", "open_questions": "", "synthesis": "s"})
        return json.dumps({"body": "x", "passed": True, "gaps": []})

    res = synthesize(root, "kafka", bad_sources_llm, "2026-07-10")
    assert res.quarantined == ["ghost"]
    assert (root / "_failed" / "ghost.md").exists()
    assert not (root / "concepts" / "ghost.md").exists()


def test_load_raw_excludes_underscore(tmp_path):
    seed_raw(tmp_path)
    raw = load_raw(tmp_path, "kafka")
    assert set(raw) == {"apache-kafka-producer.md", "apache-kafka-consumer.md"}


def test_concept_prompt_contains_sources_verbatim():
    p = build_concept_prompt("producer-batching", {"a.md": "SOURCE TEXT HERE"})
    assert "CONCEPT-NOTE" in p and "SOURCE TEXT HERE" in p and "producer-batching" in p
