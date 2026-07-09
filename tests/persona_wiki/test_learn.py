import json as _json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from persona_wiki.cli import app
from persona_wiki.models import NoteFrontmatter
from persona_wiki.storage import write_note, parse_note as _pn
from persona_wiki.learn import (
    SPARK_ORDER, load_topic_concepts, concept_order,
    build_teach_prompt, build_reflect_prompt, build_answer_prompt, build_score_prompt,
    parse_json, run_concept, ConceptResult,
    render_concept_body, write_concept_note, write_qa_note,
    _safe_write, append_open_questions, write_mastery, upsert_transcript, learn,
)

_runner = CliRunner()


# ---- Task 1: order + loader -------------------------------------------------

def _seed_vutr(tmp_path):
    root = tmp_path / "wiki/personas/vutr"
    for slug, topics, body in [
        ("rdd", ["spark"], "An RDD is a resilient distributed dataset."),
        ("kafka-origin", ["kafka"], "Kafka came from LinkedIn."),
        ("brand-new", ["spark"], "A spark thing not in the static order."),
    ]:
        write_note(root, f"entities/{slug}.md",
                   NoteFrontmatter(persona="vutr", kind="entity", slug=slug,
                                   sources=["persona-snapshot"], last_updated="2026-07-09",
                                   topics=topics), body)
    return root


def test_frontmatter_has_learner_fields():
    fm = NoteFrontmatter(persona="alex", kind="concept", slug="rdd",
                         last_updated="2026-07-09", learner="alex",
                         source_note="rdd", mastery="mastered")
    assert fm.learner == "alex" and fm.source_note == "rdd" and fm.mastery == "mastered"


def test_load_topic_concepts_only_that_topic(tmp_path):
    root = _seed_vutr(tmp_path)
    got = load_topic_concepts(root, "spark")
    assert set(got) == {"rdd", "brand-new"}
    assert "resilient distributed dataset" in got["rdd"]


def test_concept_order_uses_static_then_appends_unknowns(tmp_path):
    root = _seed_vutr(tmp_path)
    order = concept_order(load_topic_concepts(root, "spark"))
    assert order[0] == "rdd"
    assert order[-1] == "brand-new"
    assert "spark-origin" not in order


def test_spark_order_is_16_unique_slugs():
    assert len(SPARK_ORDER) == 16 and len(set(SPARK_ORDER)) == 16


# ---- Task 2: prompts + parse ------------------------------------------------

def test_teach_prompt_is_closed_book_and_15yo():
    p = build_teach_prompt("rdd", "An RDD has 5 properties.")
    assert "An RDD has 5 properties." in p
    assert "15-year-old" in p or "15 year old" in p
    assert "only" in p.lower() and "mermaid" in p.lower()


def test_reflect_prompt_asks_for_restatement_and_questions_json():
    p = build_reflect_prompt("rdd", "EXPLANATION HERE")
    assert "EXPLANATION HERE" in p
    assert "restatement" in p and "questions" in p and "mermaid" in p


def test_answer_prompt_carries_questions_and_note():
    p = build_answer_prompt("rdd", "NOTE TEXT", ["why lazy?", "what is a DAG?"])
    assert "NOTE TEXT" in p and "why lazy?" in p and "gaps" in p


def test_score_prompt_asks_for_level_and_unverified():
    p = build_score_prompt("rdd", "NOTE", "RESTATEMENT")
    assert "RESTATEMENT" in p and "NOTE" in p
    assert "mastered" in p and "unverified" in p


def test_parse_json_tolerates_fence_and_raises_on_garbage():
    assert parse_json('```json\n{"level": "mastered"}\n```')["level"] == "mastered"
    with pytest.raises(ValueError):
        parse_json("not json")


# ---- Task 3: run_concept ----------------------------------------------------

def _fake_llm(explanation="RDDs are lazy.", level="mastered", questions=("why lazy?",),
              mermaid="graph TD; A-->B", gaps=(), unverified=()):
    def llm(prompt):
        if "judging whether Alex" in prompt:
            return _json.dumps({"level": level, "reason": "covered it",
                                "unverified": list(unverified)})
        if "answering Alex's follow-ups" in prompt:
            return _json.dumps({"answers": ["because it builds a DAG"], "gaps": list(gaps)})
        if "You are Alex" in prompt:
            return _json.dumps({"restatement": "RDD = lazy dataset",
                                "questions": list(questions), "mermaid": mermaid})
        return explanation
    return llm


def test_run_concept_assembles_result():
    r = run_concept("rdd", "An RDD is lazy.", _fake_llm())
    assert isinstance(r, ConceptResult)
    assert r.level == "mastered" and r.restatement == "RDD = lazy dataset"
    assert r.questions == ["why lazy?"] and r.mermaid == "graph TD; A-->B"
    assert r.answers == ["because it builds a DAG"]


