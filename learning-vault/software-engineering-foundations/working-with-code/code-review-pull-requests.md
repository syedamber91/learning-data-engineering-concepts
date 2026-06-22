---
title: "Code Review & Pull Requests"
area: "Software Engineering Foundations"
topic: "Working with Code"
tags: [code-review, pull-requests, collaboration, git, teamwork, quality]
---

# Code Review & Pull Requests

*Part of [[working-with-code-moc|Working with Code]] · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

← Prev: [[version-control-with-git|Version Control with Git]] · Next: [[automated-testing|Automated Testing]] →

## Recap — where we just were

In the previous lesson you learned that Git lets you save snapshots of your work as commits and run parallel experiments using branches — without ever touching the shared `main` branch. Now the natural question is: *how does your work on a branch safely travel into `main` for everyone to use?* The answer is the pull request, and that gate is what this lesson is about.

## Level 1 — The big idea

A **pull request** (PR) is a formal proposal to merge one branch into another.

**Everyday analogy:** Imagine you rewrote a chapter of a shared textbook. Before the new chapter goes to print, you hand it to an editor. The editor reads every sentence, leaves sticky notes in the margins, and eventually stamps it "approved." Only then does the chapter replace the old one. A pull request is that editorial process for code — your branch is the draft chapter, `main` is the printed book.

A **code review** is the act of a teammate reading your proposed changes and deciding whether they are safe, clear, and correct. It is the most universal quality-control step in professional software development.

<!-- mermaid-source:
graph LR
    DEV[Your feature branch] -->|open a PR| GATE[Code Review Gate]
    GATE -->|approved| MAIN[main branch]
    GATE -->|changes requested| DEV
-->
![[code-review-pull-requests-d1.svg]]

Your branch does not touch `main` until a teammate explicitly says "this looks good." That single rule prevents an enormous number of bugs from ever reaching users.

## Level 2 — How it actually works

Now that you have the picture, let's walk through every step of the lifecycle so you could do this yourself tomorrow.

### Step 1 — Push your branch to a remote

Your commits live only on your machine. To let teammates see them you **push** the branch to a shared server — typically GitHub, GitLab, or Bitbucket. These services all run Git under the hood; they add a web interface on top so reviews can happen in a browser.

### Step 2 — Open a pull request

On GitHub you click "New pull request" and choose: *from* your feature branch, *into* `main`. GitHub then displays a **diff** — a coloured view of every line that changed. Green lines are additions; red lines are deletions. This diff is what your reviewer actually reads.

### Step 3 — Reviewers leave comments

Teammates read the diff line by line. They can post an **inline comment** on a specific line ("this variable name is misleading"), ask a **question** ("what happens if the list is empty?"), or even suggest a direct one-line fix inside the UI itself. The author receives a notification for each comment.

### Step 4 — Author responds and updates

You push new commits to the same branch. The PR updates automatically — you never close and reopen it. The conversation keeps going until both sides are satisfied.

### Step 5 — Approval and merge

Once reviewers click "Approve", you or a team lead clicks "Merge pull request." GitHub creates a merge commit on `main` (exactly like `git merge` does locally) and the branch's history is permanently woven in.

<!-- mermaid-source:
sequenceDiagram
    participant DEV as You
    participant GH as GitHub
    participant REV as Reviewer
    DEV->>GH: git push feature/search
    DEV->>GH: Open PR - feature/search into main
    GH->>REV: Notify reviewer
    REV->>GH: Inline comment on line 42
    GH->>DEV: Notify you
    DEV->>GH: Push fix commit
    REV->>GH: Approve PR
    DEV->>GH: Click Merge
    GH->>GH: Merge commit lands on main
-->
![[code-review-pull-requests-d2.svg]]

### Why teams bother — three jobs a PR does at once

1. **Catches bugs before release.** A second pair of eyes spots the edge case you were too close to see after hours of writing.
2. **Spreads knowledge.** Every reviewer learns what changed and why. Nobody ends up as the one person who understands a critical feature.
3. **Keeps a discussion trail.** Six months later someone asks "why did we do it this way?" The PR comments are the answer, forever searchable.

