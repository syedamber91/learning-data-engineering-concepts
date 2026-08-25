"""Report slugs a persona shares with its hub siblings. REPORT ONLY -- never renames.

Obsidian resolves [[bare-slugs]] in one flat namespace, so a shared slug is
ambiguous vault-wide. The hub already ships two such collisions (bloom-filters,
redis). Every link this project writes is path-qualified, so new links are
unambiguous; this script exists so pre-existing ambiguity is visible, not silent.
"""

import sys
from pathlib import Path

KINDS = ("topics", "concepts", "entities")


def slugs(hub: Path, persona: str):
    out = {}
    for kind in KINDS:
        for p in (hub / "wiki" / "personas" / persona / kind).glob("*.md"):
            out.setdefault(p.stem, []).append(f"{persona}/{kind}")
    return out


def main(hub: Path, persona: str, siblings):
    mine = slugs(hub, persona)
    theirs = {}
    for s in siblings:
        for slug, where in slugs(hub, s).items():
            theirs.setdefault(slug, []).extend(where)
    hits = sorted(set(mine) & set(theirs))
    print(f"{persona}: {len(mine)} slugs; collisions with {', '.join(siblings)}: {len(hits)}")
    for slug in hits:
        print(f"  {slug}: {' + '.join(mine[slug] + theirs[slug])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), sys.argv[2], sys.argv[3:]))
