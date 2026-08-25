"""Stage A feeder for Udemy lecture notes: transform a captured lecture into the
persona wiki's immutable raw/<group>/ layer, routed by a checked-in
lecture_id -> group map. Append-only, like ingest.py, but transforming rather
than copying (ingest.py is a byte-for-byte shutil.copyfile and has no seam for
this)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

from .ingest import MANIFEST, IngestResult
from .storage import slugify

TRANSCRIPT_HEADING = "## Transcript"


def parse_lecture(text: str) -> Tuple[dict, str]:
    """(frontmatter dict, transcript body) for one captured Udemy lecture note.

    Everything before the ``## Transcript`` heading is discarded: it is the H1,
    a ``Part of [[courses/...]]`` breadcrumb and an ``[Open on Udemy]`` link,
    all of which point into a different Obsidian vault.
    """
    if not text.startswith("---"):
        raise ValueError("lecture note has no frontmatter")
    _, front, rest = text.split("---", 2)
    fm = yaml.safe_load(front) or {}
    if TRANSCRIPT_HEADING not in rest:
        raise ValueError(f"lecture note has no '{TRANSCRIPT_HEADING}' section")
    body = rest.split(TRANSCRIPT_HEADING, 1)[1]
    return fm, body.strip()


_LECTURE_ID_RE = re.compile(r"-(\d+)\.md$")


def lecture_id_from_filename(name: str) -> str:
    """The trailing numeric Udemy lecture id: '1-adapter-...-41932990.md' -> '41932990'."""
    m = _LECTURE_ID_RE.search(name)
    if not m:
        raise ValueError(f"no lecture id in filename: {name}")
    return m.group(1)


def load_group_map(path: Path) -> Dict[str, str]:
    """lecture_id -> group slug, flattened from the YAML's nested ``groups:`` block."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out: Dict[str, str] = {}
    for group, ids in (data.get("groups") or {}).items():
        for lecture_id in ids or []:
            key = str(lecture_id)
            if key in out:
                raise ValueError(
                    f"lecture id {key} listed in both '{out[key]}' and '{group}'")
            out[key] = group
    return out


INSTRUCTOR = "Shrayansh Jain"

_FM_ORDER = ("title", "instructor", "course", "section",
             "lecture_id", "url", "duration", "captured_at")


@dataclass
class UdemyIngestResult(IngestResult):
    """IngestResult plus the lecture ids the group map does not route."""
    unmapped: List[str] = field(default_factory=list)


def render_raw_note(fm: dict, body: str, lecture_id: str) -> str:
    """The raw/ note: provenance frontmatter + the transcript, nothing else."""
    kept = {
        "title": fm.get("title", ""),
        "instructor": INSTRUCTOR,
        "course": fm.get("course", ""),
        "section": fm.get("section", ""),
        "lecture_id": lecture_id,
        "url": fm.get("url", ""),
        "duration": fm.get("duration", ""),
        "captured_at": str(fm.get("captured_at", "")),
    }
    lines = [f'{k}: "{kept[k]}"' for k in _FM_ORDER if kept[k]]
    front = "\n".join(lines)
    return f"---\n{front}\n---\n\n# {kept['title']}\n\n{body}\n"


def ingest_udemy(course_dir: Path, root: Path, group_map: Dict[str, str],
                 stamp: str) -> UdemyIngestResult:
    """Transform every lecture in ``course_dir`` into ``root/raw/<group>/``.

    Idempotent: a lecture is skipped when its id is already in the group's
    manifest OR when the destination file exists. Never overwrites — the raw
    layer is immutable. An id absent from ``group_map`` is reported, not copied.
    """
    res = UdemyIngestResult(manifest=root / "raw")
    manifests: Dict[str, Dict[str, dict]] = {}

    def manifest_for(group: str) -> Dict[str, dict]:
        if group not in manifests:
            path = root / "raw" / group / MANIFEST
            manifests[group] = (
                yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                if path.exists() else {})
        return manifests[group]

    for src in sorted(course_dir.glob("*.md")):
        lecture_id = lecture_id_from_filename(src.name)
        group = group_map.get(lecture_id)
        if group is None:
            res.unmapped.append(lecture_id)
            continue

        manifest = manifest_for(group)
        if any(e.get("lecture_id") == lecture_id for e in manifest.values()):
            res.skipped.append(lecture_id)
            continue

        fm, body = parse_lecture(src.read_text(encoding="utf-8"))
        name = f"{slugify(fm.get('title', lecture_id))}.md"
        raw_dir = root / "raw" / group
        raw_dir.mkdir(parents=True, exist_ok=True)
        dst = raw_dir / name
        if dst.exists():
            res.skipped.append(lecture_id)
            continue

        dst.write_text(render_raw_note(fm, body, lecture_id), encoding="utf-8")
        manifest[name] = {"source": str(src), "copied": stamp,
                          "lecture_id": lecture_id}
        res.copied.append(name)

    for group, manifest in manifests.items():
        (root / "raw" / group).mkdir(parents=True, exist_ok=True)
        (root / "raw" / group / MANIFEST).write_text(
            yaml.safe_dump(manifest, sort_keys=True, allow_unicode=True),
            encoding="utf-8")
    return res
