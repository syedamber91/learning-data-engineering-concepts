"""Stage A synthesis: mechanism-depth concept notes written FROM raw/<topic>/
posts, with provenance receipts, quarantine on gate failure, a depth gate
whose gaps are logged as source gaps, and a rebuilt topic note whose links
resolve by construction."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from .index import (atomic_dir, load_index, register_atomic, register_topic,
                    save_index)
from .llm import LLMFn
from .log import log_ingest
from .models import NoteFrontmatter
from .qc import provenance_gate, resolution_gate
from .storage import write_note

_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n(.*)\n```$", re.DOTALL)


def parse_json_any(raw: str):
    """Like learn.parse_json but tolerates a top-level list (the concept plan)."""
    s = raw.strip()
    m = _FENCE_RE.match(s)
    if m:
        s = m.group(1).strip()
    try:
        return json.loads(s)
    except json.JSONDecodeError as exc:
        raise ValueError(f"expected JSON, got: {exc}") from exc


@dataclass
class SynthesisResult:
    written: List[str] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)
    quarantined: List[str] = field(default_factory=list)
    source_gaps: Dict[str, List[str]] = field(default_factory=dict)


# ---------------------------------------------------------------- raw loading

def load_raw(root: Path, topic: str) -> Dict[str, str]:
    """filename -> text for every raw post of the topic (manifest excluded)."""
    d = root / "raw" / topic
    return {p.name: p.read_text(encoding="utf-8")
            for p in sorted(d.glob("*.md")) if not p.name.startswith("_")}


# ---------------------------------------------------------------- prompts

def build_concept_list_prompt(topic: str, raw: Dict[str, str]) -> str:
    listing = "\n".join(f"--- {name} ---\n{text}" for name, text in raw.items())
    return (
        f"CONCEPT-LIST for topic '{topic}'.\n"
        "Read the raw posts below. Return STRICT JSON: a list of objects "
        '{"slug": kebab-case concept slug, "sources": [post filenames that cover it]}. '
        "Cover every distinct mechanism-level concept; no invented concepts.\n\n"
        f"{listing}"
    )


def build_concept_prompt(slug: str, sources: Dict[str, str]) -> str:
    src = "\n".join(f"--- {name} ---\n{text}" for name, text in sources.items())
    return (
        f"CONCEPT-NOTE for '{slug}'. Write a mechanism-depth note (the HOW and "
        "WHY, with the numbers/case studies the sources give) grounded ONLY in "
        'the sources below. Return STRICT JSON {"body": markdown}. '
        "Never state a claim absent from the sources.\n\n"
        f"{src}"
    )


def build_depth_prompt(slug: str, body: str) -> str:
    return (
        f"DEPTH-CHECK for '{slug}'. From the note below ALONE, could a reader "
        "reconstruct the mechanism (how/why, not just keywords)? Return STRICT "
        'JSON {"passed": bool, "gaps": [missing mechanism, phrased as what the '
        "source doesn't spell out]}.\n\n"
        f"{body}"
    )


def build_topic_prompt(topic: str, bodies: Dict[str, str]) -> str:
    notes = "\n".join(f"--- {slug} ---\n{b}" for slug, b in bodies.items())
    return (
        f"TOPIC-NOTE for '{topic}'. From the concept notes below, return STRICT "
        'JSON {"comparisons": md, "open_questions": md bullet list, "synthesis": '
        "one-paragraph md threading the concepts with [[wikilinks]]}.\n\n"
        f"{notes}"
    )


# ---------------------------------------------------------------- pipeline

def synthesize(root: Path, topic: str, llm: LLMFn, stamp: str) -> SynthesisResult:
    raw = load_raw(root, topic)
    res = SynthesisResult()
    plan = parse_json_any(llm(build_concept_list_prompt(topic, raw)))
    if isinstance(plan, dict):
        plan = plan.get("concepts", [])

    bodies: Dict[str, str] = {}
    fms: Dict[str, NoteFrontmatter] = {}
    for item in plan:
        slug = item["slug"]
        srcs = {n: raw[n] for n in item.get("sources", []) if n in raw}
        fm = NoteFrontmatter(
            persona=root.name, kind="concept", slug=slug, topics=[topic],
            sources=[f"raw/{topic}/{n}" for n in item.get("sources", [])],
            last_updated=stamp)
        ok, reason = provenance_gate(fm)
        if not ok or not srcs:
            fm.qc, fm.qc_reason = "failed", reason or "cited source not in raw/"
            write_note(root, f"_failed/{slug}.md", fm, "(quarantined before synthesis)")
            res.quarantined.append(slug)
            continue
        try:
            out = parse_json_any(llm(build_concept_prompt(slug, srcs)))
            body = out["body"]
        except (ValueError, KeyError, TypeError):
            res.skipped.append(slug)            # retry next pass; never abort
            continue
        bodies[slug], fms[slug] = body, fm

    # depth gate over written bodies (gap-logging; fails open on bad verdicts)
    for slug, body in bodies.items():
        try:
            verdict = parse_json_any(llm(build_depth_prompt(slug, body)))
        except ValueError:
            verdict = {"passed": True, "gaps": []}
        gaps = [g for g in verdict.get("gaps", []) if g]
        if gaps:
            res.source_gaps[slug] = gaps

    # write concept notes
    index = load_index(root)
    for slug, body in bodies.items():
        write_note(root, f"{atomic_dir('concept')}/{slug}.md", fms[slug], body)
        register_atomic(index, "concept", slug, topic, stamp)
        res.written.append(slug)

    # topic note: links only to notes that now exist → resolution by construction
    parts = parse_json_any(llm(build_topic_prompt(topic, bodies)))
    related = " · ".join(f"[[{s}]]" for s in res.written)
    gap_lines = "\n".join(
        f"- **source gap** ([[{s}]]): {g}"
        for s, gaps in sorted(res.source_gaps.items()) for g in gaps)
    open_q = (parts.get("open_questions", "") + ("\n" + gap_lines if gap_lines else "")).strip()
    tbody = (
        f"Related: {related}\n\n## Comparisons\n{parts.get('comparisons', '')}\n\n"
        f"## Open questions\n{open_q}\n\n## Synthesis\n{parts.get('synthesis', '')}"
    )
    ok, dangling = resolution_gate(tbody, root)
    if not ok:                                   # belt & braces; construction should prevent
        tbody = tbody + "\n\n<!-- UNRESOLVED: " + ", ".join(dangling) + " -->"
    tfm = NoteFrontmatter(persona=root.name, kind="topic", topic=topic,
                          sources=[f"raw/{topic}"], last_updated=stamp)
    write_note(root, f"topics/{topic}.md", tfm, tbody)
    register_topic(index, topic, len(raw), stamp)
    save_index(root, index)
    log_ingest(root / "log.md", index.total(),
               f"{len(res.written)} {topic} concept(s) synthesized from raw", stamp)
    return res
