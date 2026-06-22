---
title: "Automated Testing"
area: "Software Engineering Foundations"
topic: "Code Quality"
tags: [testing, unit-tests, automation, regression, code-quality, ci]
---

# Automated Testing

*Part of [[code-quality-moc|Code Quality]] · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

*Part of Code Quality · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

← Prev: [[code-review-pull-requests|Code Review & Pull Requests]] · Next: [[clean-code-refactoring|Clean Code & Refactoring]] →

## Recap — where we just were

In the previous lesson you saw how a pull request creates a human gate: a teammate reads your diff, leaves comments, and only approves it when the code looks safe. But human reviewers are slow, expensive, and can only look at the code — they cannot run it and verify that it actually works. This lesson introduces the *automated* gate that runs in milliseconds, never gets tired, and fires on every single push without being asked.

---

## Level 1 — The big idea

**Automated testing** means writing extra pieces of code whose only job is to run your *real* code and confirm it still behaves correctly — automatically, every time something changes.

**Everyday analogy:** Think of the spell-checker built into your word processor. You do not manually proofread every paragraph after every keystroke; the software watches in the background and flags errors the moment they appear. Automated tests do the same thing for code. They sit alongside your program and, every time you make a change, they fire up and report back — "everything still works" or "something broke on line 42."

The verdict is a simple traffic light:

<!-- mermaid-source:
graph LR
    CODE[Your Code] --> RUNNER[Test Runner]
    TESTS[Test Code] --> RUNNER
    RUNNER --> PASS[Green — all tests pass]
    RUNNER --> FAIL[Red — a test failed]
-->
![[automated-testing-d1.svg]]

Green means "safe to ship." Red means "stop and fix before anyone else sees this."

That single loop — write code, run tests, fix until green — is the heartbeat of modern software development.

---

## Level 2 — How it actually works

Now that you have the picture, let's open the hood and see every moving part.

### What is one test, exactly?

A test is a tiny program that calls your real code with a *known input* and checks that the *output* matches what you expected. That is the entire idea.

<!-- mermaid-source:
graph TD
    A[1. Set up a known input] --> B[2. Call your real function]
    B --> C[3. Compare output to expected value]
    C --> D{Match?}
    D -->|Yes| PASS[PASS]
    D -->|No| FAIL[FAIL — tells you which line]
-->
![[automated-testing-d2.svg]]

If the output matches, the test passes. If not, the test runner tells you exactly what it got versus what it expected — far faster than you could debug manually.

### The three kinds of tests

**Unit tests** check the smallest possible piece — usually a single function — in complete isolation. They never touch a database or a network. They run in milliseconds each and form the base of every test suite.

**Integration tests** check that two or more pieces work *together* — for example, that your search function correctly queries the database. They are slower and more complex to write, but they catch bugs that unit tests miss because they test the *joints* between components.

**End-to-end tests** (E2E) simulate a real user clicking through the app: open the browser, type into the search box, check that the results appear. The most realistic but also the slowest and most fragile.

The healthy ratio has a name — the **test pyramid**:

<!-- mermaid-source:
graph TD
    E2E[End-to-end tests — few — slowest] --> INT[Integration tests — some — medium speed]
    INT --> UNIT[Unit tests — many — fastest]
-->
![[automated-testing-d3.svg]]

Most of your effort goes into the base: fast, isolated unit tests. You build up from there.

### How the test runner fits in

A **test runner** is a tool — **pytest** for Python, **Jest** for JavaScript, **JUnit** for Java — that:

1. Discovers all your test files automatically.
2. Runs every test function in sequence (or in parallel).
3. Catches failures and reports the exact file, line, and mismatch.
4. Prints a final summary: N passed, M failed.

You do not trigger this by hand on every commit. You wire it up to run automatically — either as a **pre-commit hook** on your machine or (more importantly) as part of **Continuous Integration** (CI): a remote server that GitHub or GitLab spins up whenever you push a branch.