## Level 3 — See it with real numbers

Imagine your team's to-do app has **12,000 lines of code** across **47 files**. You spent 3 days adding a search feature. Your branch, `feature/search`, has **4 commits** touching **6 files**: **+218 lines added, −44 lines removed**.

Here is the complete command sequence on your machine:

```bash
# You're on your feature branch, all commits done
git checkout feature/search

# Push to GitHub; -u links the branch for future pushes
git push -u origin feature/search
# Output: Branch 'feature/search' set up to track 'origin/feature/search'.

# GitHub shows a banner: "Compare & pull request" — click it.
# Title:       "Add full-text search to task list"
# Description: "Closes #88. Adds a search bar above the task list.
#               Filters tasks client-side on keydown.
#               Tested on Chrome, Firefox, and Safari."
```

Your reviewer sees this in the diff:

```diff
# File: src/components/TaskList.jsx   (+47 lines, -12 lines)

- export function TaskList({ tasks }) {
+ export function TaskList({ tasks, query }) {
+   const visible = tasks.filter(t =>
+     t.title.toLowerCase().includes(query.toLowerCase())
+   );
    return (
-     <ul>{tasks.map(t => <Task key={t.id} item={t} />)}</ul>
+     <ul>{visible.map(t => <Task key={t.id} item={t} />)}</ul>
    );
  }
```

Reviewer leaves a comment on the filter line: *"What happens when `query` is `undefined`? This will throw a TypeError."*

You push one more commit:

```bash
git commit -am "Guard against undefined query prop"
git push
# PR automatically shows the new commit — no need to reopen
```

Reviewer approves. You merge. Total time: **2 hours**, **3 comment threads**, **1 bug caught before it ever hit a user.** The whole history — original code, bug catch, fix — is permanently attached to the PR.

<!-- mermaid-source:
graph TD
    C1[commit 1 - add search bar] --> C2[commit 2 - wire filter logic]
    C2 --> C3[commit 3 - add tests]
    C3 --> C4[commit 4 - guard undefined query]
    C4 --> MERGE[merge commit on main]
    REVIEW[Reviewer comment on line 42] -.->|triggered| C4
-->
![[code-review-pull-requests-d3.svg]]

## Level 4 — In the real world & common traps

### Named real-world use case: Google's mandatory review culture

Google requires **every** change to its codebase — even a one-line typo fix — to be reviewed and approved by at least one other engineer before it merges. This is enforced by tooling (their internal system is called Critique; the open-source world uses GitHub PRs for the same purpose). The result: a codebase of roughly **2 billion lines of code** stays stable even though tens of thousands of engineers make changes every single day. The PR gate is the primary reason a codebase can scale to that size without collapsing into chaos. Meta, Stripe, Shopify, and virtually every professional software team follow the same practice. In most companies, pushing directly to `main` without a PR is blocked at the server level — it is simply not allowed.

### Common misconceptions

**People think: PRs are only about finding bugs.**
Actually: Bug-catching is one of three jobs. PRs also transfer knowledge across the team and document the *reasoning* behind decisions. A codebase with a rich PR history is dramatically easier to maintain because you can trace every line back to the conversation that produced it.

**People think: A code review means the reviewer rewrites your code.**
Actually: The reviewer's job is to read, question, and approve or decline — not to code for you. You remain responsible for the solution. When reviewers start posting large alternative implementations in comments, they have overstepped; they should open their own follow-up PR instead. The author decides how to address feedback.

