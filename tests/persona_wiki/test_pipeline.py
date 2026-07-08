import json

from persona_wiki.index import has_topic, load_index
from persona_wiki.pipeline import Source, update

_BUNDLE = json.dumps({
    "entities": [{"slug": "lsm-tree", "body": "LSM body"}],
    "concepts": [],
    "comparisons": "SMJ vs SHJ",
    "open_questions": "- why?",
    "synthesis": "Kafka is write-optimized.",
})


def _derive_then_pass_llm(prompt):
    # QC prompts contain the word "fact-checker"; everything else is a derive call.
    if "fact-checker" in prompt:
        return '{"passed": true, "reason": "ok"}'
    return _BUNDLE


def _derive_then_fail_llm(prompt):
    if "fact-checker" in prompt:
        return '{"passed": false, "reason": "overreach"}'
    return _BUNDLE


def _broken_llm(prompt):
    if "fact-checker" in prompt:
        return '{"passed": true, "reason": "ok"}'
    return "NOT JSON"


def test_pipeline_creates_and_registers(tmp_path):
    src = Source(id="substack/vutr/kafka-internals", text="Kafka commit log internals.")
    result = update(tmp_path, "vutr", [src], _derive_then_pass_llm, "2026-07-08")
    assert result["failed"] == 0 and result["logged"] is True
    idx = load_index(tmp_path)
    assert has_topic(idx, "kafka")
    assert (tmp_path / "topics/kafka.md").exists()


def test_qc_failure_excludes_from_index(tmp_path):
    src = Source(id="s1", text="Kafka internals.")
    update(tmp_path, "vutr", [src], _derive_then_fail_llm, "2026-07-08")
    idx = load_index(tmp_path)
    # note written to disk but not blessed into the index
    assert (tmp_path / "topics/kafka.md").exists()
    assert not has_topic(idx, "kafka")
    fm_text = (tmp_path / "topics/kafka.md").read_text(encoding="utf-8")
    assert "qc: failed" in fm_text


def test_broken_llm_counts_failure_no_partial(tmp_path):
    src = Source(id="s1", text="Kafka internals.")
    result = update(tmp_path, "vutr", [src], _broken_llm, "2026-07-08")
    assert result["failed"] == 1
    assert not (tmp_path / "topics/kafka.md").exists()


def test_idempotent_rerun_no_duplicate_log(tmp_path):
    src = Source(id="s1", text="Kafka internals.")
    update(tmp_path, "vutr", [src], _derive_then_pass_llm, "2026-07-08")
    second = update(tmp_path, "vutr", [src], _derive_then_pass_llm, "2026-07-09")
    # total unchanged -> no new log line
    assert second["logged"] is False


def test_source_without_topic_is_skipped(tmp_path):
    src = Source(id="s1", text="gardening tips and nothing technical")
    result = update(tmp_path, "vutr", [src], _derive_then_pass_llm, "2026-07-08")
    assert result["written"] == 0 and result["failed"] == 0
