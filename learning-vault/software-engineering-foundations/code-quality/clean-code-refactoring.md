---
title: "Clean Code & Refactoring"
area: "Software Engineering Foundations"
topic: "Code Quality"
tags: [refactoring, clean-code, readability, maintainability, software-engineering, testing]
---

# Clean Code & Refactoring

*Part of [[code-quality-moc|Code Quality]] · [[software-engineering-foundations-moc|Software Engineering Foundations]]*

## In one line

Refactoring means changing the *shape* of your code — its names, structure, and layout — without changing what it actually *does*, so future-you (and everyone else) can still understand it six months from now.

## Picture this

Imagine you wrote directions to a friend's house on a napkin at 2 a.m.:

> *"Go fwd, L after thing, R near that place, park near stuff."*

You show up and it works — you found the house. But if someone else reads it, or if you read it a week later, you're lost. Now imagine rewriting those same directions clearly:

> *"Drive north on Oak Street for 2 km. Turn left at the traffic light on Maple Ave. Turn right onto River Road. Park in the lot beside the blue water tower."*

Same route. Same destination. Totally different readability. That rewrite *is* refactoring: you didn't change where the directions lead — you changed how clearly they're expressed.

## How it actually works

**Refactoring has one golden rule:** the program's *behaviour must stay identical*. You are not adding features, fixing bugs, or making it faster. You are only improving the shape of the code.

Here is what "shape" means in practice:

**1. Naming.** Variables, functions, and classes should say *what they are*, not *how they were implemented* or *when you wrote them*. A variable called `x` or `temp2` makes every reader do mental work. A variable called `total_order_price_usd` does the explaining for you.

**2. Function size.** A function that is 200 lines long is doing too many things at once. When a function does only *one thing*, you can name it precisely, test it in isolation, and reuse it elsewhere. The rule of thumb: if you can't describe what a function does in one short sentence, it should be split.

**3. Structure.** Repeated blocks of code (copy-pasted three times) are a maintenance trap — fix a bug in one copy and forget the other two. Refactoring extracts the repeated logic into one place.

**Why does all this matter?** Because code is read far more often than it is written. A feature you build in two hours might be read, debugged, and modified by five different people over two years. Readable code reduces mistakes, speeds up debugging, and makes adding new features less scary.

**The safety net: tests.** Before you change *any* code during a refactor, your automated tests must be passing (green). The tests are your proof that the behaviour hasn't changed. If you break a test during a refactor, you know immediately — and you haven't shipped anything yet. This is called *refactoring under green tests*, and it is non-negotiable.

## Worked example

Here is a real Python function pulled from a data pipeline script. It works, but it is messy.

**Before refactoring:**

```python
def proc(d):
    r = []
    for i in d:
        if i[2] > 0:
            r.append((i[0], i[1], i[2] * 1.1))
    return r
```

Can you tell what this does? You'd have to trace it mentally: iterate over `d`, check `i[2]`, multiply by 1.1... Eventually you might guess it applies a 10 % price increase to items with a positive quantity. But you shouldn't have to guess.

**After refactoring:**

```python
def apply_price_increase(orders: list, increase_rate: float = 0.10) -> list:
    """Return orders with price increased, skipping zero-quantity rows."""
    updated_orders = []
    for order in orders:
        product_id, quantity, unit_price = order
        if quantity > 0:
            new_price = unit_price * (1 + increase_rate)
            updated_orders.append((product_id, quantity, new_price))
    return updated_orders
```

**What changed:**

| Before | After | Why |
|---|---|---|
| `proc` | `apply_price_increase` | Name says exactly what it does |
| `d`, `r`, `i` | `orders`, `updated_orders`, `order` | No decoding needed |
| `i[2] * 1.1` | `unit_price * (1 + increase_rate)` | The magic number `1.1` becomes a named parameter |
| No type hints | `list`, `float` | A reader knows what to pass in |

The function's output is **identical** for the same input. Tests that passed before still pass. Nothing broke — it just became readable.

## In the real world

