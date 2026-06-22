---
title: "Clean Code & Refactoring"
area: "Software Engineering Foundations"
topic: "Code Quality"
tags: [clean-code, refactoring, readability, technical-debt, code-quality, software-engineering]
---

# Clean Code & Refactoring

*Part of [[code-quality-moc|Code Quality]] · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

← Prev: [[automated-testing|Automated Testing]] · Next: [[arrays-hash-maps|Arrays & Hash Maps]] →

## Recap — where we just were

In the previous lesson you built a safety net: automated tests that fire on every push and turn red the moment something breaks. That safety net does more than catch bugs — it gives you the confidence to improve code you have already written, knowing the tests will immediately tell you if you accidentally change how it behaves. This lesson is about exactly that: how to improve the *shape* of working code so the next person who reads it — including future you — can understand it at a glance.

---

## Level 1 — The big idea

**Refactoring** means changing how code is *written* — its names, structure, and layout — without changing what it *does*. The program's behavior stays identical. Only the shape gets better.

**Everyday analogy:** Imagine you write instructions for making a sandwich in a hurry: "t b, s, m, l — repeat x2." Your friend can follow it once if you explain every abbreviation on the spot. Three months later, even you have forgotten what "m" stands for. Refactoring is going back and rewriting it as "Toast the bread. Spread mustard. Add lettuce. Repeat for the second sandwich." Nothing about the sandwich changed. The instructions just became something a stranger can read cold, without asking anyone.

<!-- mermaid-source:
graph TD
    BEFORE[Messy Working Code] -->|refactor| AFTER[Clean Working Code]
    AFTER --> READ[Easier to read]
    AFTER --> TEST[Easier to test]
    AFTER --> EXTEND[Easier to extend]
    BEFORE --> SAME[Same behavior throughout]
    AFTER --> SAME
-->
![[clean-code-refactoring-d1.svg]]

The crucial word is *working*. Refactoring is not rewriting from scratch, and it is never mixed with bug-fixing. It is a deliberate, separate activity with one rule: the program must produce the exact same outputs before and after.

---

## Level 2 — How it actually works

Now that you have the picture, let's look at the three levers the vault names and why each one matters at the mechanism level.

### Lever 1 — Clear names beat clever tricks

Every name in your code — every variable, every function — is a tiny message to the next reader. A name like `x` or `tmp` forces the reader to trace the whole program just to figure out what it holds. A name like `unshipped_order_ids` delivers the answer in half a second.

The test for a good name: can you guess what it holds or does *without* reading the body? If yes, the name is earning its place. If no, rename it.

### Lever 2 — Small functions are easier to test

A function that does ten things is a black box. If it produces the wrong answer, you have ten possible culprits. A function that does *one* thing can be verified by one focused test, and when it breaks, the bug is obvious. There is a useful rule of thumb called the **Single Responsibility Principle** — one function, one job. It is not enforced by the computer; it is a discipline that keeps code comprehensible.

### Lever 3 — Refactor under green tests

This is the most important operational rule: **you may only refactor when your tests are green**. Here is why. Refactoring must not change behavior. Tests are your evidence that behavior has not changed. If tests are already failing before you start, you cannot tell whether a new failure is your fault or was already there before you touched anything.

The refactoring loop in full:

<!-- mermaid-source:
graph LR
    GREEN[Tests passing] --> READ[Read the code]
    READ --> SMELL[Spot something unclear]
    SMELL --> CHANGE[Make one small change]
    CHANGE --> RUN[Run tests]
    RUN -->|Green| COMMIT[Commit and continue]
    RUN -->|Red| REVERT[Undo the change]
    COMMIT --> READ
    REVERT --> SMELL
-->
![[clean-code-refactoring-d2.svg]]

Notice: one small change, then run the tests immediately. Not ten changes in a row, then test. Tiny steps make it trivial to identify which change broke things.

---

## Level 3 — See it with real numbers

Let's take a concrete piece of messy Python code and refactor it, step by step, with tests confirming nothing breaks.

**The starting function — it works, but nobody can read it:**

```python
# BEFORE — 4 anonymous parameters, 1 cryptic letter 't'
def p(x, y, z, t):
    if t == "d":
        return (x * y) - z
    elif t == "w":
        return ((x * y) - z) / 7
    else:
        return ((x * y) - z) / 30
```

What is `x`? What is `t == "d"` supposed to mean? You have to hunt through every place in the codebase that calls `p(...)` to find out.

**Step 1 — Rename for clarity (run tests after this step alone):**

```python
# After renaming — behavior is identical
def calculate_profit(price_per_unit, units_sold, fixed_costs, period):
    if period == "daily":
        return (price_per_unit * units_sold) - fixed_costs
    elif period == "weekly":
        return ((price_per_unit * units_sold) - fixed_costs) / 7
    else:
        return ((price_per_unit * units_sold) - fixed_costs) / 30
```

Tests: green. One thing changed: a stranger can now read it without help.

**Step 2 — Extract the shared inner calculation into its own function:**

```python
# After extracting — the formula appears exactly once
def _daily_profit(price_per_unit, units_sold, fixed_costs):
    return (price_per_unit * units_sold) - fixed_costs

def calculate_profit(price_per_unit, units_sold, fixed_costs, period):
    daily = _daily_profit(price_per_unit, units_sold, fixed_costs)
    if period == "daily":
        return daily
    elif period == "weekly":
        return daily / 7
    else:
        return daily / 30
```

