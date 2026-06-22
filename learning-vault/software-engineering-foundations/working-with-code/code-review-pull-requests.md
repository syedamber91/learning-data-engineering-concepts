---
title: "Code Review & Pull Requests"
area: "Software Engineering Foundations"
topic: "Working with Code"
tags: [code-review, pull-requests, git, collaboration, software-engineering]
---

# Code Review & Pull Requests

*Part of [[working-with-code-moc|Working with Code]] · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

## In one line

A pull request is a formal way to say "here are my changes — please read them before they become part of the main codebase," giving teammates a structured chance to catch problems, ask questions, and approve.

## Picture this

Imagine you wrote a science essay and, before handing it to your teacher, you passed it to three classmates. They highlight the sentence that makes no sense, spot the fact you got backwards, and suggest a clearer way to explain the conclusion. Only after at least two of them sign off does the essay go in. That back-and-forth — the draft, the comments, the fixes, the final approval — *is* a code review via a pull request.

The "pull request" name comes from the action: you are asking the team to *pull* (import) your changes into the shared codebase.

## How it actually works

Here is the sequence, step by step.

**Step 1 — Work on a branch.**
You never edit the `main` branch directly. Instead, you create a *branch* — a private copy of the codebase — make all your changes there, and commit them. (A *commit* is a saved snapshot with a message describing what you changed.)

**Step 2 — Push and open a PR.**
You push your branch to a platform like GitHub or GitLab and click "Open Pull Request." The platform automatically computes a *diff* — a line-by-line view showing every line you added (green) or removed (red) compared to `main`. This diff is the heart of the PR; it is exactly what reviewers will read.

**Step 3 — Review happens.**
Teammates open the diff and leave *inline comments* — notes attached to specific lines of code. They might write "this function name is confusing," "this loop will break if the list is empty," or "why did we choose this approach over X?" The author reads the comments, replies, and pushes new commits to address the feedback. The diff updates automatically.

**Step 4 — Approve and merge.**
When a reviewer is satisfied, they click "Approve." Most teams require at least one (often two) approvals before anyone can merge. Once the threshold is met, the branch is merged into `main` and then usually deleted. The entire comment thread is stored permanently, so anyone can look back and understand *why* a decision was made.

**Step 5 — Automated checks run alongside.**
Most teams hook up a *CI pipeline* (Continuous Integration — an automated system that runs tests every time a PR is opened or updated). If the tests fail, the PR is blocked until they pass, adding a safety net on top of human review.

## Worked example

Suppose you are on a team building a data pipeline. A colleague named Sara opens a PR to fix a bug where dividing by zero crashed the row-count calculation.

```bash
# Sara creates a branch and makes her fix
git checkout -b fix/divide-by-zero-in-row-count
# ... edits pipeline/transform.py ...
git add pipeline/transform.py
git commit -m "fix: guard against zero row count in ratio calc"
git push origin fix/divide-by-zero-in-row-count
```

She opens a PR on GitHub. The diff shows:

```python
# BEFORE (line 47, shown in red in the diff)
- ratio = processed_rows / total_rows

# AFTER (shown in green)
+ ratio = processed_rows / total_rows if total_rows > 0 else 0.0
```

Her teammate Raj reviews and leaves an inline comment on line 47:

> "Good catch. Should `ratio` be `None` instead of `0.0` when `total_rows` is 0, so callers know data was missing rather than that the ratio was genuinely zero?"

Sara replies, agrees, updates the line to return `None`, pushes a new commit. Raj re-reads, clicks **Approve**. A second reviewer clicks **Approve**. The CI pipeline has already run 142 unit tests — all green. Sara merges. The fix is now in `main`, and six months later anyone can open the PR and read exactly why `None` was chosen over `0.0`.

## In the real world

Consider how the Python open-source library **pandas** handles contributions. Pandas has thousands of contributors worldwide who have never met. When someone fixes a bug or adds a feature, they open a PR on GitHub. Core maintainers — often volunteers on different continents — review the diff, run automated tests, request changes, and eventually merge (or decline with a reason). Without pull requests, coordinating thousands of strangers editing the same files would be chaos. The PR is the entire collaboration infrastructure: diff, discussion, approval trail, and merge gate, all in one place.

