"""The LLM seam: a ``Callable[[str], str]`` so tests inject a stub, plus the
prompt builders. The default implementation shells out to the local ``claude``
CLI via de_toolkit's ``run_claude``."""

from __future__ import annotations

from typing import Callable, List, Optional

from de_toolkit.teach import run_claude

LLMFn = Callable[[str], str]


def default_llm(prompt: str) -> str:
    return run_claude(prompt)


_BUNDLE_CONTRACT = (
    "Return ONLY a JSON object with these keys: "
    '"entities" (list of {"slug","body"}), "concepts" (list of {"slug","body"}), '
    '"comparisons" (string), "open_questions" (string), "synthesis" (string). '
    "Slugs are lowercase-hyphenated. Bodies and sections are Markdown in the "
    "persona's grounded voice, citing only what the source supports. No prose "
    "outside the JSON."
)


def _registry_block(known_slugs: Optional[List[str]]) -> str:
    """The cross-linking contract: show the wiki's existing slugs so the LLM
    reuses them instead of coining near-duplicates, and links across topics."""
    if not known_slugs:
        return ""
    return (
        "\nEXISTING WIKI SLUGS — the wiki already has these entity/concept notes. "
        "If something you would write matches one, REUSE that exact slug instead of "
        "inventing a variant, and you may reference any of them as [[slug]] in your "
        "comparisons/open_questions/synthesis even without redefining them (this is "
        "what cross-links topics in the graph):\n"
        + ", ".join(sorted(known_slugs)) + "\n"
    )


def build_derive_prompt(
    persona: str,
    topic: str,
    source_text: str,
    existing_note: str = "",
    known_slugs: Optional[List[str]] = None,
) -> str:
    revise = ""
    if existing_note:
        revise = (
            "\nYou are revising an existing note (REVISE mode). Here is its current "
            "content — preserve what still holds, integrate the new source, do not "
            "drop correct prior material:\n<<<EXISTING\n" + existing_note + "\nEXISTING\n"
        )
    return (
        f"You are building research-memory derivatives for the '{persona}' persona "
        f"on the topic '{topic}'. Read the source below and produce the five "
        "derivative kinds (entities, concepts, comparisons, open questions, "
        "synthesis) grounded strictly in the persona's positions.\n\n"
        + _BUNDLE_CONTRACT
        + _registry_block(known_slugs)
        + revise
        + "\n\n<<<SOURCE\n" + source_text + "\nSOURCE\n"
    )


def build_bootstrap_prompt(
    persona: str,
    topic: str,
    section_text: str,
    known_slugs: Optional[List[str]] = None,
) -> str:
    return (
        f"Split the following authored section of the '{persona}' persona on "
        f"'{topic}' into research-memory derivatives. Do not invent anything not "
        "present in the section.\n\n"
        + _BUNDLE_CONTRACT
        + _registry_block(known_slugs)
        + "\n\n<<<SECTION\n" + section_text + "\nSECTION\n"
    )


def build_qc_prompt(note_text: str, source_text: str) -> str:
    return (
        "You are a fact-checker. Verify that every claim in the NOTE is supported "
        "by the SOURCE. Flag overreach (a conditional source claim rewritten as "
        "absolute, or any claim with no source support).\n"
        'Return ONLY JSON: {"passed": true|false, "reason": "<one sentence>"}.\n\n'
        "<<<NOTE\n" + note_text + "\nNOTE\n\n<<<SOURCE\n" + source_text + "\nSOURCE\n"
    )
