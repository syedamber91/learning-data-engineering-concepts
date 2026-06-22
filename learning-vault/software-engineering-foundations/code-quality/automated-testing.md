---
title: "Automated Testing"
area: "Software Engineering Foundations"
topic: "Code Quality"
tags: [testing, unit-test, regression, quality]
---

# Automated Testing

*Part of [[code-quality-moc|Code Quality]] · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

**In one line:** Automated tests are extra bits of code whose only job is to check that your real code still does the right thing — run automatically, every time.

**Picture this:** A car factory has a robot that presses every door handle 1,000 times before the car ships. You don't trust your memory that "it probably still works" — the robot proves it. Tests are that robot for your code.

**How it actually works:** You write a small test that gives your code an input and checks the output. For example: "add(2, 2) should return 4". A *unit test* checks one small piece. You run all tests with one command; if a future change breaks something, a test turns red and tells you exactly what failed — that broken-again problem is called a *regression*.

**In the real world:** NASA, banks, and companies like Stripe run thousands of automated tests on every change. Stripe processes real money, so a test suite guards against a bug that could mischarge millions of customers.

**Why you'd use it (and when not to):** Tests give you the confidence to change code without fear. They cost time to write, so for a five-line experiment you might skip them — but anything others rely on should be tested.

**Connects to:** [[clean-code-refactoring]] · [[code-review-pull-requests]] · [[idempotency]]
