"""Render the Mermaid diagrams inside a generated lesson into real SVG files.

Obsidian renders ```mermaid blocks natively, but the user wants committed image
files (ByteByteGo-style infographics) that show up reliably on mobile. So after a
lesson is generated we extract every ```mermaid block, render it to an SVG under
``learning-vault/assets/`` with the local ``mermaid-cli`` (provisioned into
``.toolcache/``), and replace the block with an Obsidian image embed.

If the renderer is unavailable, ``rasterize_lesson`` leaves the native ```mermaid
blocks untouched — they still render on the phone — so generation never fails just
because diagrams could not be rasterized.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from .config import ROOT_DIR

# A fenced ```mermaid ... ``` block (non-greedy, multiline).
MERMAID_RE = re.compile(r"```mermaid[ \t]*\n(.*?)\n```", re.DOTALL)

_MMDC = ROOT_DIR / ".toolcache" / "node_modules" / ".bin" / "mmdc"
# Chrome runs as root in the sandbox, so it needs --no-sandbox.
_PUPPETEER_CFG = '{ "args": ["--no-sandbox", "--disable-setuid-sandbox"] }'


def mmdc_available() -> bool:
    """True if the local mermaid-cli binary is present."""
    return _MMDC.exists()


def render_mermaid_to_svg(source: str, out_path: Path) -> bool:
    """Render one Mermaid source string to an SVG file. Returns success."""
    if not mmdc_available():
        return False
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        mmd = Path(tmp) / "d.mmd"
        cfg = Path(tmp) / "pp.json"
        mmd.write_text(source.strip() + "\n", encoding="utf-8")
        cfg.write_text(_PUPPETEER_CFG, encoding="utf-8")
        proc = subprocess.run(
            [str(_MMDC), "-i", str(mmd), "-o", str(out_path),
             "-b", "transparent", "-p", str(cfg)],
            capture_output=True, text=True,
        )
    return proc.returncode == 0 and out_path.exists()


def rasterize_lesson(
    markdown: str,
    concept_slug: str,
    assets_dir: Path,
) -> tuple[str, list[Path], int]:
    """Replace every ```mermaid block with a rendered SVG embed.

    Returns ``(new_markdown, written_svgs, failures)``. When the renderer is
    missing or a render fails, that block is left as native ```mermaid so it
    still displays in Obsidian. Embeds use the filename only — Obsidian resolves
    it anywhere in the vault, and our names are globally unique.
    """
    if not mmdc_available():
        return markdown, [], len(MERMAID_RE.findall(markdown))

    written: list[Path] = []
    failures = 0
    counter = {"n": 0}

    def repl(match: re.Match) -> str:
        nonlocal failures
        counter["n"] += 1
        idx = counter["n"]
        source = match.group(1)
        svg_name = f"{concept_slug}-d{idx}.svg"
        svg_path = assets_dir / svg_name
        if render_mermaid_to_svg(source, svg_path):
            written.append(svg_path)
            # Keep the source in a comment so the diagram can be re-rendered.
            comment = "<!-- mermaid-source:\n" + source.strip() + "\n-->"
            return f"{comment}\n![[{svg_name}]]"
        failures += 1
        return match.group(0)  # leave the native mermaid block in place

    new_markdown = MERMAID_RE.sub(repl, markdown)
    return new_markdown, written, failures
