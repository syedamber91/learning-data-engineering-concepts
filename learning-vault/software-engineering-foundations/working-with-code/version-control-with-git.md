---
title: "Version Control with Git"
area: "Software Engineering Foundations"
topic: "Working with Code"
tags: [git, version-control, commits, branching, collaboration]
---

# Version Control with Git

*Part of [[working-with-code-moc|Working with Code]] · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

Next: [[code-review-pull-requests|Code Review & Pull Requests]] →

## Recap — Where We Just Were

This is the opening lesson of *Software Engineering Foundations: Working with Code* — the track that turns you from someone who writes code into someone who engineers it. Before a single feature ships, professionals need a system to track changes, collaborate without chaos, and recover from mistakes. That system is Git, and every other concept in this course builds on top of it.

## Level 1 — The Big Idea

**Git is a time machine for your code.**

Every time you say "save a snapshot", Git photographs your entire project and stores it permanently. You can jump back to any snapshot, run parallel "what-if?" experiments without touching the main code, and safely combine everyone's work — even when ten engineers are editing the same files simultaneously.

**Everyday analogy:** Think of writing an essay in Google Docs. Google keeps a version history: you can click "See version history" and restore last Tuesday's draft in two seconds. Git does the exact same thing for code — except *you* choose when to take each snapshot and you label it with a message like `"Fixed the login bug"`.

**Why this matters:** Without Git, teams resort to emailing folders named `project_final_v3_REAL_FINAL.zip`. Someone overwrites someone else's work. A bug appears and nobody knows when it was introduced. Git makes all of that disappear.

<!-- mermaid-source:
graph LR
    S1[Snapshot 1 - project starts] --> S2[Snapshot 2 - login added]
    S2 --> S3[Snapshot 3 - bug fixed]
    S3 --> S4[Snapshot 4 - search added]
    style S4 fill:#90EE90
-->
![[version-control-with-git-d1.svg]]

Each box is a saved checkpoint. You can always travel back to any of them.

## Level 2 — How It Actually Works

Now that you have the intuition, here is the real mechanism — three ideas that together make Git tick.

### Idea 1 — Commits: deliberate snapshots

A **commit** is a snapshot you intentionally save, plus a short message explaining what changed. Git does not store the entire project file-by-file every time; it stores only what changed (called a **diff** — short for "difference") and a pointer back to the previous commit. This makes Git fast even on enormous projects.

Every commit also records: *who* saved it (your name and email), *when* (a timestamp), and a unique ID called a **hash** — a 40-character fingerprint like `a3f8c1d2...` that identifies this exact snapshot forever.

### Idea 2 — Branches: parallel timelines

A **branch** is a named pointer to one commit. The default branch is usually called `main`. When you create a new branch — say `feature/dark-mode` — Git creates a second pointer that starts at the same commit you are on. From that moment, new commits on `feature/dark-mode` do not touch `main` at all. The two timelines grow independently.

Think of it like writing two versions of a story simultaneously. You keep your original Chapter 3 in one notebook. You draft an alternative Chapter 3 in a second notebook. If the new draft is better, you staple it in. If not, you throw the notebook away and the original is completely untouched.

### Idea 3 — Merging: reuniting timelines

**Merging** takes two branches and combines their changes into one. Git finds the commit where the two branches last shared history (the **common ancestor**), sees what each branch added since then, and stitches the changes together. If the same line of code was edited differently on both branches, Git pauses and asks you to decide which version wins. This pause is called a **merge conflict**.

<!-- mermaid-source:
graph LR
    A[commit A - shared start] --> B[commit B - on main]
    A --> C[commit C - on feature]
    C --> D[commit D - on feature]
    B --> M[merge commit - combines both]
    D --> M
    style M fill:#FFD700
-->
![[version-control-with-git-d2.svg]]

The gold box is the merge commit. It has two parents — one from each branch — so the full history of both lines of work is preserved.

### The hidden engine: `.git`

When you run `git init` inside a folder, Git creates a hidden subfolder called `.git`. Every snapshot, every branch pointer, every commit message lives inside it. Your project folder looks completely normal. Deleting `.git` erases the entire history — so treat it as sacred.

<!-- mermaid-source:
graph TD
    P[Your project folder] --> Code[src and files you edit]
    P --> GIT[.git - hidden folder]
    GIT --> OBJ[objects - the snapshots]
    GIT --> REF[refs - branch pointers]
    GIT --> LOG[logs - commit history]
-->
![[version-control-with-git-d3.svg]]

## Level 3 — See It With Real Numbers

Let's build a tiny project with real Git commands. You are the sole developer on a to-do app. The full story: **1 repo, 2 commits on `main`, then 1 feature branch with 1 commit, then a merge**.

```bash
# 1. Create a folder and enter it
mkdir todo-app && cd todo-app

# 2. Tell Git to start tracking this folder
git init
# Git creates .git/ — 0 commits yet

# 3. Create your first file and stage it
echo "Buy milk" > tasks.txt
git add tasks.txt          # "stage" = include this file in the next snapshot

# 4. Save the first snapshot
git commit -m "First commit: add tasks file"
# Git assigns hash: 3a1bc7f  (first 7 characters shown)

# 5. Add a second task and commit again
echo "Walk the dog" >> tasks.txt
git commit -am "Add second task"
# Hash: 9d4ef22   — main points here now

# 6. Create a feature branch for a dark-mode experiment
git checkout -b feature/dark-mode
# A new pointer is created; it also points at 9d4ef22 for now

# 7. Make a change ON the feature branch only
echo "dark_mode = true" > settings.txt
git add settings.txt
git commit -m "Add dark mode setting"
# Hash: c0b3e11  — only on feature/dark-mode; main is still at 9d4ef22

# 8. Switch back to main and merge the feature in
git checkout main
git merge feature/dark-mode
# Git creates a merge commit — hash: b7f2a19
# main now contains BOTH tasks.txt AND settings.txt
```

