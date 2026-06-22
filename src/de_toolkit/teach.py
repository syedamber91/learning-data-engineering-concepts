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


def build_lesson_prompt(sel: Selection) -> str:
    """Assemble the full prompt that produces a single lesson note."""
    payload = json.dumps(sel.concept.model_dump(mode="json"), indent=2)
    return (
        _engine_prompt()
        + "\n\n"
        + "=== YOUR TASK FOR THIS RUN ===\n"
        + "Produce exactly ONE lesson for the concept below, following the LESSON "
        + "TEMPLATE and PRESENTATION CONTRACT above. Output ONLY the vault-ready "
        + "Markdown for the lesson (YAML frontmatter then body). Do not add "
        + "commentary before or after the Markdown. Remember: a named real-world "
        + "use case is mandatory.\n\n"
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
            say(build_lesson_prompt(sel))
            continue
        say(f"Teaching [bold]{sel.concept.title}[/bold]…")
        _write(target, run_claude(build_lesson_prompt(sel), model))
        written.append(target)
        say(f"[green]✓[/green] {target}")

    return written
