---
title: "Automated Testing"
area: "Software Engineering Foundations"
topic: "Code Quality"
tags: [automated-testing, unit-tests, regression, code-quality, software-engineering]
---

# Automated Testing

*Part of [[code-quality-moc|Code Quality]] · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

## In one line

Automated testing is writing extra code whose only job is to check that your real code still does what it is supposed to do — and running those checks automatically every time you make a change.

## Picture this

Imagine you work in a factory that makes locks. Every time the production line spits out a new lock, a robot arm grabs it and tries a key in it: does it turn? Does it lock again? The robot does this in two seconds, thousands of times a day, without getting tired. If a batch comes out wrong, the alarm goes off before any broken locks leave the building.

Automated tests are that robot arm — except for code. Every time you change your program, your tests run in seconds and tell you whether the locks still work.

## How it actually works

When you write a program, you have **production code** — the real thing your users run — and **test code** — a second program whose only job is to call your production code and check the answers.

A test does three things:
1. **Arrange** — set up the data or situation needed for the test.
2. **Act** — call the piece of code you want to check.
3. **Assert** — check that the result matches what you expected. If it does not, the test fails.

The most common kind is a **unit test** (a test that checks one small, isolated piece of code — a single function, not the whole program). Unit tests are fast because they do not touch databases, networks, or files; they just call a function and inspect its return value.

Tests are wired into your development process so they run automatically — usually when you save a file, push code to a repository, or open a pull request. A **test runner** (a tool like `pytest` for Python or `Jest` for JavaScript) collects all your test functions, executes them one by one, and prints a summary: how many passed, how many failed, and exactly which ones failed.

A **regression** is when a change to one part of the code accidentally breaks something that used to work. Because you are not always looking at every part of the system when you change one part, regressions are easy to create and hard to catch by hand. Automated tests catch them the moment they appear.

When all tests pass — a "green build" — you have evidence that the code behaves as specified. That evidence gives you the confidence to change or improve code without being terrified you broke something invisible.

## Worked example

Say you write a Python function that calculates a delivery surcharge:

```python
# production code — surcharge.py
def delivery_surcharge(order_total):
    """Returns the surcharge: 10 % if order < £50, else £0."""
    if order_total < 50:
        return round(order_total * 0.10, 2)
    return 0.0
```

Now you write tests:

```python
# test code — test_surcharge.py
from surcharge import delivery_surcharge

def test_small_order_gets_surcharge():
    # Arrange
    total = 30.00
    # Act
    result = delivery_surcharge(total)
    # Assert
    assert result == 3.00, f"Expected 3.00 but got {result}"

def test_large_order_no_surcharge():
    assert delivery_surcharge(50.00) == 0.0

def test_boundary_just_below_50():
    assert delivery_surcharge(49.99) == 5.00  # 10 % of 49.99 = 4.999 → rounds to 5.00
```

Run them:

```bash
$ pytest test_surcharge.py -v
PASSED  test_small_order_gets_surcharge
PASSED  test_large_order_no_surcharge
PASSED  test_boundary_just_below_50
3 passed in 0.04s
```

Now imagine a colleague changes the threshold from `< 50` to `<= 50` by mistake. The next run immediately fails `test_large_order_no_surcharge`. The robot arm catches the broken lock before it ships.

## In the real world

Stripe — the payments company — processes millions of transactions a day. Every time an engineer changes the code that calculates fees, a suite of thousands of automated tests runs inside a CI/CD pipeline (**Continuous Integration / Continuous Delivery** — a system that automatically builds, tests, and deploys code). If any test fails, the change is blocked from reaching production. No customer ever sees the broken version. Engineers at Stripe can ship dozens of updates per day precisely because they trust the test suite to catch mistakes instantly.

## Common misconceptions

**People think tests prove code is bug-free — actually they only prove the cases you thought to test.** If you never test an edge case (e.g., a negative order total), a bug there stays hidden. Tests shrink your bug surface; they do not eliminate it.

**People think writing tests slows you down — actually it speeds up future changes.** Writing the first test takes a few minutes. But over months of development, tests save hours of manual clicking-through-the-app to check nothing broke. The investment front-loads cost and back-loads speed.

**People think tests are only for big companies — actually they matter most when one person is changing code quickly.** A solo developer working fast is exactly the person most likely to break something without noticing. Tests are a safety net for everyone.

## How it relates & differs

| Concept | Relates to Automated Testing | Differs from Automated Testing |
|---|---|---|
| [[clean-code-refactoring\|Clean Code & Refactoring]] | Tests are what make safe refactoring possible: you tidy the code and re-run the tests to confirm behaviour is unchanged | Refactoring is about restructuring code; tests are about verifying it — separate activities that depend on each other |
| [[version-control-with-git\|Version Control with Git]] | Tests typically run automatically on every commit or push; git provides the trigger point | Git tracks *what* changed; tests check *whether* the change is safe |
| [[code-review-pull-requests\|Code Review & Pull Requests]] | CI systems block a pull request from merging if tests fail — tests are an automated reviewer that runs before any human looks | Code review is human judgement about design and clarity; tests are automated judgement about correctness |

## Why you'd use it (and when not to)

Use automated tests whenever code will be changed more than once — which is almost always. The payoff grows the longer a codebase lives and the more people touch it. The main trade-off is up-front time: writing a good test suite takes real effort, and badly written tests (ones that test implementation detail rather than behaviour) break constantly and destroy trust in the suite. When you are writing a one-off throwaway script you will delete tomorrow, or rapidly prototyping to see if an idea even works, automated tests may genuinely not be worth it yet. The honest rule: if this code matters tomorrow, test it.

## Check yourself

**Memory hook:** Tests are the factory robot that catches broken locks before they ship — write them once, run them forever.

**Q1: What is a regression?**
A: A regression is when a change to one part of the code accidentally breaks behaviour that used to work correctly somewhere else.

**Q2: What do the three steps Arrange, Act, Assert mean in a unit test?**
A: Arrange sets up the data you need; Act calls the function under test; Assert checks that the result matches what you expected.

**Q3: Why do automated tests give you the confidence to change code?**
A: Because after any change you can run the full suite in seconds and see whether existing behaviour is still correct — if everything passes, you have evidence (not a guarantee, but strong evidence) that you have not broken anything already tested.

## Connects to

[[clean-code-refactoring|Clean Code & Refactoring]] · [[version-control-with-git|Version Control with Git]] · [[code-review-pull-requests|Code Review & Pull Requests]] · [[idempotency|Idempotency]]