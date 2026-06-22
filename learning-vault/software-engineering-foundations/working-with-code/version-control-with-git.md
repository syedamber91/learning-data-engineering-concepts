---
title: "Version Control with Git"
area: "Software Engineering Foundations"
topic: "Working with Code"
tags: [git, version-control, commits, branches, collaboration]
---

# Version Control with Git

*Part of [[working-with-code-moc|Working with Code]] · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

## In one line
Git is a tool that saves labelled snapshots of your code over time, so you can undo mistakes, try new ideas safely, and work alongside a whole team without anyone overwriting anyone else's work.

## Picture this
Imagine you're writing a long essay and you keep hitting "Save As" every time you finish a solid draft: `essay_v1.docx`, `essay_v2.docx`, `essay_final.docx`, `essay_FINAL_REAL.docx`. Git does the same thing, but far more cleverly — it doesn't copy every file from scratch each time. It records only *what changed*, labels each version with a message you write ("added introduction"), gives it a unique ID, and lets multiple people edit *different parts simultaneously* without overwriting each other.

## How it actually works

Git stores your project inside a **repository** (repo) — an ordinary folder that Git has been told to track. Inside that folder, Git maintains a hidden `.git` directory where all the history lives.

When you're ready to save your progress, you create a **commit** — a snapshot of every tracked file at that exact moment. Each commit gets a unique 40-character **SHA hash** (a long string like `a3f8d91b...`) that acts as its permanent ID. Git also records who made the commit, when, and a short human-readable message.

Under the hood, Git is efficient: instead of storing full file copies for every commit, it stores **diffs** (the lines that changed) and compresses them. A repo with 2,000 commits doesn't weigh 2,000 times as much as one commit — it's far smaller.

**Branches** are where the real power lives. A branch is a parallel timeline for your code. You start on the default branch, usually called `main`. When you want to try something — a new feature, a bug fix, an experiment — you create a new branch. That branch starts as an exact copy of `main` at that moment. You make commits on your branch while `main` stays completely untouched. When your work is ready, you **merge** your branch back into `main`: Git compares the two timelines and combines the changes. If two people edited the *exact same line* in different ways, Git flags a **merge conflict** and asks you to decide which version wins. Everything else merges automatically.

This means 20 engineers can all work on the same codebase simultaneously, each on their own branch, without destroying each other's work.

## Worked example

Say your project has one file, `app.py`, that currently prints `"Hello"`.

```bash
# Step 1 — initialise a new repo in a folder
git init my-project
cd my-project

# Step 2 — create the file, stage it, then commit
echo 'print("Hello")' > app.py
git add app.py            # "stage" = tell Git to include this file in the next commit
git commit -m "Initial commit: print Hello"
# Git stores snapshot #1 with ID, say, a3f8d91

# Step 3 — create a branch to add a feature without touching main
git checkout -b feature/greet-world

# Step 4 — edit, stage, commit on the new branch
echo 'print("Hello, world!")' > app.py
git add app.py
git commit -m "Update greeting to include world"
# Git stores snapshot #2 with ID b7c12e4, on the feature branch only

# Step 5 — merge the feature into main
git checkout main
git merge feature/greet-world
```

After the merge, `main` now contains `print("Hello, world!")`. But snapshot `a3f8d91` — the original "Hello" version — is still in history. You can retrieve it any time with `git checkout a3f8d91`. Nothing is lost.

Now scale that up: your team has **1,000 commits** across six months. If a bug was introduced on day 143, the command `git bisect` binary-searches through the history to find the exact commit that broke things — in roughly 10 checks instead of 1,000.

## In the real world

At a company like Spotify, hundreds of engineers push code every day. Each works on a separate Git branch. When a feature is ready, the engineer opens a **pull request** (a formal proposal to merge their branch into `main`). Automated tests run against the branch automatically. Teammates review the code and leave comments. Only after approval does the code merge. If that merge breaks something in production, the team can run `git revert` on the bad commit in minutes — rolling it back without touching any other recent work. None of this team coordination would be possible without Git.

## Common misconceptions

**People think "saving a file" and "committing" mean the same thing — actually they're completely different.** Saving writes the file to your disk. Committing is a deliberate, labelled checkpoint that Git records in permanent history. You can save a file fifty times and still have zero commits. Git only knows about what you commit.

**People think deleting a branch deletes its code — actually the commits still exist.** A branch is just a *label* pointing to a commit. Deleting the label doesn't delete the underlying snapshots. They remain in the repo's history (until Git's garbage collector eventually cleans up truly unreferenced commits, which takes days or weeks by default).

**People think Git automatically shares your commits with teammates — actually you have to `git push`.** Git is *distributed*: your local repo is a complete, independent copy. Nothing you commit reaches your team until you explicitly push it to a shared remote server like GitHub or GitLab. "Committing" and "pushing" are two separate steps, and beginners conflate them constantly.

## How it relates & differs

| Concept | Relates to Git how? | Differs from Git how? |
|---|---|---|
| [[code-review-pull-requests\|Code Review & Pull Requests]] | Pull requests are built *on top of* Git branches — you open a PR to request a merge of your branch into `main` | Code review is the *human process* of inspecting code quality; Git is the *technical plumbing* that stores and moves code |
| [[automated-testing\|Automated Testing]] | Test suites are typically triggered by Git events (a push, a PR opening) via CI/CD pipelines | Tests verify whether code *works correctly*; Git tracks *what changed, when, and by whom* |
| [[clean-code-refactoring\|Clean Code & Refactoring]] | Git makes refactoring *safe* — you can rewrite code on a branch and revert instantly if you break things | Refactoring is about *improving code structure*; Git is about *recording and managing* those structural changes over time |

## Why you'd use it (and when not to)

Use Git any time more than one person touches code — and honestly even when working solo, the ability to roll back a mistake in seconds is worth the learning cost. The trade-off: Git has an unintuitive vocabulary for beginners (staging? HEAD? detached state?), and merge conflicts on large teams are painful when people work on the same files for too long without syncing. Git is also poorly suited to very large binary files — videos, machine-learning model weights, big datasets — because it was designed for text-based source code. For those cases, tools like **Git LFS** (Large File Storage) or dedicated data-versioning systems exist.

## Check yourself

**Memory hook:** Commit = camera click. Branch = parallel timeline. Merge = timelines rejoin.

**Q1: What exactly is stored inside a commit?**
A snapshot of every tracked file at that moment, plus a unique hash ID, the author's name, a timestamp, and a commit message.

**Q2: Why create a branch rather than editing `main` directly?**
A branch isolates your work-in-progress. The `main` branch (which may be live in production) stays stable while you experiment. If your branch breaks everything, you delete it and `main` is unaffected.

**Q3: You commit your changes locally, close your laptop, and go home. Can your teammates see what you did?**
No. Local commits stay on your machine until you run `git push` to send them to the shared remote repository. Committing and pushing are two separate actions.

## Connects to

[[code-review-pull-requests|Code Review & Pull Requests]] · [[automated-testing|Automated Testing]] · [[clean-code-refactoring|Clean Code & Refactoring]] · [[idempotency|Idempotency]]