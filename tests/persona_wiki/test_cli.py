from typer.testing import CliRunner

from persona_wiki.cli import app

runner = CliRunner()


def test_help_lists_commands():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "bootstrap" in result.output
    assert "update" in result.output
    assert "query" in result.output


def test_query_on_empty_wiki_reports_no_match(tmp_path):
    result = runner.invoke(app, ["query", "kafka", "--vault-dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "No matching" in result.output


def test_bootstrap_dry_run_calls_no_llm(tmp_path):
    # seed a persona snapshot the dry-run can read
    (tmp_path / "data" / "personas").mkdir(parents=True)
    (tmp_path / "data" / "personas" / "vutr.md").write_text(
        "## TECHNICAL POSITIONS\n\n### Apache Kafka\n- built by LinkedIn\n",
        encoding="utf-8",
    )
    result = runner.invoke(
        app, ["bootstrap", "--vault-dir", str(tmp_path), "--dry-run"]
    )
    assert result.exit_code == 0
    assert "Apache Kafka" in result.output  # printed the section it would process


def test_cli_ingest_propose_and_copy(tmp_path):
    posts = tmp_path / "posts"; posts.mkdir()
    (posts / "apache-kafka-producer.md").write_text("kafka", encoding="utf-8")
    inc = tmp_path / "inc.txt"; inc.write_text("apache-kafka-producer.md\n", encoding="utf-8")
    r = runner.invoke(app, ["ingest", "--persona", "vutr", "--topic", "kafka",
                            "--posts-dir", str(posts), "--include", str(inc),
                            "--vault-dir", str(tmp_path)])
    assert r.exit_code == 0, r.output
    assert (tmp_path / "wiki/personas/vutr/raw/kafka/apache-kafka-producer.md").exists()
    r2 = runner.invoke(app, ["ingest", "--persona", "vutr", "--topic", "kafka",
                             "--posts-dir", str(posts), "--propose", "kafka",
                             "--vault-dir", str(tmp_path)])
    assert "apache-kafka-producer.md" in r2.output


def test_cli_status(tmp_path):
    r = runner.invoke(app, ["status", "--persona", "vutr", "--learner", "alex",
                            "--topic", "kafka", "--vault-dir", str(tmp_path)])
    assert r.exit_code == 0
    assert "ingest: missing" in r.output


LECTURE_MIN = '''---
title: "SQL vs NoSQL"
course: "System Design (LLD + HLD) from Basics to Advanced"
section: "HLD(High Level Design)"
url: "https://www.udemy.com/course/x/learn/lecture/41910228"
duration: "00:20:00"
captured_at: 2026-08-22T06:02:45+00:00
---

# SQL vs NoSQL

## Transcript

[00:00:00] Let us compare SQL and NoSQL.
'''


def test_cli_ingest_udemy_routes_and_is_idempotent(tmp_path):
    course = tmp_path / "course"; course.mkdir()
    (course / "2-sql-vs-nosql-41910228.md").write_text(LECTURE_MIN, encoding="utf-8")
    gm = tmp_path / "groups.yaml"
    gm.write_text('groups:\n  databases:\n    - 41910228\n', encoding="utf-8")

    args = ["ingest-udemy", "--persona", "sj", "--course-dir", str(course),
            "--group-map", str(gm), "--vault-dir", str(tmp_path)]
    r = runner.invoke(app, args)
    assert r.exit_code == 0, r.output
    assert (tmp_path / "wiki/personas/sj/raw/databases/sql-vs-nosql.md").exists()
    assert "copied 1" in r.output

    r2 = runner.invoke(app, args)
    assert r2.exit_code == 0, r2.output
    assert "copied 0" in r2.output and "skipped 1" in r2.output


def test_cli_ingest_udemy_reports_unmapped(tmp_path):
    course = tmp_path / "course"; course.mkdir()
    (course / "2-sql-vs-nosql-41910228.md").write_text(LECTURE_MIN, encoding="utf-8")
    gm = tmp_path / "groups.yaml"
    gm.write_text('groups:\n  databases:\n    - 99999999\n', encoding="utf-8")
    r = runner.invoke(app, ["ingest-udemy", "--persona", "sj", "--course-dir", str(course),
                            "--group-map", str(gm), "--vault-dir", str(tmp_path)])
    assert r.exit_code == 0, r.output
    assert "unmapped 1" in r.output
    assert "41910228" in r.output


def test_cli_crosslink_adds_line_for_match(tmp_path):
    for persona in ("sj", "lucsystemdesign"):
        d = tmp_path / "wiki" / "personas" / persona / "topics"
        d.mkdir(parents=True)
        (d / "databases.md").write_text("---\nkind: topic\n---\n\nbody\n",
                                        encoding="utf-8")
    r = runner.invoke(app, ["crosslink", "--persona", "sj",
                            "--against", "lucsystemdesign",
                            "--vault-dir", str(tmp_path)])
    assert r.exit_code == 0, r.output
    assert "databases" in r.output
    text = (tmp_path / "wiki/personas/sj/topics/databases.md").read_text(encoding="utf-8")
    assert "[[wiki/personas/lucsystemdesign/topics/databases|lucsystemdesign]]" in text


def test_cli_crosslink_reports_nothing_when_no_match(tmp_path):
    d = tmp_path / "wiki" / "personas" / "sj" / "topics"
    d.mkdir(parents=True)
    (d / "structural-patterns.md").write_text("---\nkind: topic\n---\n\nbody\n",
                                              encoding="utf-8")
    r = runner.invoke(app, ["crosslink", "--persona", "sj",
                            "--against", "lucsystemdesign",
                            "--vault-dir", str(tmp_path)])
    assert r.exit_code == 0, r.output
    assert "0 topic(s)" in r.output
