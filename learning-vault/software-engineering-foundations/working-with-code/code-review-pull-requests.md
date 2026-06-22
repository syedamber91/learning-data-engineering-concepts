---
title: "Code Review & Pull Requests"
area: "Software Engineering Foundations"
topic: "Working with Code"
tags: [code-review, pull-request, collaboration, quality]
---

# Code Review & Pull Requests

*Part of [[working-with-code-moc|Working with Code]] · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

**In one line:** A pull request is a polite "please check my changes" — it lets teammates read and approve your code before it joins the main project.

**Picture this:** Before a school magazine is printed, an editor reads each article, suggests fixes, and only then says "ready to print". A pull request (PR) is that editor's desk for code.

**How it actually works:** You make your changes on a branch (see [[version-control-with-git]]) and open a PR. Teammates see exactly what lines you added or removed, leave comments like "this could crash if the list is empty", and you push fixes. Once someone approves, the branch is merged into the main code.

**In the real world:** Google requires almost every code change to be reviewed by at least one other engineer before it ships — billions of users depend on that gate. Open-source projects like React use public PRs so anyone can suggest and review changes.

**Why you'd use it (and when not to):** Use reviews to catch bugs, share knowledge, and keep a written trail of *why* a change happened. For a solo hobby project, a full review process can slow you down — though reviewing your own PR after a coffee break still helps.

**Connects to:** [[version-control-with-git]] · [[automated-testing]] · [[clean-code-refactoring]]
