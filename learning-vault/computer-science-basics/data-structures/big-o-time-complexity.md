---
title: "Big-O / Time Complexity"
area: "Computer Science Basics"
topic: "Data Structures"
tags: [big-o, time-complexity, algorithms, performance, computer-science, data-structures]
---

# Big-O / Time Complexity

*Part of [[data-structures-moc|Data Structures]] · [[computer-science-basics-moc|Computer Science Basics]]*

← Prev: [[arrays-hash-maps|Arrays & Hash Maps]] · Next: [[tables-keys-sql-basics|Tables, Keys & SQL Basics]] →

## Recap — where we just were

In [[arrays-hash-maps|Arrays & Hash Maps]] you discovered the most important performance gap in programming: a list scan that checks every item one by one versus a hash map that jumps straight to the answer in one step — a difference between trillions of operations and two million. **Big-O notation** is the shared language engineers use to *name* that gap precisely, compare any two algorithms, and predict how code will behave before it ever runs on a million-row dataset.

---

## Level 1 — The big idea

**Big-O** is a grade that tells you how the *amount of work* a piece of code does changes as the input grows. Not milliseconds — just the *shape of the growth*.

Think of it as a report card for scalability. Two algorithms might both finish in under a second today, but one falls apart at a million rows while the other barely notices. Big-O tells you which is which, *before* you ever need a million rows.

**Everyday analogy:** You need to find your friend's name in a list. Three scenarios:

1. Your friend is always at the top of every list — you check once and you are done.
2. You read every name from top to bottom until you find it.
3. You compare every name on the list against every other name, hunting for duplicates.

Scenario 1: the work never changes. Scenario 2: the work grows with the list. Scenario 3: the work grows with the *square* of the list length. Those three shapes are Big-O's three most common grades.

<!-- mermaid-source:
graph TD
    A[Input size n doubles] --> B1[O1 constant: work stays the same]
    A --> B2[On linear: work doubles]
    A --> B3[On2 quadratic: work quadruples]
-->
![[big-o-time-complexity-d1.svg]]

The grade ignores how fast your computer is and focuses only on how the work *scales*. That is the whole idea — a precise word for the shape of growth.

---

## Level 2 — How it actually works

Now that you have the shape in mind, let's trace exactly where these grades come from.

The key move: **count operations, not seconds.** A second depends on the hardware. An operation count depends only on how you wrote the code — and it holds true on any machine.

### Grading O(n) — the linear ramp

```python
for name in names:    # runs n times
    print(name)       # one operation per run
```

Total operations: n. If the list has 1,000 items you do 1,000 prints; if it has 1,000,000 you do 1,000,000. The work grows in a straight line with n. Grade: **O(n)**.

### Why we drop constants

Suppose the loop body does five things instead of one: `5 × n` total operations. Does that change the grade? No. Big-O drops constant multipliers because at very large n, whether each item costs 1 step or 5 steps is noise compared to whether you have n items or n² items to process. Keep only the *dominant term* — the part that grows fastest.

Rule: `5n + 3` → **O(n)**. `3n² + 100n + 7` → **O(n²)**.

### Grading O(n²) — the nested-loop cliff

Whenever you put a loop *inside* a loop, and both loops run n times:

```python
for i in names:       # n iterations
    for j in names:   # n iterations for each outer step
        compare(i, j) # 1 operation
```

Total: n × n = n² operations. Doubling the input quadruples the work. This is the shape that breaks production systems — the code review red flag you will recognise for the rest of your career.

### Grading O(1) — the flat line

A hash map lookup, or reading one array element by index, always does a fixed number of steps regardless of how many entries exist. Grade: **O(1)** — the work is *constant*.

### The logarithmic bonus: O(log n)

One more grade worth knowing right now. If an algorithm can *halve* the remaining work at each step — like opening a dictionary to the middle page, then the middle of whichever half remains — the total steps grow only as the *logarithm* of n. Doubling n adds just *one more step*.

<!-- mermaid-source:
graph LR
    S[1000 items] --> H1[500 items left]
    H1 --> H2[250 items left]
    H2 --> H3[125 items left]
    H3 --> H4[Found in about 10 steps total]
-->
![[big-o-time-complexity-d2.svg]]

Ten halvings covers a thousand items — that is log₂(1000) ≈ 10. This pattern, called **binary search**, is exactly how database indexes work under the hood. You will meet it again in [[indexing|Indexing]].

Here is the full ladder from best to worst:

<!-- mermaid-source:
graph TD
    Best[O1 constant] --> Good[O log n logarithmic]
    Good --> OK[On linear]
    OK --> Warn[On log n linearithmic]
    Warn --> Bad[On2 quadratic]
    Bad --> Terrible[O2n exponential]
-->
![[big-o-time-complexity-d3.svg]]

For data engineering, O(n log n) is roughly the practical ceiling. Anything worse will not survive contact with a million-row dataset.

---

## Level 3 — See it with real numbers

Your nightly pipeline receives two lists of order IDs, each containing **1,000,000 entries**. You must find which orders appear in both lists.

### Approach A — nested loop, O(n²)

```python
today     = [...]         # 1,000,000 IDs
yesterday = [...]         # 1,000,000 IDs

matches = []
for t in today:            # 1,000,000 iterations
    for y in yesterday:    # 1,000,000 iterations each time
        if t == y:
            matches.append(t)
```

Steps: 1,000,000 × 1,000,000 = **1,000,000,000,000** (one trillion).
At 1 billion operations per second: **~16 minutes per nightly run.**

### Approach B — hash map lookup, O(n)

