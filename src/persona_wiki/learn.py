"""Alex the learner: an autonomous loop that learns a vutr topic (Spark) from the
vutr wiki, closed-book, and captures the learning into Alex's own growing wiki."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from .index import atomic_dir, load_index, register_atomic, save_index
from .llm import LLMFn
from .log import log_ingest
from .models import NoteFrontmatter
from .storage import parse_note, write_note

SPARK_ORDER: List[str] = [
    "spark-origin", "rdd", "lazy-evaluation", "catalyst-optimizer",
    "adaptive-query-execution", "executor-memory-model", "shuffle-writes-to-disk",
    "data-skew-oom", "sort-merge-join", "shuffle-hash-join", "data-locality",
    "jvm-object-overhead", "pyspark", "spark-structured-streaming", "photon",
    "remote-shuffle-service",
]

_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n(.*)\n```$", re.DOTALL)


# ---------------------------------------------------------------- source loading

def load_topic_concepts(vutr_root: Path, topic: str) -> Dict[str, str]:
    """Return {slug: note_body} for every vutr atomic note tagged with ``topic``."""
    out: Dict[str, str] = {}
    for kind in ("entity", "concept"):
        d = vutr_root / atomic_dir(kind)
        if not d.exists():
            continue
        for p in d.glob("*.md"):
            fm, body = parse_note(p.read_text(encoding="utf-8"))
            if topic in (fm.topics or []):
                out[p.stem] = body
    return out


def concept_order(available: Dict[str, str]) -> List[str]:
    """SPARK_ORDER restricted to available slugs, then any extra slugs appended."""
    ordered = [s for s in SPARK_ORDER if s in available]
    extra = sorted(s for s in available if s not in SPARK_ORDER)
    return ordered + extra


# ---------------------------------------------------------------- prompts + parse

def parse_json(raw: str) -> dict:
    """Parse a JSON object from LLM output, tolerating a ```json fence."""
    s = raw.strip()
    m = _FENCE_RE.match(s)
    if m:
        s = m.group(1).strip()
    try:
        data = json.loads(s)
    except json.JSONDecodeError as exc:
        raise ValueError(f"expected JSON, got: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("expected a JSON object")
    return data


def build_teach_prompt(slug: str, note_text: str) -> str:
    return (
        f"You are Vu Trinh teaching a curious 15-year-old about '{slug}'. Explain it "
        "in plain language a 15-year-old could follow, using ONLY the facts in the "
        "NOTE below — do not add outside facts. Add a simple ```mermaid diagram ONLY "
        "if it genuinely clarifies a flow or structure; otherwise omit it. Return the "
        "explanation as Markdown (no JSON).\n\n<<<NOTE\n" + note_text + "\nNOTE\n"
    )


def build_reflect_prompt(slug: str, explanation: str) -> str:
    return (
        f"You are Alex, a 15-year-old learner, hearing about '{slug}'. In your own "
        "voice ('wait, so... okay but then why...'), restate what you understood and "
        "note what still confuses you. Return ONLY JSON: "
        '{"restatement": "<your words>", "questions": ["<1-2 follow-ups>"], '
        '"mermaid": "<a simple mermaid diagram of your mental model, or empty string>"}'
        ".\n\n<<<EXPLANATION\n" + explanation + "\nEXPLANATION\n"
    )


def build_answer_prompt(slug: str, note_text: str, questions: List[str]) -> str:
    qs = "\n".join(f"- {q}" for q in questions) or "- (none)"
    return (
        f"You are Vu Trinh answering Alex's follow-ups about '{slug}', using ONLY the "
        "NOTE below. If a question cannot be answered from the NOTE, put it in gaps "
        "instead of guessing. Return ONLY JSON: "
        '{"answers": ["<grounded answer>"], "gaps": ["<question the note cannot answer>"]}'
        "\n\n<<<QUESTIONS\n" + qs + "\nQUESTIONS\n\n<<<NOTE\n" + note_text + "\nNOTE\n"
    )


def build_score_prompt(slug: str, note_text: str, restatement: str) -> str:
    return (
        f"You are Vu Trinh judging whether Alex has learned '{slug}'. Compare his "
        "RESTATEMENT against the NOTE. Level is 'mastered' if it covers the note's key "
        "points, 'familiar' if partial, 'learning' if shallow. Also list any claim in "
        "the restatement that is NOT supported by the NOTE. Return ONLY JSON: "
        '{"level": "mastered|familiar|learning", "reason": "<one sentence>", '
        '"unverified": ["<unsupported claim>"]}'
        "\n\n<<<RESTATEMENT\n" + restatement + "\nRESTATEMENT\n\n<<<NOTE\n"
        + note_text + "\nNOTE\n"
    )


