from persona_wiki.log import _last_logged_total, log_ingest


def test_first_entry_is_backfill(tmp_path):
    log = tmp_path / "log.md"
    appended = log_ingest(log, 14, "3 topic notes, 7 entities, 4 concepts already synthesized", "2026-07-08")
    assert appended is True
    text = log.read_text(encoding="utf-8")
    assert "backfill:" in text and "log started here" in text and "(14 total)" in text


def test_append_on_growth(tmp_path):
    log = tmp_path / "log.md"
    log_ingest(log, 14, "backfill note", "2026-07-08")
    appended = log_ingest(log, 15, "kafka revised (+1 source); +1 entity", "2026-07-09")
    assert appended is True
    assert "(15 total)" in log.read_text(encoding="utf-8")


def test_skip_on_no_change(tmp_path):
    log = tmp_path / "log.md"
    log_ingest(log, 14, "backfill note", "2026-07-08")
    appended = log_ingest(log, 14, "nothing new", "2026-07-09")
    assert appended is False
    assert log.read_text(encoding="utf-8").count("total)") == 1


def test_revision_wording_written_on_change(tmp_path):
    log = tmp_path / "log.md"
    log_ingest(log, 14, "backfill note", "2026-07-08")
    log_ingest(log, 15, "spark revised (+1 source: spark-photon)", "2026-07-10")
    assert "spark revised (+1 source: spark-photon)" in log.read_text(encoding="utf-8")


def test_last_logged_total_none_when_empty(tmp_path):
    assert _last_logged_total(tmp_path / "log.md") is None
