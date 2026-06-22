"""Configuration and filesystem paths.

Values come from a local ``.env`` file (see ``.env.example``) with sensible
defaults. Nothing here contains secrets — the toolkit only reads study notes you
already have and writes them into a local (or your real) Obsidian vault.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Project root is two levels up from this file:
# src/de_toolkit/config.py -> repo root
ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output"
VAULT_DIR = ROOT_DIR / "vault"

CONTENT_PATH = DATA_DIR / "content.json"


def _get_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class Settings:
    # Where notes are written by default. Point ``DE_VAULT_PATH`` at your real
    # Obsidian vault to write straight into it (the CLI ``--vault-path`` flag
    # overrides this per run).
    vault_path: str = os.environ.get("DE_VAULT_PATH", str(VAULT_DIR))
    # How many keyword tags to attach to each note.
    max_tags: int = _get_int("DE_MAX_TAGS", 6)
    # How many "Related" notes to surface per note.
    max_related: int = _get_int("DE_MAX_RELATED", 5)


settings = Settings()


def resolve_vault_dir(vault_path: str | os.PathLike[str] | None = None) -> Path:
    """Resolve the vault directory.

    Priority: explicit ``vault_path`` argument (e.g. CLI ``--vault-path``) >
    the ``DE_VAULT_PATH`` setting > the in-repo ``vault/`` directory.
    """
    chosen = vault_path or settings.vault_path
    return Path(chosen).expanduser().resolve()


def ensure_dirs() -> None:
    """Create the local working directories if they don't already exist."""
    for d in (DATA_DIR, OUTPUT_DIR, VAULT_DIR):
        d.mkdir(parents=True, exist_ok=True)
