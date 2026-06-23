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
from .diagrams import mmdc_available, rasterize_lesson
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
Output EXACTLY this shape (Markdown), as ONE flowing lesson that climbs in levels:

---
title: "<concept title>"
area: "<area>"
topic: "<topic>"
tags: [<4-6 lowercase tags>]
---

# <concept title>

## Recap — where we just were
## Level 1 — The big idea
## Level 2 — How it actually works
## Level 3 — See it with real numbers
## Level 4 — In the real world & common traps
## Level 5 — Expert view
<add Level 6 / Level 7 ONLY for genuinely hard concepts; a simple concept may stop at Level 3 or 4>
## Check yourself
## Connects to
## Coming up next

Rules:
- LEVELS ARE A LADDER. Level 1 is the first, gentlest intuition; each level goes one
  step deeper and EXPLICITLY builds on the one before ("Now that you've seen…"). The
  TOP level is genuinely expert-grade. Use as many levels as the concept needs (3 for
  simple, up to 7 for hard) — do not pad, do not stop short.
- DIAGRAMS ARE MANDATORY. Include several SIMPLE ```mermaid diagrams (e.g. `graph LR`,
  `graph TD`, `sequenceDiagram`) — at least one in Level 1 and one in Level 2, plus
  more wherever a picture explains flow better than words. Keep them small and clearly
  labelled (think ByteByteGo: boxes and arrows showing how things flow). Prefer
  `graph LR`/`graph TD`. Do NOT put quotes, semicolons, or markdown inside node text.
- "Recap — where we just were" is 1-2 sentences bridging from the PREVIOUS lesson the
  learner just finished (named below). For the very first lesson, frame the whole
  course instead.
- Level 3 MUST use real numbers/values and a short fenced code/SQL/command snippet
  (```sql, ```bash, ```python) showing input -> steps -> result.
- Level 4 names a real, concrete use case AND lists 2-3 "People think X - actually Y."
  misconceptions.
- The expert level(s) cover how this RELATES TO and DIFFERS FROM 2-3 neighbouring
  concepts (a small contrast table is ideal), plus trade-offs and edge cases.
- "Check yourself" has a one-line memory hook then 3 questions, each with its answer.
- "Connects to" is a line of [[wikilinks]]. "Coming up next" points to the NEXT
  concept (named below) with its [[wikilink]] and one sentence on why it follows.
- Target ~1200-2000 words. Reading level: a sharp 15-year-old. Output ONLY the
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


