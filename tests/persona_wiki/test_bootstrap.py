import json

from persona_wiki.bootstrap import bootstrap, parse_persona_sections
from persona_wiki.index import load_index

_MD = """\
## IDENTITY
Vu Trinh writes about data engineering.

## TECHNICAL POSITIONS

### Apache Kafka — Internals
- Kafka was built by LinkedIn.

### Apache Spark — Internals
- Spark was created at UC Berkeley.

## QUESTION GENERATION GUIDELINES
Rules here.
"""


def _bootstrap_llm(prompt):
    return json.dumps({
        "entities": [{"slug": "linkedin", "body": "built kafka"}],
        "concepts": [],
        "comparisons": "",
        "open_questions": "",
        "synthesis": "Grounded synthesis.",
    })


def test_parse_sections_finds_only_technical_positions():
    sections = parse_persona_sections(_MD)
    titles = [t for t, _ in sections]
    assert titles == ["Apache Kafka — Internals", "Apache Spark — Internals"]
    assert "built by LinkedIn" in sections[0][1]


def test_bootstrap_seeds_index_and_backfill_log(tmp_path):
    result = bootstrap(tmp_path, "vutr", _MD, _bootstrap_llm, "2026-07-08")
    assert result["topics"] == 2
    idx = load_index(tmp_path)
    assert "kafka" in idx.topics and "spark" in idx.topics
    log_text = (tmp_path / "log.md").read_text(encoding="utf-8")
    assert "backfill:" in log_text and "log started here" in log_text


_MD_COLLIDING = """\
## TECHNICAL POSITIONS

### Kimball Dimensional Modeling and dbt
- Star schemas and dbt models.

### ETL vs ELT, dbt Adoption, and Data Transformation
- dbt runs transformations in the warehouse.
"""


def test_colliding_slugs_merge_into_one_topic(tmp_path):
    # both sections map to slug 'dbt' — they must merge, not clobber each other
    calls = {"n": 0}

    def counting_llm(prompt):
        calls["n"] += 1
        # each section's text should reach the (single) dbt derive call
        assert "Star schemas" in prompt and "warehouse" in prompt
        return _bootstrap_llm(prompt)

    result = bootstrap(tmp_path, "vutr", _MD_COLLIDING, counting_llm, "2026-07-08")
    assert result["topics"] == 1          # one grouped topic, not two clobbering writes
    assert calls["n"] == 1                # a single derive call over the combined text
    assert "dbt" in load_index(tmp_path).topics


def test_bootstrap_survives_a_failing_section(tmp_path):
    def flaky_llm(prompt):
        if "Kafka" in prompt or "kafka" in prompt:
            raise RuntimeError("claude exited 1")
        return _bootstrap_llm(prompt)

    result = bootstrap(tmp_path, "vutr", _MD, flaky_llm, "2026-07-08")
    # the spark section still lands and the index is saved despite the kafka failure
    assert result["skipped"] == 1
    idx = load_index(tmp_path)
    assert "spark" in idx.topics and "kafka" not in idx.topics
    assert (tmp_path / "index.yaml").exists()
