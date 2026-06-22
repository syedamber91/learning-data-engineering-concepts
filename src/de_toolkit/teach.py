"""Generate beginner lessons from vault concepts via the Claude Code CLI.

This is the engine behind ``de-toolkit teach``. For each selected concept it
assembles the teaching prompt (``prompts/vault-teaching-engine.md`` plus the
concept's content) and asks the local ``claude`` CLI to write a lesson — so it
uses your existing Claude Code subscription rather than a raw API key.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional

from .config import ROOT_DIR, resolve_vault_dir
from .models import Area, Catalog, Concept, Topic
from .vault import _write, slugify

PROMPT_PATH = ROOT_DIR / "prompts" / "vault-teaching-engine.md"
DEFAULT_VAULT = "learning-vault"


@dataclass
class Selection:
    area: Area
    topic: Topic
    concept: Concept

    def target(self, vault_dir: Path) -> Path:
        return (
            vault_dir
            / slugify(self.area.title)
            / slugify(self.topic.title)
            / f"{slugify(self.concept.title)}.md"
        )


def _engine_prompt() -> str:
    """Load the reusable teaching mega-prompt."""
    if not PROMPT_PATH.exists():
        raise RuntimeError(f"Teaching prompt not found at {PROMPT_PATH}.")
    return PROMPT_PATH.read_text(encoding="utf-8")


def iter_selections(
    catalog: Catalog,
    area: Optional[str] = None,
    topic: Optional[str] = None,
    concept: Optional[str] = None,
) -> Iterator[Selection]:
    """Yield (area, topic, concept) triples matching the case-insensitive filters."""
    def match(value: str, flt: Optional[str]) -> bool:
        return flt is None or value.strip().lower() == flt.strip().lower()

    for a in catalog.areas:
        if not match(a.title, area):
            continue
        for t in a.topics:
            if not match(t.title, topic):
                continue
            for cpt in t.concepts:
                if not match(cpt.title, concept):
                    continue
                yield Selection(a, t, cpt)


LESSON_SKELETON = """\
Output EXACTLY this structure (Markdown), filling every section deeply:

---
title: "<concept title>"
area: "<area>"
topic: "<topic>"
tags: [<4-6 lowercase tags>]
---

# <concept title>

## In one line
## Picture this
## How it actually works
## Worked example
## In the real world
## Common misconceptions
## How it relates & differs
## Why you'd use it (and when not to)
## Check yourself
## Connects to