def test_run_concept_raises_on_bad_json():
    def llm(prompt):
        if "You are Alex" in prompt:
            return "NOT JSON"
        return "explanation"
    with pytest.raises(ValueError):
        run_concept("rdd", "note", llm)


# ---- Task 4: concept + qa notes ---------------------------------------------

def _result(mermaid="graph TD; A-->B"):
    return ConceptResult(slug="rdd", explanation="e", restatement="An RDD is a lazy dataset.",
                         questions=["why lazy?"], mermaid=mermaid, answers=["builds a DAG"],
                         gaps=[], unverified=[], level="mastered", reason="ok")


def test_concept_body_includes_mermaid_and_source():
    body = render_concept_body(_result())
    assert "An RDD is a lazy dataset." in body
    assert "```mermaid" in body and "graph TD; A-->B" in body
    assert "[[rdd]]" in body


def test_concept_body_omits_empty_mermaid_fence():
    body = render_concept_body(_result(mermaid=""))
    assert "```mermaid" not in body
    assert "[[rdd]]" in body


def test_write_concept_note_frontmatter_provenance(tmp_path):
    p = write_concept_note(tmp_path, "spark", _result(), "2026-07-09")
    assert p == tmp_path / "concepts/rdd.md"
    fm, _ = _pn(p.read_text(encoding="utf-8"))
    assert fm.learner == "alex" and fm.source_note == "rdd" and fm.mastery == "mastered"
    assert fm.persona == "alex" and fm.kind == "concept" and fm.topics == ["spark"]


def test_write_qa_note_is_numbered(tmp_path):
    p = write_qa_note(tmp_path, 2, _result(), "2026-07-09")
    assert p == tmp_path / "qa/002-rdd.md"
    text = p.read_text(encoding="utf-8")
    assert "why lazy?" in text and "builds a DAG" in text


# ---- Task 5: open-questions + mastery ---------------------------------------

def test_safe_write_rejects_escape(tmp_path):
    with pytest.raises(ValueError):
        _safe_write(tmp_path, "../escape.md", "x")


def test_append_open_questions_records_gaps_and_unverified(tmp_path):
    r = ConceptResult(slug="rdd", explanation="e", restatement="r",
                      gaps=["what tunes shuffle partitions?"],
                      unverified=["RDDs are always cached"], level="familiar")
    append_open_questions(tmp_path, r, "2026-07-09")
    text = (tmp_path / "open-questions.md").read_text(encoding="utf-8")
    assert "what tunes shuffle partitions?" in text
    assert "unverified" in text.lower() and "RDDs are always cached" in text


def test_write_mastery_table_and_percent(tmp_path):
    order = ["spark-origin", "rdd", "lazy-evaluation", "catalyst-optimizer"]
    levels = {"spark-origin": "mastered", "rdd": "mastered",
              "lazy-evaluation": "familiar", "catalyst-optimizer": "mastered"}
    p = write_mastery(tmp_path, order, levels, "2026-07-09")
    text = p.read_text(encoding="utf-8")
    assert "| rdd | mastered |" in text
    assert "75%" in text and "3 mastered / 4" in text


# ---- Task 6: transcript -----------------------------------------------------

def test_transcript_section_and_no_duplicate(tmp_path):
    r = ConceptResult(slug="rdd", explanation="RDDs are lazy.", restatement="RDD = lazy",
                      questions=["why lazy?"], answers=["builds a DAG"], mermaid="graph TD;A-->B",
                      level="mastered", reason="covered it")
    upsert_transcript(tmp_path, 2, r)
    upsert_transcript(tmp_path, 2, r)
    text = (tmp_path / "transcript.md").read_text(encoding="utf-8")
    assert text.count("## 2. rdd") == 1
    assert "RDDs are lazy." in text and "RDD = lazy" in text
    assert "builds a DAG" in text and "Verdict:" in text
    assert "Diagram added: yes" in text


# ---- Task 7: learn() loop ---------------------------------------------------

def _vutr_two(tmp_path):
    root = tmp_path / "wiki/personas/vutr"
    for slug in ("rdd", "spark-origin"):
        write_note(root, f"entities/{slug}.md",
                   NoteFrontmatter(persona="vutr", kind="entity", slug=slug,
                                   sources=["persona-snapshot"], last_updated="2026-07-09",
                                   topics=["spark"]), f"Note about {slug}.")
    return root


def _llm_all_mastered():
    def llm(prompt):
        if "judging whether Alex" in prompt:
            return _json.dumps({"level": "mastered", "reason": "ok", "unverified": []})
        if "answering Alex's follow-ups" in prompt:
            return _json.dumps({"answers": ["a"], "gaps": []})
        if "You are Alex" in prompt:
            return _json.dumps({"restatement": "got it", "questions": ["why?"], "mermaid": ""})
        return "explanation"
    return llm


