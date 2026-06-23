# Vault improvement recommendations (deferred)

> Captured 2026-06-23 from an anti-sycophancy review of `learning-vault/` (the 16
> regenerated leveled lessons). Stored for later action — nothing here is done yet.
> Scope: only what is already in the vault, judged from PhD rigour down to a
> 15-year-old's comprehension, across learning / understanding / memorisation /
> experience-building.

## Verdict
The pedagogy scaffolding is strong (recap → levels → coming-up-next chaining works;
worked examples mostly use real numbers). But there are three objectively-wrong
shipped defects, and one systemic gap: the lessons build *understanding*, not
*experience*. It reads like a good blog post, not yet a course you build skill from.

## A. Hard defects (factually wrong / broken — fix first)
1. **Arithmetic error in the flagship correctness example.**
   `databases/relational-databases/transactions-acid.md` states the system total is
   **$1,300** twice (≈ lines 145 and 168) when Alice $800 + Bob $700 = **$1,500**
   (the same line even prints 1500 correctly). The lesson on consistency is
   internally inconsistent.
2. **Agent commentary leaked into a published note.**
   `data-modeling/warehouse-modeling/star-schema.md` line 1 is "The user needs to
   approve the write. Here is the complete lesson…" and lines ~263–271 are a trailing
   "The lesson is ~1,700 words and hits every mandatory requirement…" block. Because
   the file no longer starts with `---`, its **YAML frontmatter does not parse in
   Obsidian**. Root cause: `teach.py:run_claude` only strips a wrapping ``` fence
   (`_strip_code_fence`), not prose the model adds around the markdown. 1/16 files hit,
   but the failure is silent and will recur.
3. **Diagrams degrade the notation the prose teaches.**
   The Big-O ladder SVG renders `O1`, `On2`, `O2n` instead of O(1), O(n²), O(2ⁿ)
   (verified in `learning-vault/assets/big-o-time-complexity-d3.svg`). Cause: the
   prompt rule "no parentheses in mermaid node labels." The picture teaches sloppier
   notation than the text.

## B. Systemic gap — experience building
Only **1 of 16** lessons has any hands-on task. Every "Check yourself" is recall Q&A
(tests reading, not doing). Missing: runnable datasets/sandbox, "build it / break it /
fix it" labs (e.g. actually trigger lock contention; actually time O(n²) vs O(n)),
and a project that accumulates across the course. Highest-leverage change for the
stated goal.

## C. Gaps by lens
- **Understanding / PhD rigour:** `version-control-with-git.md` says Git "stores only
  what changed (called a diff)" — Git stores **snapshots/blobs**, not diffs. Worked
  examples are sometimes toy-sized (Star Schema's "500M-row warehouse" shown on 4
  rows). Confident absolutes need caveats ("most databases default to Read Committed"
  is false for MySQL/InnoDB = Repeatable Read).
- **Memorisation:** mnemonics are inconsistent; no spaced-repetition / flashcard
  convention and no per-topic one-page cheat-sheet, so facts are read once and never
  re-encountered. Mangled diagrams (A3) also hurt recall.
- **Comprehension / 15-year-old:** lessons are long (~1,500–2,000 words) with no
  30-second TL;DR, difficulty marker, or estimated reading time at the top; some walls
  of prose between diagrams.
- **Connectedness (strongest area):** recaps are excellent — keep them. Two cracks:
  forward-references to concepts not yet taught (e.g. Big-O Level 2 links
  `[[indexing]]`, which comes later), and "Connects to" lists are long and don't
  separate *prerequisite* from *related*.
- **Cosmetic but pervasive:** heading capitalisation drifts file-to-file ("The Big
  Idea" vs "The big idea"; "Check Yourself" vs "Check yourself").

## D. Recommended actions, in priority order
1. **Fix the 3 hard defects (A1–A3).** Correct the $1,500 total; make `run_claude`
   slice from the first `---` to the last real section (strip pre/post agent prose)
   and re-emit star-schema; allow quoted `O(1)`/`O(n²)` in mermaid labels and
   re-render the diagrams.
2. **Add an experience layer:** a `## Try it yourself` block per lesson with 1–2
   runnable tasks + expected result, backed by a small committed dataset/SQL file.
3. **Add a memorisation layer:** a standard flashcard block or per-topic cheat-sheet
   note so facts are re-encountered.
4. **Add a header band:** 30-second TL;DR + difficulty + estimated reading time.
5. **Split "Connects to"** into *Prerequisites* vs *Related*; mark forward-references
   as "(coming later)".
6. **Normalise heading case** and pin it in the lesson skeleton.

## Where the fixes live (for whoever picks this up)
- Prompt/structure: `prompts/vault-teaching-engine.md`
- Generation + sanitising + diagram rasterise: `src/de_toolkit/teach.py`,
  `src/de_toolkit/diagrams.py`
- Output: `learning-vault/**/*.md`, `learning-vault/assets/*.svg`
- Tests: `tests/test_teach.py`