```python
today         = [...]            # 1,000,000 IDs
yesterday_set = set(yesterday)   # one O(n) pass to build the set

matches = []
for t in today:                  # 1,000,000 iterations
    if t in yesterday_set:       # O(1) per check
        matches.append(t)
```

Steps: 1,000,000 (build set) + 1,000,000 (scan today) = **2,000,000**.
Same CPU: **~0.002 seconds.**

| | O(n²) nested loop | O(n) hash map |
|---|---|---|
| n = 1,000 | 1,000,000 steps | 2,000 steps |
| n = 1,000,000 | 1,000,000,000,000 steps | 2,000,000 steps |
| Time at 1B ops/s | ~16 minutes | ~0.002 seconds |
| Extra memory needed | almost none | ~8 MB for the set |

The code looks nearly identical. The Big-O grade is the difference between a pipeline that finishes before anyone wakes up and one still running at noon.

---

## Level 4 — In the real world & common traps

### Named use case: Uber's surge-pricing engine

Uber's surge-pricing system must, in real time, match open driver requests against active rider requests to compute pricing zones — thousands of times per second across millions of concurrent users. An early prototype used a naïve pairwise comparison (O(n²)). As the user base grew from thousands to millions, engine latency ballooned from milliseconds to minutes. Switching to a spatial-index approach — closer to O(n log n) — brought latency back under 100 ms. The wrong Big-O grade broke surge pricing at exactly the moment the product needed it most: peak demand.

### Common misconceptions

**People think: O(1) is always faster than O(n) in practice.**
Actually: Big-O ignores constant factors. If your O(1) hash lookup costs 500 nanoseconds and your O(n) loop runs over 4 items at 10 ns each, the loop finishes first. Big-O describes *scale behaviour*. For small, bounded inputs, simpler code often wins outright.

**People think: Big-O tells me how long my code will take.**
Actually: Big-O only tells you the *growth rate*. Two O(n) algorithms can differ by 100× in real runtime due to memory access patterns, CPU cache effects, and hardware. Use Big-O to compare approaches at scale; use a profiler to measure actual time.

**People think: lower Big-O always means better code.**
Actually: improving time complexity almost always costs memory — hash sets, indexes, caches all buy speed with RAM. A correct O(n²) algorithm on 200 rows beats a buggy O(n) one. Always weigh complexity against space, correctness, and readability, especially when the dataset is small and will never grow.

---

## Level 5 — Expert view

### How Big-O relates to concepts you have met and will soon meet

| Concept | Where Big-O appears | Typical grade |
|---|---|---|
| Arrays and Hash Maps | list scan vs hash lookup | O(n) vs O(1) |
| Indexing | B-tree index vs full-table scan | O(log n) vs O(n) |
| Tables, Keys and SQL Basics | primary-key lookup vs unindexed WHERE clause | O(log n) vs O(n) |

(See [[arrays-hash-maps|Arrays & Hash Maps]], [[indexing|Indexing]], and [[tables-keys-sql-basics|Tables, Keys & SQL Basics]] for the full story on each.)

### Trade-offs and edge cases

**Space–time trade-off.** Almost every improvement in time complexity costs more memory. Hash maps, indexes, caches — they all buy speed with RAM. You will make this trade-off on nearly every design decision in data engineering.

**Average vs. worst case.** A hash map lookup is O(1) *on average*. In a pathological case — all keys land in the same bucket — it degrades to O(n). Production systems use randomised hash seeds to prevent this from becoming a security exploit; the language handles it automatically, but it is worth knowing the guarantee is probabilistic.

**Amortized complexity.** Python's `list.append()` is O(1) *amortized*. Occasionally the list must copy itself into a larger block of memory (one O(n) event), but that happens rarely enough that the average cost per append stays O(1). A single call can be slow; the sequence as a whole is fast. Amortized analysis is how engineers reason about data structures that have occasional expensive operations hidden inside a cheap average.

**When Big-O does not matter.** If your dataset is always bounded at a few hundred rows, an O(n²) algorithm finishing in 0.5 ms is fine — and it is likely simpler to read and maintain. Reach for Big-O reasoning when data is large, unbounded, or growing. Applying it prematurely adds complexity for zero benefit.

---

## Check yourself

**Memory hook:** *"Big-O grades the growth curve — flat is O(1), ramp is O(n), cliff is O(n²)."*

**Q1: A function loops once through a list of n items and prints each one. What is its Big-O grade?**
A: O(n). The work grows in direct proportion to the number of items — double the list, double the prints. One loop over n items is the definition of linear.

**Q2: Why does Big-O drop constants like the "5" in "5n steps"?**
A: Because at very large n the constant becomes noise compared to how n itself grows. Big-O describes the shape of scaling, not the exact step count. Whether each step takes 1 ns or 5 ns does not change whether the algorithm is linear or quadratic — and at scale only the shape matters.

**Q3: Your code review reveals a loop nested inside a loop, both iterating over the same n-item dataset. What Big-O grade do you flag, and why is it dangerous at scale?**
A: O(n²). Each outer-loop iteration triggers a complete inner-loop pass, giving n × n total steps. Doubling the dataset quadruples the work. At one million rows that is one trillion operations — minutes of wall time in a pipeline expected to finish in seconds.

---

## Connects to

[[arrays-hash-maps|Arrays & Hash Maps]] · [[indexing|Indexing]] · [[tables-keys-sql-basics|Tables, Keys & SQL Basics]]

---

## Coming up next

[[tables-keys-sql-basics|Tables, Keys & SQL Basics]] — now that you can grade how fast any algorithm is, you are ready to meet the foundational data structure of every database: the table, its rows and columns, and the keys that turn O(n) scans into O(log n) lookups.