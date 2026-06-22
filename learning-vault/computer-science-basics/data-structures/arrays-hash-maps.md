---
title: "Arrays & Hash Maps"
area: "Computer Science Basics"
topic: "Data Structures"
tags: [arrays, hash-maps, data-structures, lookup, python, performance, computer-science]
---

# Arrays & Hash Maps

*Part of [[data-structures-moc|Data Structures]] · [[computer-science-basics-moc|Computer Science Basics]]*

← Prev: [[clean-code-refactoring|Clean Code & Refactoring]] · Next: [[big-o-time-complexity|Big-O / Time Complexity]] →

## Recap — where we just were

In [[clean-code-refactoring|Clean Code & Refactoring]] you learned that the names you give your code carry meaning — `unshipped_order_ids` tells its own story, while `x` tells nothing. Now notice two ways to fetch data: `orders[0]` and `orders["ORD-9918"]`. Both use brackets. Both look similar. But they are hiding completely different machines underneath. This lesson opens the hood.

---

## Level 1 — The big idea

A **data structure** is a way of organising information in memory so it is fast and easy to retrieve later. The two most universal data structures — found in every language, every pipeline, every system — are the **array** and the **hash map**.

- An **array** stores items in a numbered row. You find things by their *position number* (called an index).
- A **hash map** stores items under a *label* (called a key). You find things by that label.

**Everyday analogy:** Picture a row of school lockers, each with a number painted on the door. If you know your locker is number 47, you walk straight there — no searching. That is an array. Now picture a dictionary. You want the definition of "photosynthesis". You do not read from page 1; you jump straight to P. That is a hash map.

<!-- mermaid-source:
graph LR
    subgraph ARRAY
        A0[slot 0 Alice] --> A1[slot 1 Bob] --> A2[slot 2 Carol]
    end
    subgraph HASHMAP
        K1[key alice] --> V1[Alice Chen]
        K2[key bob] --> V2[Bob Smith]
        K3[key carol] --> V3[Carol Park]
    end
-->
![[arrays-hash-maps-d1.svg]]

The rule that drives every design decision: **choose the structure that matches how you will look things up.** Know the position? Use an array. Know the name? Use a hash map.

---

## Level 2 — How it actually works

Now that you have the intuition, let's trace the actual mechanism for each structure.

### Arrays: one arithmetic step

When you create an array, the computer books a row of *consecutive memory slots* and records the address of the first one. To fetch item at index `i`, it does one calculation:

```
address of item[i] = start_address + (i × size_of_one_item)
```

One arithmetic operation. One memory jump. No searching. This is called **random access** — "random" meaning *any* item, instantly, not that it is unpredictable.

<!-- mermaid-source:
graph LR
    subgraph Memory
        M0[1000: 10] --> M1[1004: 20] --> M2[1008: 30] --> M3[1012: 40] --> M4[1016: 50]
    end
    IDX[want index 3] --> CALC[1000 + 3x4 = address 1012]
    CALC --> M3
-->
![[arrays-hash-maps-d2.svg]]

**The hidden cost:** if you want to find the item with value `40` but you do not know its index, you must check every slot in order: 1000, 1004, 1008, 1012… This is a **linear scan** and gets slow when the array is large.

### Hash maps: one computation, then jump

A hash map uses a **hash function** — a formula that converts any key into a slot number called a **bucket**. The steps are always the same:

1. You provide a key, e.g. `"alice"`.
2. The hash function turns `"alice"` into a number, e.g. `7`.
3. The map stores or retrieves your value at bucket 7.
4. Done — no scan of all entries required.

<!-- mermaid-source:
graph LR
    alice[alice] --> HF[hash function]
    bob[bob] --> HF
    HF --> B7[bucket 7]
    HF --> B2[bucket 2]
    B7 --> V1[Alice Chen]
    B2 --> V2[Bob Smith]
-->
![[arrays-hash-maps-d3.svg]]

**What is a hash collision?** Occasionally, two different keys land on the same bucket. The map handles this by keeping a short list at that bucket and scanning only those few entries. With a well-designed hash function, collisions are rare, so lookup stays nearly instant. Your language handles all of this automatically.

---

## Level 3 — See it with real numbers

You are building a sign-up form for an app with 1,000,000 existing users. Each time someone types a new username, you must answer in under one millisecond: *"Is this name already taken?"*

### Option A — list (Python dynamic array)

```python
usernames = ["alice", "bob", "carol", ..., "zoe_2026"]  # 1,000,000 names

def is_taken(name, usernames):
    for existing in usernames:    # worst case: scan all 1,000,000
        if existing == name:
            return True
    return False

is_taken("zoe_2026", usernames)   # up to 1,000,000 comparisons
```

Worst case: 1,000,000 comparisons. At 10,000 sign-ups per second, this quickly becomes a bottleneck.

### Option B — dict (Python hash map)

```python
# Build once — one pass through all names
username_set = {name: True for name in usernames}   # 1,000,000 entries

def is_taken(name, username_set):
    return name in username_set   # one hash computation

is_taken("zoe_2026", username_set)   # effectively instant
```

One hash computation regardless of whether there are 1,000 or 10,000,000 users.

### At a glance

| Operation | List of 1M names | Dict of 1M names |
|---|---|---|
| Check if name exists | up to 1,000,000 steps | ~1 step |
| Get item at position 500,000 | 1 step | not supported |
| Memory used | ~8 MB | ~50 MB |
| Insert a new name | append: ~1 step | ~1 step |

Hash maps buy speed at the cost of extra memory — a trade-off you will see constantly in data engineering.

---

