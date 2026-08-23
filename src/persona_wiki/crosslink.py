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
from typing import Dict, FrozenSet, List, Sequence, Tuple

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


BACKLINK_PREFIX = "**Also covered by:**"


def backlink_line(persona: str, slug: str) -> str:
    """A vault-root-relative, path-qualified Obsidian link. Never '../', never bare."""
    return f"{BACKLINK_PREFIX} [[{WIKI_SUBDIR}/{persona}/topics/{slug}|{persona}]]"


def apply_backlinks(hub_root: Path, persona: str,
                    personas: Sequence[str]) -> Dict[str, List[str]]:
    """Append one backlink line per genuine match to each of ``persona``'s topic notes.

    Returns {topic_slug: [lines added]} for topics that changed; topics with no
    match, or whose lines are already present, are absent. Run this AFTER all
    synthesis — resolution_gate is single-persona-scoped and would flag a
    cross-persona link as dangling if it ran over this output.
    """
    added: Dict[str, List[str]] = {}
    topics_dir = hub_root / WIKI_SUBDIR / persona / "topics"
    for slug in topic_slugs(hub_root, persona):
        matches = find_matches(slug, hub_root, personas)
        if not matches:
            continue
        path = topics_dir / f"{slug}.md"
        text = path.read_text(encoding="utf-8")
        new = [backlink_line(p, s) for p, s in matches
               if backlink_line(p, s) not in text]
        if not new:
            continue
        path.write_text(text.rstrip("\n") + "\n\n" + "\n".join(new) + "\n",
                        encoding="utf-8")
        added[slug] = new
    return added
