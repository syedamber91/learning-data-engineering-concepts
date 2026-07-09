"""Stage A feeder: copy captured posts into the persona wiki's immutable
raw/<topic>/ layer, with an auditable manifest. Append-only by design."""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

import yaml

MANIFEST = "_manifest.yaml"


@dataclass
class IngestResult:
    copied: List[str] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)
    manifest: Path = Path()


def propose_include(posts_dir: Path, keywords: List[str]) -> List[str]:
    """Candidate post filenames whose name OR body matches any keyword."""
    kws = [k.lower() for k in keywords]
    out = []
    for p in sorted(posts_dir.glob("*.md")):
        hay = (p.name + "\n" + p.read_text(encoding="utf-8", errors="ignore")).lower()
        if any(k in hay for k in kws):
            out.append(p.name)
    return out


def load_include(path: Path) -> List[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]


def ingest(posts_dir: Path, root: Path, topic: str,
           include: List[str], stamp: str) -> IngestResult:
    """Copy each included post into root/raw/<topic>/ (never overwriting),
    recording provenance in _manifest.yaml."""
    raw_dir = root / "raw" / topic
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = raw_dir / MANIFEST
    manifest: Dict[str, dict] = {}
    if manifest_path.exists():
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}

    res = IngestResult(manifest=manifest_path)
    for name in include:
        src = posts_dir / name
        if not src.exists():
            raise ValueError(f"include-listed post not found: {name}")
        dst = raw_dir / name
        if dst.exists():
            res.skipped.append(name)          # append-only: never overwrite
            continue
        shutil.copyfile(src, dst)
        manifest[name] = {"source": str(src), "copied": stamp}
        res.copied.append(name)

    manifest_path.write_text(
        yaml.safe_dump(manifest, sort_keys=True, allow_unicode=True), encoding="utf-8")
    return res
