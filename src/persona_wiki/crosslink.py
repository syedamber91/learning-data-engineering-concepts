"""Deterministic cross-persona topic backlinks inside one hub vault.

No LLM, no shared vocabulary file. Two topic slugs match only when their
normalized token sets are EQUAL; anything looser fabricates links between
unrelated topics ('structural-patterns' and 'resilience-patterns' both contain
'pattern'). Links are written vault-root-relative and fully path-qualified,
because the hub already has slug collisions across personas and Obsidian
resolves [[bare-slugs]] in one flat namespace.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import FrozenSet, List, Sequence, Tuple

WIKI_SUBDIR = "wiki/personas"

_STOP = {"and", "or", "the", "of", "in", "a", "an", "for"}
_EXPAND = {
    "hld": ("high", "level", "design"),
    "lld": ("low", "level", "design"),
    "db": ("database",),
    "oo": ("object", "oriented"),
    "auth": ("authentication",),
}
_SPLIT_RE = re.compile(r"[-_\s]+")


def normalize(slug: str) -> FrozenSet[str]:
    """Comparable token set for a topic slug: 'High-Level-Design.md' -> {high, level, design}."""
    stem = slug[:-3] if slug.endswith(".md") else slug
    tokens: List[str] = []
    for tok in _SPLIT_RE.split(stem.lower()):
        if not tok or tok in _STOP:
            continue
        expanded = _EXPAND.get(tok, (tok,))
        for t in expanded:
            tokens.append(t[:-1] if len(t) > 3 and t.endswith("s") else t)
    return frozenset(tokens)


def topic_slugs(hub_root: Path, persona: str) -> List[str]:
    """Real topics/*.md stems for one persona — never a guessed path."""
    d = hub_root / WIKI_SUBDIR / persona / "topics"
    if not d.is_dir():
        return []
    return sorted(p.stem for p in d.glob("*.md"))


def find_matches(sj_topic: str, hub_root: Path,
                 personas: Sequence[str]) -> List[Tuple[str, str]]:
    """(persona, their_slug) for every sibling topic whose normalized set is equal."""
    target = normalize(sj_topic)
    out: List[Tuple[str, str]] = []
    for persona in personas:
        for slug in topic_slugs(hub_root, persona):
            if normalize(slug) == target:
                out.append((persona, slug))
    return out