<!-- mermaid-source:
sequenceDiagram
    participant DEV as You
    participant GH as GitHub
    participant CI as CI Server
    participant TR as Test Runner

    DEV->>GH: git push feature/search
    GH->>CI: Trigger build
    CI->>TR: Run all tests
    TR->>CI: 47 passed  0 failed
    CI->>GH: Mark commit green
    GH->>DEV: PR ready to review
-->
![[automated-testing-d4.svg]]

When CI marks a commit green, every reviewer on your pull request can see it instantly — proof that the new code did not break anything that existed before.

---

## Level 3 — See it with real numbers

Let's make this concrete with the same to-do app from the previous lesson. You have a Python function that filters tasks by a search query.

**The real function (`src/utils.py`):**

```python
def filter_tasks(tasks, query):
    if not query:
        return tasks
    return [t for t in tasks if query.lower() in t["title"].lower()]
```

**Your test file (`tests/test_utils.py`) — four tests, five fake tasks:**

```python
from src.utils import filter_tasks

SAMPLE_TASKS = [
    {"id": 1, "title": "Buy groceries"},
    {"id": 2, "title": "Write unit tests"},
    {"id": 3, "title": "Read the Python docs"},
    {"id": 4, "title": "Buy birthday present"},
    {"id": 5, "title": "Review pull request"},
]

def test_filter_finds_matching_tasks():
    result = filter_tasks(SAMPLE_TASKS, "buy")
    assert len(result) == 2                      # tasks 1 and 4
    assert result[0]["title"] == "Buy groceries"

def test_filter_is_case_insensitive():
    result = filter_tasks(SAMPLE_TASKS, "BUY")
    assert len(result) == 2                      # same two tasks

def test_empty_query_returns_all():
    result = filter_tasks(SAMPLE_TASKS, "")
    assert len(result) == 5                      # nothing filtered

def test_no_match_returns_empty_list():
    result = filter_tasks(SAMPLE_TASKS, "xyzzy")
    assert len(result) == 0
```

**Running the suite:**

```bash
$ pytest tests/test_utils.py -v

tests/test_utils.py::test_filter_finds_matching_tasks    PASSED  [0.002s]
tests/test_utils.py::test_filter_is_case_insensitive     PASSED  [0.001s]
tests/test_utils.py::test_empty_query_returns_all        PASSED  [0.001s]
tests/test_utils.py::test_no_match_returns_empty_list    PASSED  [0.001s]

========================= 4 passed in 0.08s =========================
```

Now imagine you later refactor `filter_tasks` and accidentally remove the `.lower()` call on `query`. The case-insensitive test catches it immediately, before any reviewer even opens the PR:

```bash
$ pytest tests/test_utils.py -v

tests/test_utils.py::test_filter_is_case_insensitive     FAILED

AssertionError: assert 0 == 2
  Left:  0   (what the broken code returned)
  Right: 2   (what the test expected)
```

Zero users harmed. The bug never reached `main`. That is the entire promise of automated testing.

---

## Level 4 — In the real world & common traps

### Named real-world use case: Shopify's deployment pipeline

Shopify runs one of the largest e-commerce platforms on Earth — millions of transactions per day. Their engineers push code dozens of times daily. Before any commit touches production, their CI pipeline runs **over 100,000 automated tests**, completing in under 10 minutes because they execute in parallel across hundreds of machines. If a single test turns red, the deployment is blocked automatically — no human has to remember to check. The tests are as much a part of the product as the code itself.

### Common misconceptions

**People think: "Tests slow me down — I'll write them later."**
Actually, tests save time over the life of the project. A bug caught by a test costs 10 seconds to fix. The same bug found by a customer in production can mean hours of debugging, emergency hotfixes, and incident reviews. "Later" almost never arrives, and by then the code is so entangled that writing tests becomes twice as hard.

**People think: "If all tests pass, the code is correct."**
Actually, tests only verify what you remembered to test. A suite with 500 green tests can still ship a serious bug — because nobody wrote the test for that specific edge case. Think of green tests as "no *known* problems," not "definitely works." This is why code review and monitoring in production are still essential even with a full test suite.

