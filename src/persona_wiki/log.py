"""Append-only CDC log for the persona wiki (the 4-shape ``_log_ingest`` contract)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

_TOTAL_RE = re.compile(r"\((\d+) total\)")
_HEADER = "# Persona Wiki Log\n\nAppend-only change history.\n"


def _last_logged_total(log_path: Path) -> Optional[int]:
    """Prior total parsed from the last logged entry, or None if no entries yet."""
    if not log_path.exists():
        return None
    matches = _TOTAL_RE.findall(log_path.read_text(encoding="utf-8"))
    return int(matches[-1]) if matches else None


def log_ingest(log_path: Path, total: int, summary: str, stamp: str) -> bool:
    """Append a log line if the total changed. Returns True when a line was written."""
    prior = _last_logged_total(log_path)
    if prior is None:
        line = f"- {stamp} — backfill: {summary} (log started here) ({total} total)\n"
        header = _HEADER + "\n" if not log_path.exists() else ""
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(header + line)
        return True
    if total == prior:
        return False
    line = f"- {stamp} — {summary} ({total} total)\n"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(line)
    return True