def build_lesson_prompt(
    sel: Selection,
    catalog: Optional[Catalog] = None,
    story_so_far: str = "",
    prev_lesson_md: str = "",
    prev_title: Optional[str] = None,
    next_title: Optional[str] = None,
) -> str:
    """Assemble the full prompt that produces a single deep, connected lesson note."""
    payload = json.dumps(sel.concept.model_dump(mode="json"), indent=2)
    continuity = ""
    if story_so_far:
        continuity += (
            "STORY SO FAR — concepts the learner has ALREADY studied (build on these,\n"
            "do not re-teach them; reference them with [[wikilinks]] where useful):\n"
            + story_so_far
            + "\n\n"
        )
    if prev_title:
        continuity += (
            f"PREVIOUS lesson (recap and bridge FROM this one): {prev_title}\n"
        )
    if next_title:
        continuity += (
            f"NEXT lesson (point to it in 'Coming up next'): {next_title}\n"
        )
    if prev_lesson_md:
        snippet = prev_lesson_md.strip()
        if len(snippet) > 6000:
            snippet = snippet[:6000] + "\n…[truncated]…"
        continuity += (
            "\nFULL TEXT OF THE PREVIOUS LESSON (so your Recap connects precisely — do\n"
            "NOT repeat its content, just bridge from it):\n"
            "<<<PREVIOUS_LESSON\n" + snippet + "\nPREVIOUS_LESSON\n"
        )
    if continuity:
        continuity += "\n"
    return (
        _engine_prompt()
        + "\n\n"
        + "=== YOUR TASK FOR THIS RUN ===\n"
        + "Produce exactly ONE deep, illustrated lesson for the concept below, "
        + "following the LESSON TEMPLATE and PRESENTATION CONTRACT above. It must read "
        + "as the NEXT chapter of one continuous course: open with a Recap that bridges "
        + "from the previous lesson, climb the levels, and close by pointing to the next "
        + "concept. Mandatory: ascending Levels, several simple ```mermaid diagrams, "
        + "real numbers + a code/SQL snippet, misconceptions, the relates/differs "
        + "comparison, and self-check.\n\n"
        + LESSON_SKELETON
        + "\n"
        + _link_guide(catalog, sel.concept)
        + continuity
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


def _inject_nav(markdown: str, prev: Optional[Selection], nxt: Optional[Selection]) -> str:
    """Add a prev/next navigation line just under the breadcrumb (or H1)."""
    parts = []
    if prev is not None:
        parts.append(f"← Prev: [[{slugify(prev.concept.title)}|{prev.concept.title}]]")
    if nxt is not None:
        parts.append(f"Next: [[{slugify(nxt.concept.title)}|{nxt.concept.title}]] →")
    if not parts:
        return markdown
    nav = " · ".join(parts)
    if nav in markdown:
        return markdown
    lines = markdown.splitlines()
    # Prefer placing it right after the breadcrumb line ("*Part of …*").
    anchor = next((i for i, ln in enumerate(lines) if ln.startswith("*Part of")), None)
    if anchor is None:
        anchor = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
    if anchor is None:
        return nav + "\n\n" + markdown
    lines[anchor + 1:anchor + 1] = ["", nav]
    return "\n".join(lines)


def _one_liner(markdown: str) -> str:
    """Pull a one-sentence summary out of a generated lesson for the recap list."""
    lines = markdown.splitlines()
    in_body = False
    for i, line in enumerate(lines):
        # Start scanning after the first Level/intro heading.
        if line.startswith("## "):
            in_body = True
            continue
        if not in_body:
            continue
        text = line.strip()
        if not text or text.startswith(("#", "*", "<", "!", "|", "-", ">", "```")):
            continue
        # First real prose sentence.
        sentence = text.split(". ")[0].strip().rstrip(".")
        if len(sentence) > 160:
            sentence = sentence[:157] + "…"
        return sentence
    return ""


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
    assets_dir = vault_dir / "assets"

    # The whole course, in fixed teaching order, regardless of the filters. This is
    # the spine used to chain prerequisites and build prev/next navigation.
    course = list(iter_selections(catalog))
    pos = {id(s.concept): i for i, s in enumerate(course)}

    selections = list(iter_selections(catalog, area, topic, concept))
    if not selections:
        raise RuntimeError(
            "No concepts matched your filters (--area/--topic/--concept)."
        )

    written: list[Path] = []

    def say(msg: str) -> None:
        if console is not None:
            console.print(msg)

    if not dry_run and not mmdc_available():
        say(
            "[yellow]![/yellow] mermaid-cli not found — diagrams will stay as native "
            "```mermaid blocks (they still render in Obsidian, including mobile)."
        )

    if roadmap:
        target = vault_dir / "Home.md"
        if dry_run:
            say(f"[dim]--- ROADMAP -> {target} ---[/dim]")
            say(build_roadmap_prompt(catalog))
        else:
            _write(target, run_claude(build_roadmap_prompt(catalog), model))
            written.append(target)
            say(f"[green]✓[/green] {target}")

    # One-liner recaps of every lesson already taught this run (keyed by course index),
    # so each new lesson gets a compact "story so far".
    recaps: dict[int, str] = {}

    def prev_lesson_text(idx: int, prev_sel: Optional[Selection]) -> str:
        """Full text of the previous lesson — from this run or already on disk."""
        if prev_sel is None:
            return ""
        path = prev_sel.target(vault_dir)
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    for sel in selections:
        idx = pos[id(sel.concept)]
        prev_sel = course[idx - 1] if idx > 0 else None
        next_sel = course[idx + 1] if idx + 1 < len(course) else None
        target = sel.target(vault_dir)

        story = "\n".join(
            f"- {course[i].concept.title}: {recaps[i]}"
            for i in range(idx) if i in recaps and recaps[i]
        )
        prev_md = prev_lesson_text(idx, prev_sel)
        prompt = build_lesson_prompt(
            sel, catalog,
            story_so_far=story,
            prev_lesson_md=prev_md,
            prev_title=prev_sel.concept.title if prev_sel else None,
            next_title=next_sel.concept.title if next_sel else None,
        )

        if dry_run:
            say(f"[dim]--- {sel.concept.title} -> {target} ---[/dim]")
            say(prompt)
            continue

        say(f"Teaching [bold]{sel.concept.title}[/bold]…")
        lesson = run_claude(prompt, model)
        lesson = _inject_breadcrumb(lesson, sel.area.title, sel.topic.title)
        lesson = _inject_nav(lesson, prev_sel, next_sel)
        lesson, svgs, failed = rasterize_lesson(
            lesson, slugify(sel.concept.title), assets_dir
        )
        _write(target, lesson)
        recaps[idx] = _one_liner(lesson)
        written.extend(svgs)
        written.append(target)
        note = f" (+{len(svgs)} diagrams" + (f", {failed} unrendered" if failed else "") + ")"
        say(f"[green]✓[/green] {target}{note if svgs or failed else ''}")

    return written