At a real company like Shopify or a bank's data team, engineers add new features to the same codebase for years. A data pipeline that started as 50 lines of Python grows — patch by patch — into 3,000 lines. Without regular refactoring, that growth becomes a "big ball of mud": a mess so tangled that adding a new feature breaks three others, and no one is sure why.

Teams schedule deliberate **refactoring sprints** — periods where no new features are built, only the codebase's shape is improved. They also practice **boy scout rule** commits: "leave the code a little cleaner than you found it." Before you add a feature to a messy function, spend 15 minutes renaming its variables and extracting a helper. You did not change what the function does — but the next person (possibly you next week) will thank you.

## Common misconceptions

**People think refactoring means rewriting from scratch — actually**, refactoring is a series of *small, safe steps*, each one preserving correct behaviour. A total rewrite is risky and expensive. True refactoring changes one name, extracts one function, removes one duplication — then runs the tests, then does the next small step.

**People think refactoring makes code faster — actually**, refactoring is about *readability and structure*, not performance. Making code run faster is called *optimisation*, and it is a separate activity with different tradeoffs. Confusing the two leads to "optimised" code that is unreadable and full of bugs.

**People think you should refactor whenever the code feels messy — actually**, you should only refactor *when the tests are green*. Refactoring broken code hides the original bug, because you don't know whether a new failure was caused by the refactor or was already there. Green tests first, always.

## How it relates & differs

| Concept | Relates to Clean Code & Refactoring | Differs from Clean Code & Refactoring |
|---|---|---|
| [[automated-testing\|Automated Testing]] | Tests are the safety net that make refactoring safe — without them, you cannot verify behaviour is unchanged | Testing checks that code is *correct*; refactoring improves that code is *readable*. They are complementary, not the same thing. |
| [[version-control-with-git\|Version Control with Git]] | Git lets you make tiny refactoring commits with clear messages ("rename variable", "extract helper function") and revert instantly if something breaks | Git tracks *history*; refactoring improves *present-state quality*. Git doesn't tell you how to structure your code — it just remembers every version of it. |
| [[big-o-time-complexity\|Big-O / Time Complexity]] | Both care about code quality, and a well-structured (refactored) codebase makes it easier to spot inefficient algorithms | Big-O is about *how fast* code runs (performance); refactoring is about *how clearly* code reads (structure). You can have fast-but-unreadable code, or readable-but-slow code. |

## Why you'd use it (and when not to)

Refactor whenever you're about to add a feature to a messy area of code, or when a bug was hard to find because the code was tangled. The upfront cost (15–60 minutes of cleanup) pays back quickly as the codebase grows. However, avoid refactoring code that is *about to be deleted* — cleaning up throwaway code wastes time. Also avoid refactoring just before a critical deadline with no test coverage; without tests, you can't prove nothing broke. Prefer refactoring in small, frequent doses over large, infrequent overhauls — small steps are safer and easier to review.

## Check yourself

**Memory hook:** *"Refactor = same destination, better directions — always under green lights."*

---

**Q1: What is the one thing that must NOT change during a refactor?**

**A:** The external behaviour of the code — what it does, what it returns, what it produces. Only the internal structure (names, layout, size of functions) changes.

---

**Q2: Why should tests be green (passing) before you start refactoring?**

**A:** If tests are already failing before you start, you can't tell whether a new failure was caused by your refactor or was already there. Green tests give you a baseline: if a test breaks during the refactor, you know *your changes* caused it.

---

**Q3: You have a 150-line function called `do_stuff`. Is this a refactoring problem? What would you do?**

**A:** Yes. A 150-line function almost certainly does more than one thing, which makes it hard to name, test, and reuse. The fix is to identify the distinct steps inside it, extract each into a small, well-named function, and call those functions from the original one — keeping the overall behaviour identical.

## Connects to

[[automated-testing|Automated Testing]] · [[version-control-with-git|Version Control with Git]] · [[code-review-pull-requests|Code Review & Pull Requests]] · [[big-o-time-complexity|Big-O / Time Complexity]]