**Running `git log --oneline` on `main` after the merge:**

```
b7f2a19  Merge branch feature/dark-mode into main
c0b3e11  Add dark mode setting
9d4ef22  Add second task
3a1bc7f  First commit: add tasks file
```

Four commits. Four hashes. The entire history of the project, readable in seconds.

## Level 4 — In the Real World & Common Traps

### Real-world use case: the Linux kernel

The Linux operating system — which runs most of the world's servers, every Android phone, and the world's top 500 supercomputers — is maintained by roughly **28,000 contributors** across hundreds of companies including Google, Intel, and Red Hat. Every single change goes through Git. On a busy week, thousands of commits land from engineers who have never met in person. Without Git's branching model, coordinating this would be physically impossible. Linus Torvalds (Linux's creator) actually *wrote* Git in 2005 because no existing tool could scale to a project that large.

At any tech company you could work at — Spotify, Uber, a three-person startup — the workflow mirrors this: every engineer opens their own branch, pushes it to a shared server, and asks teammates to review it via a **pull request** before it touches `main`. Nothing ships without passing through Git.

### Common misconceptions

**People think: "Git and GitHub are the same thing."**
Actually: Git is a tool you install on your own computer. GitHub is a website owned by Microsoft that hosts *copies* of Git repositories in the cloud. You can use Git with zero internet connection, or host your code on GitLab, Bitbucket, or your own server. GitHub is just the most popular storage destination for Git repos — not Git itself.

**People think: "A branch is a full copy of the project — it must eat disk space."**
Actually: A branch is a tiny text file containing one 40-character hash that points at a commit. Creating a thousand branches costs almost no disk space. The snapshots (objects) are shared between branches; Git stores each unique file version only once across the whole history.

**People think: "`git commit` saves my work to the internet."**
Actually: `git commit` saves a snapshot *locally* inside your `.git` folder. Nothing leaves your machine until you explicitly run `git push`. You can commit freely offline on a plane and push later when you have Wi-Fi.

## Level 5 — Expert View

### How Git relates to — and differs from — neighbouring concepts

Git is the foundation layer that [[automated-testing|Automated Testing]] and [[code-review-pull-requests|Code Review & Pull Requests]] both sit on top of. Here is how they differ in purpose:

| | **Git** | **Automated Testing** | **Code Review & Pull Requests** |
|---|---|---|---|
| **What it tracks** | Who changed what, and when | Whether the code works correctly | Whether the code is well-written |
| **When it runs** | Every time you commit or push | On every commit or in CI | When a branch is proposed for merge |
| **Output** | A commit graph and history | Pass / fail report | Approved or rejected change |
| **The relationship** | The infrastructure everything else sits on | Tests run against Git commits | Reviews happen on Git branches |

You cannot run automated tests on code you have not tracked. Code review only makes sense once code lives in a branch. Git is not one tool among many equals — it is the stage on which everything else performs.

### Trade-offs and edge cases

**Where Git shines:** text-based source code, configuration files, Markdown documents — anything where line-by-line diffs are meaningful.

**Where Git struggles:** large binary files such as video, audio, or Photoshop `.psd` files. Git stores every version of every binary, so a 500 MB video committed ten times becomes a 5 GB repository. Teams use an extension called **Git LFS** (Large File Storage) to handle binaries separately.

**Rebase vs. Merge:** Instead of creating a merge commit with two parents, `git rebase` replays your branch's commits on top of the latest `main` as if you had branched off today. The result is a clean, straight-line history with no merge commits — easier to read. The trade-off: rebasing rewrites commit hashes, which confuses teammates who already pulled that branch. Rule of thumb: merge for shared branches, rebase for private ones.

**The staging area (index):** Between your files and a commit sits an invisible tray called the **staging area**. `git add` places changes onto the tray; `git commit` photographs only what is on the tray. This lets you craft a precise commit — for example, committing only the bug fix from a file where you also made unrelated style edits. Many beginners skip learning this and later discover half their changes are missing from a commit.

## Check Yourself

**Memory hook:** **Commit → Branch → Merge** = **Save → Experiment → Reunite**

---

**Q1. What is stored inside a Git commit?**
A snapshot of every tracked file (or a diff from the parent commit), a commit message, the author's name and email, a timestamp, and a unique hash. Each commit also stores a pointer to its parent, chaining the entire history together.

**Q2. You create a branch called `feature/search`, make three commits on it, then delete the branch without merging. What happens to those commits?**
They become unreachable — Git can no longer find them by following branch pointers — and will eventually be garbage-collected (quietly deleted by Git's housekeeping process). The work is lost. Always merge or keep the branch alive if you want the commits to survive.

**Q3. Your teammate changed line 42 of `app.py` on their branch. You also changed line 42 of `app.py` on your branch. What happens when you merge?**
Git detects a **merge conflict**: it cannot automatically decide which version of line 42 to keep. It marks the file with conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) and pauses. You open the file, choose the correct version (or write a combination), run `git add` on the resolved file, and then `git commit` to finish the merge.

## Connects to

[[code-review-pull-requests|Code Review & Pull Requests]] · [[automated-testing|Automated Testing]] · [[clean-code-refactoring|Clean Code & Refactoring]]

## Coming Up Next

[[code-review-pull-requests|Code Review & Pull Requests]] — Now that your code lives safely in branches, the next question is: *how does a team decide whether a branch is good enough to merge?* That is the art and discipline of code review and pull requests.