## Level 4 — In the real world & common traps

### Named use case: counting song plays at Spotify

Spotify's data engineering team processes billions of listening events per day. Every time a user plays a song, a pipeline must increment a counter for that song title. Using a list would require finding the right song among hundreds of millions of entries on every event. Instead, the pipeline uses a hash map where the song title is the key and the play count is the value:

```python
play_counts["Blinding Lights"] += 1   # one hash lookup, one increment
```

This pattern — hash map as an accumulator — appears in virtually every [[batch-vs-streaming|Batch vs Streaming]] aggregation job and in [[data-quality-validation|Data Quality & Validation]] checks that need to look up reference values instantly. It is the engine behind the phrase "fast lookups" in data engineering.

### Common misconceptions

**People think: "Hash maps are always faster than arrays."**
Actually: Arrays beat hash maps when you already know the *position*. `scores[42]` is a single memory read — no hash function needed. For sequential iteration (looping through every item in order), arrays are also faster because their memory is packed tightly, which CPU caches love. Hash maps are faster only when you are looking up by an arbitrary key.

**People think: "A Python `list` and an array are the same thing."**
Actually: A Python `list` is a *dynamic array* — it grows by doubling its memory block when full, copying everything over. Under the hood it is still position-based storage. A Python `dict` is the hash map. They share bracket syntax but are completely different machines. Confusing them leads to picking the wrong one for the job.

**People think: "Hash map lookup is always instant — guaranteed."**
Actually: Hash maps are *average-case* constant time. In the rare worst case — many keys colliding into the same bucket — lookup degrades toward a linear scan of that bucket. Good hash functions and properly sized maps make this extremely uncommon in practice, but "always instant" overstates it. The next lesson will give you the precise notation to express this.

---

## Level 5 — Expert view

### How arrays and hash maps compare to neighbouring structures

| | Array | Hash Map | Linked List | DB Table with index |
|---|---|---|---|---|
| Find by position | instant | not supported | slow scan | slow scan |
| Find by key | slow scan | instant | slow scan | instant |
| Memory layout | compact contiguous | sparse with overhead | scattered pointers | on disk |
| Insert in the middle | slow - must shift | fast | fast | fast |
| Preserves order | yes - by index | not always | yes - by chain | depends on index |

(**Linked List** is not currently in this vault.)

The "DB Table with index" row connects directly to [[tables-keys-sql-basics|Tables, Keys & SQL Basics]]. When a database fetches a row by primary key, it uses a structure similar in spirit to a hash map (or, more precisely, a **B-tree**, not yet in this vault). The [[indexing|Indexing]] lesson shows how databases build these lookup shortcuts efficiently on disk.

### When to use each one

**Choose an array when:**
- You iterate through every item in order.
- You frequently access the Nth item by its index.
- Memory is tight — arrays are the most compact structure.
- Data is a natural sequence: time series, pixel buffers, daily readings.

**Choose a hash map when:**
- You look things up by name, username, ID, or any non-integer key.
- You need fast existence checks ("is this email already registered?").
- You are counting or grouping: event tallies, word counts, deduplication.
- You need to attach metadata to each key.

### Edge cases worth knowing

**Unhashable keys in Python:** You cannot use a `list` as a dict key because lists are mutable — if the list changed after insertion, the hash would be wrong and the entry would be lost. Use immutable types as keys: strings, integers, tuples.

**Ordering:** Python `dict` preserves insertion order since Python 3.7. Many other languages' hash map implementations do not guarantee any order. If you need sorted output, sort the keys separately — a hash map is the wrong tool for sorted retrieval.

**Resize cost:** When a hash map fills past a threshold (its **load factor**), it allocates a larger bucket array and recomputes every entry's position. This occasional resize is expensive, but it happens rarely enough that the average cost per operation stays low. Most languages tune this automatically.

---

## Check yourself

**Memory hook:** *Arrays are numbered lockers. Hash maps are labelled drawers.*

**Q1: You have 500,000 daily temperature readings stored in order. You need the reading from minute 312,000. Array or hash map — which is faster, and why?**
A: Array. You know the position (312,000), so the computer does one arithmetic step — `start + 312000 × element_size` — and jumps directly there. No searching required.

**Q2: You are building a URL shortener. Given a short code like `"x7k2"`, you need to return the full URL in under a millisecond. Which structure do you use?**
A: Hash map. You are looking up by a string key, not by position. The hash map computes one hash of `"x7k2"`, jumps to the right bucket, and returns the URL — effectively constant time no matter how many URLs are stored.

**Q3: A teammate says "Python dicts are always O(1), full stop." What is the more precise answer?**
A: Python dicts are *average-case* O(1). In the rare worst case — many keys colliding into the same bucket — lookup degrades toward O(n). Good hash functions and reasonable load factors keep this from happening in practice, but the guarantee is probabilistic, not absolute. (The next lesson will explain O(1) and O(n) precisely.)

---

## Connects to

[[clean-code-refactoring|Clean Code & Refactoring]] · [[big-o-time-complexity|Big-O / Time Complexity]] · [[tables-keys-sql-basics|Tables, Keys & SQL Basics]] · [[indexing|Indexing]] · [[batch-vs-streaming|Batch vs Streaming]] · [[data-quality-validation|Data Quality & Validation]]

---

## Coming up next

**[[big-o-time-complexity|Big-O / Time Complexity]]** — You have been using words like "instant" and "slow scan" informally throughout this lesson; Big-O notation is the universal, precise language engineers use to describe exactly how an algorithm's speed changes as its input grows, turning those informal words into numbers you can compare, reason about, and argue over in code reviews.