def test_learn_masters_all_and_writes_artifacts(tmp_path):
    vutr = _vutr_two(tmp_path)
    learn_root = tmp_path / "wiki/personas/alex/spark"
    res = learn(learn_root, vutr, "spark", _llm_all_mastered(), "2026-07-09")
    assert res == {"total": 2, "mastered": 2, "pct": 100, "failed": 0}
    assert (learn_root / "concepts/rdd.md").exists()
    assert (learn_root / "concepts/spark-origin.md").exists()
    assert (learn_root / "mastery.md").exists() and (learn_root / "transcript.md").exists()
    assert (learn_root / "index.yaml").exists() and (learn_root / "log.md").exists()
    tr = (learn_root / "transcript.md").read_text(encoding="utf-8")
    assert tr.index("## 1. spark-origin") < tr.index("## 2. rdd")


def test_learn_retry_cap_records_best_level(tmp_path):
    vutr = _vutr_two(tmp_path)
    learn_root = tmp_path / "wiki/personas/alex/spark"

    def stubborn(prompt):
        if "judging whether Alex" in prompt:
            return _json.dumps({"level": "familiar", "reason": "partial", "unverified": []})
        if "answering Alex's follow-ups" in prompt:
            return _json.dumps({"answers": ["a"], "gaps": []})
        if "You are Alex" in prompt:
            return _json.dumps({"restatement": "sort of", "questions": [], "mermaid": ""})
        return "explanation"

    res = learn(learn_root, vutr, "spark", stubborn, "2026-07-09", max_retries=1)
    assert res["mastered"] == 0 and res["total"] == 2 and res["pct"] == 0
    assert "familiar" in (learn_root / "mastery.md").read_text(encoding="utf-8")


def test_learn_skips_already_mastered_on_rerun(tmp_path):
    vutr = _vutr_two(tmp_path)
    learn_root = tmp_path / "wiki/personas/alex/spark"
    learn(learn_root, vutr, "spark", _llm_all_mastered(), "2026-07-09")

    calls = {"n": 0}
    def counting(prompt):
        calls["n"] += 1
        return _llm_all_mastered()(prompt)
    res = learn(learn_root, vutr, "spark", counting, "2026-07-10")
    assert calls["n"] == 0 and res["mastered"] == 2


def test_learn_counts_failure_and_continues(tmp_path):
    vutr = _vutr_two(tmp_path)
    learn_root = tmp_path / "wiki/personas/alex/spark"

    def flaky(prompt):
        if "spark-origin" in prompt and "You are Alex" in prompt:
            return "NOT JSON"
        return _llm_all_mastered()(prompt)
    res = learn(learn_root, vutr, "spark", flaky, "2026-07-09", max_retries=1)
    assert res["failed"] >= 1 and res["mastered"] == 1
    assert (learn_root / "concepts/rdd.md").exists()
    assert not (learn_root / "concepts/spark-origin.md").exists()


# ---- Task 8: CLI ------------------------------------------------------------

def test_cli_learn_dry_run_lists_order_no_llm(tmp_path):
    root = tmp_path / "wiki/personas/vutr"
    for slug in ("rdd", "spark-origin"):
        write_note(root, f"entities/{slug}.md",
                   NoteFrontmatter(persona="vutr", kind="entity", slug=slug,
                                   sources=["persona-snapshot"], last_updated="2026-07-09",
                                   topics=["spark"]), f"Note {slug}.")
    res = _runner.invoke(app, ["learn", "--from", "vutr", "--topic", "spark",
                               "--vault-dir", str(tmp_path), "--dry-run"])
    assert res.exit_code == 0
    assert "spark-origin" in res.output and "rdd" in res.output
    assert not (tmp_path / "wiki/personas/alex/spark/mastery.md").exists()


def test_cli_learn_help_lists_command():
    res = _runner.invoke(app, ["--help"])
    assert res.exit_code == 0 and "learn" in res.output


def test_topic_order_reads_related_line(tmp_path):
    from persona_wiki.learn import topic_order
    (tmp_path / "topics").mkdir()
    (tmp_path / "topics" / "kafka.md").write_text(
        "---\npersona: vutr\nkind: topic\nlast_updated: '2026-07-10'\n---\n\n"
        "Related: [[broker-log]] · [[producer-batching]] · [[consumer-pull]]\n\n## Synthesis\nx",
        encoding="utf-8")
    assert topic_order(tmp_path, "kafka") == ["broker-log", "producer-batching", "consumer-pull"]


def test_topic_order_missing_note_is_empty(tmp_path):
    from persona_wiki.learn import topic_order
    assert topic_order(tmp_path, "kafka") == []


def test_concept_order_with_preferred():
    from persona_wiki.learn import concept_order
    avail = {"consumer-pull": "a", "broker-log": "b", "zz-extra": "c"}
    assert concept_order(avail, ["broker-log", "consumer-pull", "not-there"]) == \
        ["broker-log", "consumer-pull", "zz-extra"]
