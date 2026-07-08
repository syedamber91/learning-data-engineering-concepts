"""Paths and configuration for the persona wiki.

Output lives under ``<vault>/wiki/personas/<persona>/`` — the learning-vault's
existing synthesized-layer namespace. Nothing here writes outside that subtree.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

WIKI_SUBDIR = "wiki/personas"


def resolve_vault_dir(vault_dir: Optional[str] = None) -> Path:
    """Vault root: explicit arg > ``PERSONA_WIKI_DIR`` env > repo root."""
    chosen = vault_dir or os.environ.get("PERSONA_WIKI_DIR")
    if chosen:
        return Path(chosen).expanduser().resolve()
    # repo root = two levels up from src/persona_wiki/config.py
    return Path(__file__).resolve().parents[2]


def persona_root(vault_dir: Path, persona: str) -> Path:
    """Directory holding one persona's wiki (topics/, entities/, concepts/, ...)."""
    return vault_dir / WIKI_SUBDIR / persona