**People think: If all automated tests pass, the PR can be merged without human review.**
Actually: Automated tests (the next lesson's subject) verify that the code *runs correctly*. They cannot check that the code is *readable*, *maintainable*, or *architecturally sound*. A PR that passes every test can still introduce confusing variable names, duplicated logic, or a security hole that only a human reader would notice. Human review and automated tests are complementary — neither replaces the other.

## Level 5 — Expert view

### How PRs relate to and differ from neighbouring concepts

| Concept | What it is | When it happens | Who does it |
|---|---|---|---|
| Git branch | A parallel timeline for your code | Before any work starts | Just you, locally |
| Pull request | A formal merge proposal | After your local work is done | You open; teammates review |
| Code review | The act of reading and commenting | During the PR lifecycle | Teammates |
| [[automated-testing\|Automated Testing]] | Scripts that check your code runs correctly | Automatically on every push | CI system (machines) |
| [[clean-code-refactoring\|Clean Code & Refactoring]] | Rules for readable, maintainable code | Ongoing; flagged during review | You; reviewers surface violations |

The crucial insight: a PR is the *ceremony* that coordinates all of these at once. It is the moment where automated tests run, human review happens, and clean-code feedback is given — all attached to the same record.

### Trade-offs: when PRs work and when they break down

**PRs work well when:**
- Changes are small to medium (under 400 lines). Reviewers can actually read them.
- The team gives specific, kind, actionable feedback — not vague "this is bad" comments.
- The PR description explains *why* the change was made, not just *what* it does.

**PRs break down when:**
- The PR is enormous — thousands of lines across dozens of files. Reviewers rubber-stamp it without reading, a failure mode called **review fatigue**. The fix is to break large features into a sequence of smaller, focused PRs.
- Reviews feel like personal criticism rather than technical discussion. Culture matters as much as tooling.
- Reviews are slow. A PR open for more than 2 business days tends to go stale as `main` moves on. Many teams set a formal **SLA** (service-level agreement) — "all PRs reviewed within 24 hours" — to prevent this.

### Edge case: draft PRs

GitHub and GitLab support **draft PRs** — a PR you open *before* the work is done, to share early progress and get architectural feedback. Draft PRs cannot be merged until you mark them "Ready for review." This is especially valuable for large features where you want a sanity-check before writing 1,000 lines in the wrong direction.

### Scale nuance: branch protection rules

In production repositories, **branch protection rules** are set at the server level (GitHub: Settings → Branches). They can enforce:

- A minimum of 1 or 2 approvals before merging is allowed
- All automated tests must pass
- Direct pushes to `main` are completely blocked — a PR is mandatory for everyone, including repository owners

<!-- mermaid-source:
graph TD
    PUSH[Push to GitHub] --> CI[Automated tests run]
    CI -->|tests pass| APPROVAL[At least 1 approval required]
    CI -->|tests fail| BLOCK[Merge blocked - fix the tests]
    APPROVAL -->|approved| MERGE[Merge allowed]
    APPROVAL -->|changes requested| AUTHOR[Author pushes fix commit]
    AUTHOR --> CI
-->
![[code-review-pull-requests-d4.svg]]

These rules are enforced by the server. They are the last line of defence when human judgment fails — a deliberate friction that has saved production systems innumerable times.

## Check yourself

**Memory hook:** A PR is a *gate, not a rubber stamp* — it only opens when human eyes and automated checks both say "yes."

**Q1: What are the three things a pull request does for a team beyond just catching bugs?**
A1: It catches bugs before they reach `main`, spreads knowledge so multiple engineers understand a change, and keeps a permanent searchable discussion trail that explains *why* decisions were made.

**Q2: Why is a 3,000-line pull request dangerous — even if every line of code is correct?**
A2: Reviewers cannot meaningfully read 3,000 lines. They will either approve without checking (rubber-stamping) or spend so long reviewing that the branch drifts apart from `main` and goes stale. Large PRs should be split into a sequence of smaller, focused ones.

**Q3: A teammate says "all our tests pass, so we don't need code review." What is wrong with this?**
A3: Automated tests verify that code *runs correctly*, not that it is *readable or maintainable*. A passing test suite can still hide confusing variable names, duplicated logic, or security vulnerabilities that only a human reader would spot. Review and testing are complementary, not interchangeable.

## Connects to

[[version-control-with-git|Version Control with Git]] · [[automated-testing|Automated Testing]] · [[clean-code-refactoring|Clean Code & Refactoring]]

## Coming up next

[[automated-testing|Automated Testing]] — now that your code is safely merged into `main` via a reviewed PR, the next question is: how do you *prove* it still works correctly after every future change? Automated testing answers that with scripts that check your code's behaviour in seconds, every single time someone pushes a commit.