---
title: "Version Control with Git"
area: "Software Engineering Foundations"
topic: "Working with Code"
tags: [git, version-control, branches, commits]
---

# Version Control with Git

*Part of [[working-with-code-moc|Working with Code]] · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

**In one line:** Git is a tool that saves snapshots of your project over time so you can change it safely, work with others, and undo mistakes.

**Picture this:** Imagine writing an essay and hitting "Save As" every time you finish a paragraph: *essay-v1*, *essay-v2*, *essay-v3*. If version 3 goes wrong, you reopen version 2. Git does this automatically for code, but smarter.

**How it actually works:** When you finish a chunk of work you make a *commit* — a labelled snapshot of every file. Commits line up in history, so you can always travel back. A *branch* is a parallel copy where you try an idea without disturbing the main version. When the idea works, you *merge* the branch back in.

**In the real world:** Every engineer at companies like GitHub, Spotify and NASA's Mars rover teams uses Git. Thousands of people edit the Linux operating system this way — Git was literally created in 2005 to manage Linux's code.

**Why you'd use it (and when not to):** Use it for anything you'll change more than once — code, configs, even notes. For a one-off throwaway script, it can feel like overkill.

**Connects to:** [[code-review-pull-requests]] · [[automated-testing]]
