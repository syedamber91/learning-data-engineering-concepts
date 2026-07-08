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
