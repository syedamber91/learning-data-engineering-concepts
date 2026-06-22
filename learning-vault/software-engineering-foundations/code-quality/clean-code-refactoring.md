---
title: "Clean Code & Refactoring"
area: "Software Engineering Foundations"
topic: "Code Quality"
tags: [clean-code, refactoring, readability, maintainability]
---

# Clean Code & Refactoring

*Part of [[code-quality-moc|Code Quality]] · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

**In one line:** Refactoring means tidying the *shape* of code — better names, smaller pieces — without changing what it actually does.

**Picture this:** Think of a messy bedroom where everything still "works" but you can't find anything. Cleaning it doesn't add new furniture; it just makes the same room usable. Refactoring cleans code the same way.

**How it actually works:** Code is read far more often than it's written. So you rename `x` to `unpaid_invoices`, split a 200-line function into a few short ones, and delete duplicated blocks. Crucially, you do this while [[automated-testing|tests]] are green, so you can prove you didn't accidentally change the behaviour.

**In the real world:** When Twitter (now X) struggled with constant outages, large parts of the codebase were refactored from a tangled Ruby app into cleaner, separated services so engineers could safely make changes without the whole site falling over.

**Why you'd use it (and when not to):** Refactor when code is hard to understand or change. Avoid refactoring code you're about to delete, or "improving" working code with no tests — you might break it silently.

**Connects to:** [[automated-testing]] · [[code-review-pull-requests]]