Tests: green again. Now if the business rule changes — say it becomes revenue minus costs multiplied by a tax rate — you fix it in exactly one place, not three.

<!-- mermaid-source:
graph TD
    BEFORE[p - calculates AND routes - 4 unnamed params] -->|extract + rename| INNER[_daily_profit - calculates only]
    BEFORE -->|extract + rename| OUTER[calculate_profit - routes only]
    OUTER --> INNER
-->
![[clean-code-refactoring-d3.svg]]

**Verify nothing changed — same inputs, same outputs:**

| price | units | costs | period | Before | After |
|-------|-------|-------|--------|--------|-------|
| 10 | 1 000 | 3 000 | daily | 7 000 | 7 000 |
| 10 | 1 000 | 3 000 | weekly | 1 000 | 1 000 |
| 10 | 1 000 | 3 000 | monthly | 233.33 | 233.33 |

Identical outputs. The refactor is correct.

---

## Level 4 — In the real world & common traps

### Real-world use case: Stripe's engineering culture

Stripe — the company that processes payments for millions of websites — has written publicly about treating code clarity as a business requirement, not just a preference. Their payment logic is audited by regulators; external lawyers and compliance officers need to read and understand it. A function named `p` with four unnamed parameters is a legal risk. A function named `calculate_profit` with named parameters is something an auditor can follow in a meeting.

The same pattern appears everywhere a codebase outlives its original authors: a startup's "working prototype" becomes the core of a product used by millions. At that point the cost of confusion is not a slow afternoon — it is failed deployments, missed security bugs, and engineers who quit because the code is demoralising to work in. Stripe's rule: every function should fit on one screen, and every name should make the next line predictable.

### Common misconceptions

**People think refactoring means rewriting from scratch — actually**, refactoring means one small, reversible change at a time, confirmed by tests after each step. A rewrite throws away everything known to work; refactoring keeps behavior intact throughout.

**People think clean code always means fewer lines — actually**, clean code sometimes means *more* lines. Three short, well-named five-line functions are cleaner than one cramped fifteen-line function, even though they are more text. Clarity is the goal, not brevity.

**People think it is fine to clean up code at the same time as fixing a bug — actually**, mixing the two is one of the most reliable ways to introduce new bugs. Fix the bug first (backed by a failing test that you make pass), reach green, commit, and *then* refactor in a separate commit. If something breaks, you will know immediately which activity caused it.

---

## Level 5 — Expert view

### How refactoring relates to its neighbours

| Concept | What it does | How it relates to refactoring |
|---------|--------------|-------------------------------|
| [[automated-testing\|Automated Testing]] | Proves behavior is correct | The safety net that makes refactoring safe — without green tests, you have no evidence that a shape change did not break anything |
| [[code-review-pull-requests\|Code Review & Pull Requests]] | Human gate before code merges | Reviewers catch bad names and oversized functions on the way in; clean code makes their job faster and approval quicker |
| [[version-control-with-git\|Version Control with Git]] | Saves a snapshot after every change | Each small refactor step is its own commit; if tests go red, `git revert` restores the last green state in one command |

### When to refactor and when not to

Refactoring is not free — it costs time, and time is a resource. The professional judgement call is whether the cost of the current confusion outweighs the cost of fixing it.

**Refactor when you are about to change the code anyway.** Adding a feature is the ideal moment — you were going to read the code regardless, so cleaning it up while you are there is nearly free.

**Do not refactor stable code you are not going to touch.** Working code that nobody needs to read is not hurting anyone. Leave it alone.

**Refactor in small commits, not marathon sessions.** A 2 000-line "cleanup" pull request is as hard to review — and as risky to approve — as a 2 000-line feature pull request.

### Edge case: refactoring when there are no tests

The vault's third key point — *refactor under green tests* — hides a trap that matters in real jobs: many production codebases have zero test coverage. In that situation, the professional move is to write **characterisation tests** first — tests that record the current behavior exactly as it is, even if that behavior is wrong — so you have a safety net before you touch anything. Only after those tests are green should you start refactoring.

---

## Check yourself

**Memory hook:** "Rename → extract → run tests → repeat — same output, better shape."

**Question 1:** What is the fundamental difference between refactoring and rewriting?
**Answer:** Refactoring makes one small, incremental change at a time while keeping behavior identical throughout, confirmed by tests after every step. Rewriting discards the existing code and builds new code from scratch.

**Question 2:** Why must your tests be green *before* you start refactoring, not just after?
**Answer:** Because tests are the only evidence that behavior has not changed. If tests are already failing when you start, you cannot tell whether a new failure is your fault or was there before you touched anything.

**Question 3:** A colleague reduces a module from 30 lines to 15 by merging four small functions into one. They say the code is now cleaner. Are they right?
**Answer:** Almost certainly not. Fewer lines is not the goal — clarity and testability are. Merging four single-purpose functions into one large function usually makes code harder to read and harder to test, which is the opposite of clean code.

---

## Connects to

[[automated-testing|Automated Testing]] · [[code-review-pull-requests|Code Review & Pull Requests]] · [[version-control-with-git|Version Control with Git]] · [[arrays-hash-maps|Arrays & Hash Maps]]

---

## Coming up next

**[[arrays-hash-maps|Arrays & Hash Maps]]** — Now that your code is readable, tested, and safe to change, the next question is how *fast* it runs. Arrays and hash maps are the two most fundamental data structures in all of programming; understanding them is the first step toward writing code that stays fast even as your data grows from a hundred rows to a hundred million.