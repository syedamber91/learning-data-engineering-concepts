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