# ---------------------------------------------------------------- one concept

@dataclass
class ConceptResult:
    slug: str
    explanation: str
    restatement: str
    questions: List[str] = field(default_factory=list)
    mermaid: str = ""
    answers: List[str] = field(default_factory=list)
    gaps: List[str] = field(default_factory=list)
    unverified: List[str] = field(default_factory=list)
    level: str = "learning"
    reason: str = ""


def run_concept(slug: str, note_text: str, llm: LLMFn) -> ConceptResult:
    explanation = llm(build_teach_prompt(slug, note_text))
    reflect = parse_json(llm(build_reflect_prompt(slug, explanation)))
    questions = [str(q) for q in reflect.get("questions", [])]
    answer = parse_json(llm(build_answer_prompt(slug, note_text, questions)))
    score = parse_json(llm(build_score_prompt(slug, note_text, reflect.get("restatement", ""))))
    return ConceptResult(
        slug=slug,
        explanation=explanation,
        restatement=str(reflect.get("restatement", "")),
        questions=questions,
        mermaid=str(reflect.get("mermaid", "") or ""),
        answers=[str(a) for a in answer.get("answers", [])],
        gaps=[str(g) for g in answer.get("gaps", [])],
        unverified=[str(u) for u in score.get("unverified", [])],
        level=str(score.get("level", "learning")),
        reason=str(score.get("reason", "")),
    )


# ---------------------------------------------------------------- capture: notes

def render_concept_body(r: ConceptResult) -> str:
    parts = [r.restatement.strip()]
    if r.mermaid.strip():
        parts.append("```mermaid\n" + r.mermaid.strip() + "\n```")
    parts.append(f"*Source: [[{r.slug}]] (vutr)*")
    return "\n\n".join(parts) + "\n"


def write_concept_note(learn_root: Path, topic: str, r: ConceptResult, stamp: str) -> Path:
    fm = NoteFrontmatter(
        persona="alex", kind="concept", slug=r.slug, sources=[f"vutr/{r.slug}"],
        last_updated=stamp, topics=[topic], learner="alex", source_note=r.slug,
        mastery=r.level,
    )
    return write_note(learn_root, f"{atomic_dir('concept')}/{r.slug}.md", fm, render_concept_body(r))


def write_qa_note(learn_root: Path, order_idx: int, r: ConceptResult, stamp: str) -> Path:
    qa_lines = ["## Follow-up questions"]
    for i, q in enumerate(r.questions):
        a = r.answers[i] if i < len(r.answers) else "(the wiki does not cover this — see open questions)"
        qa_lines.append(f"\n**Alex:** {q}\n\n**vutr:** {a}")
    body = (
        f"*What Alex understood:* {r.restatement.strip()}\n\n"
        + "\n".join(qa_lines) + "\n"
    )
    fm = NoteFrontmatter(
        persona="alex", kind="concept", slug=f"{order_idx:03d}-{r.slug}",
        sources=[f"vutr/{r.slug}"], last_updated=stamp, topics=["spark"],
        learner="alex", source_note=r.slug, mastery=r.level,
    )
    return write_note(learn_root, f"qa/{order_idx:03d}-{r.slug}.md", fm, body)


# ---------------------------------------------------------------- capture: docs