Rules:
- "Worked example" MUST use real numbers/values and, where the concept allows, a
  short fenced code/SQL/command snippet (```sql, ```bash, ```python).
- "Common misconceptions" lists 2-3 "People think X - actually Y." items.
- "How it relates & differs" names 2-3 neighbouring concepts with [[wikilinks]] and
  explains how this RELATES to and DIFFERS from each (a small contrast table is ideal).
- "Check yourself" has a one-line memory hook then 3 questions, each with its answer.
- "Connects to" is a line of [[wikilinks]].
- Target ~600-1000 words. Reading level: a sharp 15-year-old. Output ONLY the
  Markdown — no commentary before or after, no surrounding code fence.
"""


def _link_guide(catalog: Optional[Catalog], current: Concept) -> str:
    """List the real wikilink targets so the model never invents broken links."""
    if catalog is None:
        return ""
    lines = []
    for a in catalog.areas:
        for t in a.topics:
            for cpt in t.concepts:
                if cpt.title == current.title:
                    continue
                lines.append(f"- {cpt.title}: [[{slugify(cpt.title)}|{cpt.title}]]")
    if not lines:
        return ""
    return (
        "VAULT LINK TARGETS — these are the ONLY notes that exist in this vault.\n"
        "When you cross-reference one (in 'How it relates & differs' or 'Connects "
        "to'), use EXACTLY the wikilink shown. For any concept NOT in this list "
        "(e.g. B-tree, full table scan), mention it in **bold** plain text, never "
        "as a [[wikilink]], so the vault has zero broken links.\n"
        + "\n".join(lines)
        + "\n\n"
    )


def build_lesson_prompt(sel: Selection, catalog: Optional[Catalog] = None) -> str:
    """Assemble the full prompt that produces a single deep lesson note."""
    payload = json.dumps(sel.concept.model_dump(mode="json"), indent=2)
    return (
        _engine_prompt()
        + "\n\n"
        + "=== YOUR TASK FOR THIS RUN ===\n"
        + "Produce exactly ONE deep lesson for the concept below, following the "
        + "LESSON TEMPLATE and PRESENTATION CONTRACT above. All ten sections are "
        + "mandatory — especially the Worked example (with real numbers/snippet), "
        + "Common misconceptions, How it relates & differs, and Check yourself.\n\n"
        + LESSON_SKELETON
        + "\n"
        + _link_guide(catalog, sel.concept)
        + f"Area: {sel.area.title}\n"
        + f"Topic: {sel.topic.title}\n"
        + "Concept (JSON from the vault):\n"
        + payload
        + "\n"
    )


def build_roadmap_prompt(catalog: Catalog) -> str:
    """Assemble the prompt that produces the Phase 1 roadmap / Home note."""
    outline = json.dumps(
        {
            "title": catalog.title,
            "areas": [
                {
                    "title": a.title,
                    "topics": [
                        {"title": t.title,
                         "concepts": [cpt.title for cpt in t.concepts]}
                        for t in a.topics
                    ],
                }
                for a in catalog.areas
            ],
        },
        indent=2,
    )
    return (
        _engine_prompt()
        + "\n\n"
        + "=== YOUR TASK FOR THIS RUN ===\n"
        + "Produce ONLY the Phase 1 ROADMAP as a single vault-ready Markdown file "
        + "named Home. Give an ordered syllabus (areas -> topics -> concepts), a "
        + "recommended learning order with prerequisites, and concrete milestones. "
        + "Link to concepts with [[wikilinks]]. Output only the Markdown.\n\n"
        + "Vault outline (JSON):\n"
        + outline
        + "\n"
    )


def run_claude(prompt: str, model: Optional[str] = None) -> str:
    """Run the local Claude Code CLI in print mode and return its output."""
    if shutil.which("claude") is None:
        raise RuntimeError(
            "The `claude` CLI was not found. Install Claude Code and log in "
            "(it uses your subscription), or use --dry-run to preview the prompt."
        )
    cmd = ["claude", "-p"]
    if model:
        cmd += ["--model", model]
    proc = subprocess.run(
        cmd, input=prompt, text=True, capture_output=True
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"`claude` exited with code {proc.returncode}: {proc.stderr.strip()}"
        )
    return _strip_code_fence(proc.stdout.strip())


def _inject_breadcrumb(markdown: str, area: str, topic: str) -> str:
    """Insert the vault navigation breadcrumb right after the H1 title line."""
    crumb = (
        f"*Part of [[{slugify(topic)}-moc|{topic}]] · "
        f"[[{slugify(area)}-moc|{area}]]*"
    )
    if crumb in markdown:
        return markdown
    lines = markdown.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines[i + 1:i + 1] = ["", crumb]
            return "\n".join(lines)
    # No H1 found — prepend the breadcrumb so navigation still works.
    return crumb + "\n\n" + markdown


def _strip_code_fence(text: str) -> str:
    """Remove a single wrapping ``` / ```markdown fence if the model added one."""
    lines = text.splitlines()
    if lines and lines[0].lstrip().startswith("```"):
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return text


def teach(
    catalog: Catalog,
    vault_path: Optional[str] = None,
    area: Optional[str] = None,
    topic: Optional[str] = None,
    concept: Optional[str] = None,
    model: Optional[str] = None,
    roadmap: bool = False,
    dry_run: bool = False,
    console=None,
) -> list[Path]:
    """Generate lessons for the selected concepts. Returns written file paths.

    With ``dry_run`` nothing is written and no CLI is called; the assembled
    prompt(s) and intended target path(s) are printed instead.
    """
    vault_dir = resolve_vault_dir(vault_path or DEFAULT_VAULT)
    selections = list(iter_selections(catalog, area, topic, concept))
    if not selections:
        raise RuntimeError(
            "No concepts matched your filters (--area/--topic/--concept)."
        )

    written: list[Path] = []

    def say(msg: str) -> None:
        if console is not None:
            console.print(msg)

    if roadmap:
        target = vault_dir / "Home.md"
        if dry_run:
            say(f"[dim]--- ROADMAP -> {target} ---[/dim]")
            say(build_roadmap_prompt(catalog))
        else:
            _write(target, run_claude(build_roadmap_prompt(catalog), model))
            written.append(target)
            say(f"[green]✓[/green] {target}")

    for sel in selections:
        target = sel.target(vault_dir)
        if dry_run:
            say(f"[dim]--- {sel.concept.title} -> {target} ---[/dim]")
            say(build_lesson_prompt(sel, catalog))
            continue
        say(f"Teaching [bold]{sel.concept.title}[/bold]…")
        lesson = run_claude(build_lesson_prompt(sel, catalog), model)
        lesson = _inject_breadcrumb(lesson, sel.area.title, sel.topic.title)
        _write(target, lesson)
        written.append(target)
        say(f"[green]✓[/green] {target}")

    return written
