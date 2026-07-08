"""Read/write persona-wiki notes as YAML-frontmatter Markdown, guarded so no
write ever escapes the persona-wiki root."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import yaml

from de_toolkit.vault import slugify  # re-exported for callers

from .models import NoteFrontmatter

__all__ = ["slugify", "dump_note", "parse_note", "write_note"]


def dump_note(fm: NoteFrontmatter, body: str) -> str:
    """Serialize frontmatter + body into a Markdown note."""
    data = {k: v for k, v in fm.model_dump().items() if v not in (None, [], "")}
    front = yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{front}\n---\n\n{body.strip()}\n"


def parse_note(text: str) -> Tuple[NoteFrontmatter, str]:
    """Inverse of :func:`dump_note`."""
    if not text.startswith("---"):
        raise ValueError("note has no frontmatter")
    _, front, body = text.split("---", 2)
    fm = NoteFrontmatter.model_validate(yaml.safe_load(front) or {})
    return fm, body.strip()


def write_note(root: Path, rel_path: str, fm: NoteFrontmatter, body: str) -> Path:
    """Write a note at ``root/rel_path``, rejecting any path outside ``root``."""
    root = root.resolve()
    target = (root / rel_path).resolve()
    if root != target and root not in target.parents:
        raise ValueError(f"refusing to write outside persona-wiki root: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dump_note(fm, body), encoding="utf-8")
    return target