At a company like Spotify or Airbnb the same pattern runs: no engineer merges to `main` alone. A PR is required for every change, no matter how senior you are. This is not bureaucracy — it is the mechanism that keeps a codebase with 50 engineers from turning into unreadable spaghetti overnight.

## Common misconceptions

**People think the PR is just a rubber-stamp ceremony — actually it is the primary bug-catching and knowledge-sharing event.** Many bugs are caught at review that automated tests miss entirely, because a human can ask "but what happens when this is called with an empty list?" in a way a test suite does not anticipate. Studies consistently show code review catches 60–70 % of defects before release.

**People think you only review for correctness — actually readability, naming, and architecture matter just as much.** A function that works but is named `do_thing()` and has no comments will confuse every engineer who reads it for the next five years. Good reviewers flag this.

**People think approving quickly is kind — actually it is unkind.** A lazy approval wastes the entire purpose of the PR. If a reviewer clicks Approve without reading carefully, bugs slip through, the author learns nothing, and the team loses the knowledge-spreading benefit. Honest, specific feedback — even if it means the author does extra work — is the respectful choice.

## How it relates & differs

| Concept | How it RELATES | How it DIFFERS |
|---|---|---|
| [[version-control-with-git\|Version Control with Git]] | A PR is built directly on top of Git branches. The diff the reviewer reads *is* the difference between two Git commits. No Git → no PR. | Git is the technical storage and history system; a PR is the *social and process layer* on top — the conversation, the approval gate, the merge policy. Git does not care about approvals; PRs do. |
| [[automated-testing\|Automated Testing]] | CI systems run the test suite automatically when a PR opens. Tests and review are partners: tests catch regressions fast; review catches logic errors, design problems, and readability issues that tests cannot. | Automated tests run without humans and answer "does it work?" Code review requires humans and answers "is it the right approach, is it readable, is it safe?" Neither replaces the other. |
| [[clean-code-refactoring\|Clean Code & Refactoring]] | Code review is the most common place where clean code violations are caught and named. A reviewer spotting a 200-line function and saying "can we split this?" *is* the refactoring conversation happening in real time. | Clean code is a set of *principles* about how to write readable code; code review is the *process* that enforces those principles in a team setting. You can write clean code alone; code review only exists with other people. |

## Why you'd use it (and when not to)

Use a pull request workflow for any codebase more than one person touches, or any codebase *you* will return to six months from now. The discussion trail is nearly as valuable as the bug-catching: future engineers (including future you) can open a PR from two years ago and understand why a decision was made.

When it is overkill: solo personal projects where speed matters more than safety — though even there, opening a PR to yourself creates a useful record. Very tiny fixes (correcting a typo in a comment) sometimes go straight to `main` at teams that trust their CI suite, but this is an exception that teams agree on explicitly, not a default habit.

## Check yourself

**Memory hook:** PR = Essay draft with peer editing before it becomes permanent — the comments are as valuable as the final grade.

**Q1: What is the core technical artifact that makes a PR possible?**
A: A Git *branch* containing your commits. The PR is essentially a request to merge that branch into `main`, and the diff the reviewer reads is the difference between your branch and `main`.

**Q2: Name two benefits of code review beyond catching bugs.**
A: (1) It spreads knowledge — a reviewer who reads your change now understands that part of the system. (2) It keeps a permanent discussion trail, so future engineers can read *why* a decision was made, not just *what* it is.

**Q3: Your teammate opens a PR for a one-line fix. Should you approve it in 10 seconds to save time?**
A: No. Even a one-line change can introduce a subtle bug or hide a deeper problem. Read it, think about edge cases, and leave at least a brief comment confirming you understood it. A 30-second real read is worth more than a 2-second rubber-stamp.

## Connects to

[[version-control-with-git|Version Control with Git]] · [[automated-testing|Automated Testing]] · [[clean-code-refactoring|Clean Code & Refactoring]]