def _safe_write(root: Path, rel: str, text: str) -> Path:
    root = root.resolve()
    target = (root / rel).resolve()
    if root != target and root not in target.parents:
        raise ValueError(f"refusing to write outside learn root: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return target


def append_open_questions(learn_root: Path, r: ConceptResult, stamp: str) -> None:
    if not r.gaps and not r.unverified:
        return
    path = learn_root / "open-questions.md"
    text = path.read_text(encoding="utf-8") if path.exists() else \
        "# Alex's open questions\n\nThings the wiki didn't answer, and claims to double-check.\n"
    lines = [f"\n## {r.slug} ({stamp})"]
    for g in r.gaps:
        lines.append(f"- wiki gap: {g}")
    for u in r.unverified:
        lines.append(f"- unverified (not in vutr wiki): {u}")
    _safe_write(learn_root, "open-questions.md", text.rstrip() + "\n" + "\n".join(lines) + "\n")


def write_mastery(learn_root: Path, order: List[str], levels: Dict[str, str], stamp: str) -> Path:
    n = len(order)
    mastered = sum(1 for s in order if levels.get(s) == "mastered")
    pct = round(100 * mastered / n) if n else 0
    rows = "\n".join(f"| {s} | {levels.get(s, 'not started')} |" for s in order)
    text = (
        "# Alex's Spark mastery\n\n"
        f"**Overall: {pct}% ({mastered} mastered / {n})** — updated {stamp}\n\n"
        "| concept | level |\n|---|---|\n" + rows + "\n"
    )
    return _safe_write(learn_root, "mastery.md", text)


# ---------------------------------------------------------------- capture: transcript

_TRANSCRIPT_HEADER = (
    "# Alex learns Apache Spark — transcript\n\n"
    "*Full dialogue of the learning run, in order. See [[mastery]].*\n"
)


def _transcript_section(order_idx: int, r: ConceptResult) -> str:
    followups = " ".join(r.questions) if r.questions else "(no follow-ups)"
    answers = " ".join(r.answers) if r.answers else "(the wiki did not cover the follow-ups)"
    diagram = "yes" if r.mermaid.strip() else "no"
    return (
        f"## {order_idx}. {r.slug}  ({r.level})\n\n"
        f"**vutr teaches:** {r.explanation.strip()}\n\n"
        f"**Alex:** {r.restatement.strip()}  {followups}\n\n"
        f"**vutr answers:** {answers}\n\n"
        f"**Verdict:** {r.level} — {r.reason.strip()}  ·  Diagram added: {diagram}\n"
    )


def upsert_transcript(learn_root: Path, order_idx: int, r: ConceptResult) -> Path:
    path = learn_root / "transcript.md"
    text = path.read_text(encoding="utf-8") if path.exists() else _TRANSCRIPT_HEADER
    section = _transcript_section(order_idx, r)
    pat = re.compile(rf"(?ms)^## {order_idx}\. {re.escape(r.slug)}\b.*?(?=^## |\Z)")
    if pat.search(text):
        text = pat.sub(section.rstrip() + "\n\n", text)
    else:
        text = text.rstrip() + "\n\n" + section
    return _safe_write(learn_root, "transcript.md", text.rstrip() + "\n")


# ---------------------------------------------------------------- the loop

def _prior_levels(learn_root: Path) -> Dict[str, str]:
    """Levels recovered from existing concept-note frontmatter (idempotent re-run)."""
    levels: Dict[str, str] = {}
    d = learn_root / atomic_dir("concept")
    if not d.exists():
        return levels
    for p in d.glob("*.md"):
        fm, _ = parse_note(p.read_text(encoding="utf-8"))
        if fm.mastery:
            levels[p.stem] = fm.mastery
    return levels


def learn(learn_root: Path, vutr_root: Path, topic: str, llm: LLMFn, stamp: str,
          max_retries: int = 2) -> dict:
    learn_root.mkdir(parents=True, exist_ok=True)
    concepts = load_topic_concepts(vutr_root, topic)
    order = concept_order(concepts)
    idx_of = {slug: i + 1 for i, slug in enumerate(order)}
    levels = _prior_levels(learn_root)
    index = load_index(learn_root)
    failed = 0

    for _pass in range(max_retries + 1):
        for slug in order:
            if levels.get(slug) == "mastered":
                continue
            try:
                r = run_concept(slug, concepts[slug], llm)
            except ValueError:
                failed += 1
                continue
            levels[slug] = r.level
            write_concept_note(learn_root, topic, r, stamp)
            write_qa_note(learn_root, idx_of[slug], r, stamp)
            append_open_questions(learn_root, r, stamp)
            upsert_transcript(learn_root, idx_of[slug], r)
            register_atomic(index, "concept", slug, topic, stamp)
        if all(levels.get(s) == "mastered" for s in order):
            break

    save_index(learn_root, index)
    write_mastery(learn_root, order, levels, stamp)
    total = len(order)
    mastered = sum(1 for s in order if levels.get(s) == "mastered")
    pct = round(100 * mastered / total) if total else 0
    log_ingest(learn_root / "log.md", index.total(),
               f"{mastered}/{total} Spark concepts mastered", stamp)
    return {"total": total, "mastered": mastered, "pct": pct, "failed": failed}
