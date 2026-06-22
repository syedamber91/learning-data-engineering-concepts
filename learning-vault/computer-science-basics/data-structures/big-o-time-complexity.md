---
title: "Big-O / Time Complexity"
area: "Computer Science Basics"
topic: "Data Structures"
tags: [big-o, time-complexity, algorithms, data-structures, performance, scalability]
---

# Big-O / Time Complexity

*Part of [[data-structures-moc|Data Structures]] · [[computer-science-basics-moc|Computer Science Basics]]*

## In one line

Big-O notation is a way of describing how much *more* work a piece of code has to do when you give it more data — specifically, how that extra work grows as the input gets bigger.

## Picture this

Imagine you lose your keys somewhere in your house. How long it takes you to find them depends on *how you search*:

- **You always check the same drawer first** — and your keys are always there. It doesn't matter if your house is 3 rooms or 30 rooms; you go straight to that drawer. That's **O(1)**: constant time.
- **You check every room one by one** — the bigger the house, the longer it takes. Double the rooms, double the time. That's **O(n)**: linear time.
- **You check every room AND, inside each room, check every item against every other item** — that explodes fast. Ten rooms becomes 100 checks; 100 rooms becomes 10,000 checks. That's **O(n²)**: quadratic time.

The "O" literally stands for "Order of" — as in, "what's the order of magnitude of effort here?"

## How it actually works

When we write code, we want to know: *if I have one million rows instead of one thousand, will my program slow down a little or a lot?* Big-O gives us a vocabulary to answer that without running the program first.

Here's the key insight: Big-O ignores constants and small details. It only cares about the *dominant growth pattern* as the input size — usually called **n** — gets very large.

Let's say a function does `3n + 7` operations. When n is a million, the `+7` is irrelevant and the `3` just scales everything by the same factor. Big-O strips those away and says: this is **O(n)**. What matters is the *shape* of the growth, not the exact count.

The three you'll see most often:

| Notation | Name | What it means |
|---|---|---|
| O(1) | Constant | Same work, no matter how big n gets |
| O(n) | Linear | Work grows in direct proportion to n |
| O(n²) | Quadratic | Work grows as the *square* of n |

There are others — O(log n), O(n log n), O(2ⁿ) — but those three are your foundation.

**Why does this matter?** Because a function that is O(n²) on 1,000 rows might be fast enough. On 1,000,000 rows, it does one *trillion* operations. The program doesn't just get slower — it becomes unusable.

## Worked example

Suppose you have a Python list of 1,000,000 user IDs and you want to check whether ID `42` is in it.

**Approach 1 — Linear scan (O(n)):**

```python
user_ids = [1, 2, 3, ..., 1_000_000]  # a plain list

def is_member_list(user_ids, target):
    for uid in user_ids:       # visits up to 1,000,000 items
        if uid == target:
            return True
    return False
```

Worst case: you scan all 1,000,000 IDs before deciding the target isn't there. That's 1,000,000 comparisons. Double the list → double the work. **O(n)**.

**Approach 2 — Hash set lookup (O(1)):**

```python
user_set = set(user_ids)  # build once: O(n) — but only once

def is_member_set(user_set, target):
    return target in user_set  # one hash computation, done
```

After the set is built, *every single lookup* is one operation, no matter if there are 1,000 or 1,000,000,000 IDs. **O(1)**.

**The numbers:** At 1,000,000 rows, the list scan might take ~50 ms. The set lookup takes ~0.05 ms — roughly 1,000× faster. At 100,000,000 rows, the gap is catastrophic. The set is still ~0.05 ms; the list scan could take *seconds*.

## In the real world

A data pipeline at a company like Uber ingests millions of ride records every day. During processing, the code needs to look up whether each driver ID exists in a table of approved drivers — a check performed tens of millions of times per hour.

If that lookup is O(n) — a scan through an unsorted list — the pipeline grinds to a halt as data volume grows. Engineers replace the scan with a hash-based lookup (O(1)) or a **B-tree** index (O(log n)), and suddenly the same pipeline handles 10× the data without needing 10× the machines. This is exactly why understanding Big-O is a job skill, not just a school skill.

## Common misconceptions

**People think Big-O tells you the exact speed of your code — actually, it tells you the *shape* of growth, not the real time.** An O(1) function could take 2 seconds if it does expensive work once. An O(n) function could take 0.001 ms per item on a tiny dataset. Big-O is about *scaling behaviour*, not wall-clock speed.

**People think O(n²) is always bad — actually, it depends on n.** Sorting 20 names with a quadratic algorithm is perfectly fine; you'd never notice. It only becomes a problem at scale. Always ask: "What is n in my actual situation?"

**People think a lower Big-O is always worth pursuing — actually, the constant factors matter in practice.** An O(n log n) algorithm with a huge constant might run slower than an O(n²) one for small inputs. Big-O is a guide for scale, not a substitute for measurement.

## How it relates & differs

| Concept | Relates to Big-O | Differs from Big-O |
|---|---|---|
| [[arrays-hash-maps\|Arrays & Hash Maps]] | The *reason* you choose a hash map over an array for lookups is Big-O: hash maps give O(1) lookup; arrays give O(n) scan. Big-O is the *why* behind the data structure choice. | Arrays & Hash Maps are data structures — physical things you use. Big-O is an analytical tool you use to *evaluate* those structures. |
| [[indexing\|Indexing]] | Database indexes exist to change a **full table scan** (O(n)) into a **B-tree** traversal (O(log n)). Understanding Big-O explains *why* indexes are so powerful. | Indexing is a database-level mechanism. Big-O is the notation you use to reason about the efficiency of that (or any other) mechanism. |
| [[tables-keys-sql-basics\|Tables, Keys & SQL Basics]] | When you query a table without a key-based index, the database does an O(n) scan of every row. Big-O explains the cost of different SQL query patterns. | SQL is a language for talking to databases; Big-O is a mathematical framework for analysing any algorithm, SQL-powered or otherwise. |

## Why you'd use it (and when not to)

Use Big-O thinking whenever you're choosing between two approaches and the dataset might grow — picking a data structure, designing a pipeline join, deciding whether to sort before searching. It is the single most useful tool for reasoning about whether code will still work at 100× the current data volume. The limit: Big-O ignores real-world constants, memory layout, cache behaviour, and I/O. For a 50-item list, stop worrying about it — measure instead. Big-O shines when n is large and unknown, not when n is small and fixed.

## Check yourself

**Memory hook:** Big-O is your "how bad does it get?" meter — the bigger the n, the more the shape matters.

**Q1: You have a sorted list of 1,000,000 numbers. You check whether 500,000 is in it by scanning from the start. What is the Big-O complexity of this approach?**
A: O(n) — linear. In the worst case (target is last or missing), you touch every one of the 1,000,000 elements.

**Q2: A function runs in O(n²). If n doubles from 100 to 200, roughly how many times more work does the function do?**
A: Four times more. O(n²) means work scales as n squared: 200² = 40,000 vs 100² = 10,000. Doubling n quadruples the work.

**Q3: You replace an O(n) membership check with an O(1) hash-set lookup. The dataset grows from 10,000 to 10,000,000 rows. How does the time for the O(1) lookup change?**
A: It doesn't — that's what O(1) means. Constant time is constant regardless of n.

## Connects to

[[arrays-hash-maps|Arrays & Hash Maps]] · [[indexing|Indexing]] · [[tables-keys-sql-basics|Tables, Keys & SQL Basics]]