**People think: "More tests always means better software."**
Actually, poorly written tests create *false confidence* and become a maintenance burden. A test that calls a function but never checks the output contributes to your test count and runs in CI, yet catches nothing. Quality of assertions matters more than quantity of test files.

---

## Level 5 — Expert view

### How automated testing relates to — and differs from — neighbouring concepts

| Concept | What it is | How it connects | Key difference |
|---|---|---|---|
| **Code Review** | A human reads your diff before merge | Both are quality gates before code reaches main | Reviews are manual, subjective, slow; tests are automated, objective, instant |
| **Clean Code & Refactoring** | Restructuring code for clarity without changing behaviour | Tests are what make refactoring *safe* — change the structure, run the suite, see whether anything broke | Clean code is about readability; tests are about correctness |
| **Version Control** | Saving snapshots of code over time | CI links the two: tests run automatically against each new commit or branch | Git tracks *what* changed; tests validate *whether that change works* |

### Trade-offs — when tests give you the most value

Tests pay off the most on:

- **Pure functions** with clear inputs and outputs (easiest to write and maintain).
- **Business-critical logic**: payment calculations, access control, data transformations.
- **Code that many people touch**: shared utilities, core libraries, APIs.

Tests are harder to justify for:

- Throwaway scripts that run exactly once.
- Pixel-level UI layout (snapshot tests exist but are brittle).
- Thin wrappers around external services you cannot control in tests.

### Test doubles — a concept worth knowing

When your code talks to a database or an external API, you do not want unit tests to hit the real thing: it is too slow, unreliable, and sometimes costs money. Engineers use **mocks** and **stubs** — fake versions of those external services that return predictable values. This keeps unit tests fast and isolated from the outside world.

### The coverage trap

Most teams measure **code coverage**: what percentage of your code lines were executed by at least one test. A target of "80% coverage" sounds rigorous, but coverage tells you *what was executed*, not *whether it was verified correctly*. A test that calls every line but never asserts anything gives you 100% coverage and catches zero bugs. Treat coverage as a floor that reveals *untested areas*, not a ceiling that proves correctness.

### The test-first mindset (**TDD**)

Some engineers write the test *before* the real code — a practice called **Test-Driven Development (TDD)**. The loop is: write a failing test → write the minimum code to make it pass → refactor. TDD forces you to think about the interface (what should this function take and return?) before the implementation. It is a powerful discipline but not universally adopted; many engineers write tests after the code and still ship high-quality software. What matters is that the tests exist before the code ships.

---

## Check yourself

**Memory hook:** "Tests are your safety net — they let you swing on the high wire of refactoring without fear of falling."

**Q1: What is the difference between a unit test and an integration test?**
A unit test checks a single function in isolation — no database, no network, just a known input and a checked output. An integration test checks that two or more pieces of the system work *together*, such as a function that queries a real (or test) database and returns the right rows.

**Q2: Why do engineers say "green tests build confidence to change code"?**
When a passing test suite exists, you can restructure or extend the code and immediately see whether you broke something. Without tests, every change is a leap of faith: you hope nothing broke, but you cannot know until a user reports a bug.

**Q3: A teammate says "all 500 tests pass, so we're safe to deploy." What is the honest reply?**
Passing tests mean "no *known* problems," not that the code is definitely correct. Tests only cover what someone thought to test. Untested edge cases can still harbour serious bugs. Always combine a green test suite with thorough code review and live monitoring in production.

---

## Connects to

[[code-review-pull-requests|Code Review & Pull Requests]] · [[version-control-with-git|Version Control with Git]] · [[clean-code-refactoring|Clean Code & Refactoring]]

---

## Coming up next

**[[clean-code-refactoring|Clean Code & Refactoring]]** — Now that tests give you a safety net that catches regressions automatically, the next lesson shows you how to use that net: restructuring your code to be cleaner and simpler without changing what it *does*, so the project stays readable as it grows.