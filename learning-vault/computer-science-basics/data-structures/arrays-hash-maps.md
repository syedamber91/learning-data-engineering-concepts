---
title: "Arrays & Hash Maps"
area: "Computer Science Basics"
topic: "Data Structures"
tags: [arrays, hash-maps, data-structures, computer-science, performance, lookup]
---

# Arrays & Hash Maps

*Part of [[data-structures-moc|Data Structures]] · [[computer-science-basics-moc|Computer Science Basics]]*

## In one line
An **array** holds items in a numbered line so you can grab any one by its position; a **hash map** holds items by a label (called a key) so you can grab any one by its name in roughly one step.

## Picture this
**Array:** Imagine a row of numbered lockers in a school hallway — locker 1, locker 2, locker 3... If you want locker 47, you walk straight to it. You know *exactly* where it is because of the number. But if someone asks "which locker has the red jacket?", you have to open every single one until you find it.

**Hash map:** Now imagine a coat-check at a theatre. You hand in your coat, and they give you a ticket stub with a code like `"A7"`. The attendant uses that code to go directly to hook A7. When you want your coat back, you hand over `"A7"` and they retrieve it instantly — no searching, no counting.

## How it actually works

### Arrays
An array is a block of memory where every item sits at a fixed, evenly-spaced address. Because the spacing is uniform, the computer can calculate the exact memory location of item number *i* with a single formula:

```
address of item[i] = start_address + (i × size_of_one_item)
```

That calculation takes one step no matter how many items the array holds. This is called **O(1) random access** — "O(1)" means the time cost does not grow as the data grows; it is always constant.

The trade-off: to find an item *by its value* (e.g., "find the number 42 inside this array"), the computer has no shortcut. It may have to check every slot one by one. That is **O(n)** — if the array has a million items, you could need a million checks. Inserting in the middle is also costly: every item after the insertion point must shift one position to make room.

### Hash Maps
A hash map (also called a *hash table* or, in Python, a *dictionary*) stores pairs of **keys** and **values**. You provide a key (like `"username"`) and get back a value (like `"alice"`).

Here is the mechanism behind the speed:

1. You give the hash map a key — say, the string `"alice"`.
2. A built-in **hash function** (a math formula) converts `"alice"` into a number — say, `3`. This number acts as an index into a hidden internal array.
3. Your value is stored at position `3` of that internal array.
4. Next time you look up `"alice"`, the same hash function runs again, produces `3` again, and the value is retrieved in one step.

That is why lookup, insertion, and deletion are all **O(1) on average** — the hash function does the navigation.

One honest caveat: two different keys can sometimes hash to the same index. This is called a **collision**. Hash maps handle it automatically using techniques like **chaining** (storing a small list at that index) or **open addressing** (trying the next available slot). You rarely need to think about this, but it is real.

## Worked example

Suppose you are building a word-frequency counter. You have a list of 1,000,000 words from a book and want to know how often each word appears.

**With an array scan:** For each new word, you search every entry to see if it already exists. With a million unique words, each lookup can cost up to 1,000,000 comparisons. Total work: up to 1,000,000 × 1,000,000 = one trillion operations. Not acceptable.

**With a hash map:** Each word becomes a key; its count is the value.

```python
text = ["dragon", "castle", "dragon", "knight", "castle", "dragon"]

word_count = {}   # a hash map in Python

for word in text:
    if word in word_count:        # O(1) lookup
        word_count[word] += 1
    else:
        word_count[word] = 1      # O(1) insert

print(word_count)
# {'dragon': 3, 'castle': 2, 'knight': 1}
```

Each lookup and each insert is O(1). Processing 1,000,000 words costs roughly 1,000,000 operations total — not one trillion. The difference between those two numbers is the difference between "finishes in a second" and "finishes in eleven days."

If instead you needed to access words *by position* — "give me the 50,000th word in the book" — you would use an array, because it gives you that in one step.

## In the real world

**Spotify's deduplication pipeline** — When Spotify processes hundreds of millions of play events per day, it needs to detect duplicates: was this exact event already recorded? Storing all seen event IDs in a hash map (or a **hash set**, which is a hash map without values) means every deduplication check is O(1), even across hundreds of millions of entries. An array-based scan would be fatally slow.

**NumPy arrays in data engineering** — Tools like **NumPy** and **Apache Arrow** store columns of numbers as tightly-packed arrays. Because all values are the same size and sit next to each other in memory, operations like "multiply every price by 1.05" can be **vectorised** — the CPU processes multiple items at once. This is only possible because of the fixed-layout guarantee arrays provide.

## Common misconceptions

**People think Python's `list` is the same as a fixed array — actually** a Python `list` is a *dynamic array*: it can grow, but occasionally has to copy all its contents to a larger block of memory when it runs out of space. A true fixed-size array (like a **C array** or `numpy.ndarray`) never does this and has no resizing overhead. Both give O(1) index access, but they differ in memory behaviour.

**People think hash maps are always faster than arrays — actually** for access by position, arrays win. Hash maps carry overhead: running a hash function, managing collisions, and storing key-value pairs uses more memory per item. If you are iterating over every item in sequence, arrays are faster because their items sit adjacent in memory (**cache locality** — the CPU can prefetch them before you ask).

**People think hash map lookup is guaranteed O(1) — actually** it is O(1) *on average*. In the pathological worst case — every key hashes to the same index — a naive hash map degrades to O(n). Good hash functions make this astronomically unlikely in normal use, but it can be deliberately triggered in some systems (a vulnerability called a **hash-flooding DoS attack**). Modern languages guard against this, but the guarantee is probabilistic, not absolute.

## How it relates & differs

| Concept | How it relates | Key difference |
|---|---|---|
| [[big-o-time-complexity\|Big-O / Time Complexity]] | Big-O is the *language* used to compare these structures: arrays are O(1) by index / O(n) by value; hash maps are O(1) by key | Big-O measures *speed*; arrays and hash maps are the *structures* being measured |
| [[indexing\|Indexing]] | A database index is inspired by the same insight — avoid scanning everything by navigating directly to the right location | A database index is built *on top of* a stored table on disk; an array or hash map *is* the primary in-memory storage |
| [[tables-keys-sql-basics\|Tables, Keys & SQL Basics]] | A SQL primary-key lookup works like a hash map under the hood: hand the database a key, get a row back fast | SQL tables live on disk inside a database engine with query planning and transactions; hash maps live inside a running program's memory with no such machinery |

## Why you'd use it (and when not to)

Use a **hash map** when your primary access pattern is "find me the thing with this name or ID" — caches, frequency counts, deduplication, and configuration stores are natural fits. Avoid it when memory is very tight (hash maps carry per-entry overhead), when you need items in a reliably sorted order, or when your keys are externally supplied strings that could be crafted to cause collisions.

Use an **array** when you need items in a fixed ordered sequence, when you access them by position, or when you need to crunch through all of them at high speed (numerical computing, columnar data). Avoid it when your main question is "does this key exist?" — that forces a scan.

## Check yourself

**Memory hook:** *"Array = locker number. Hash map = coat-check ticket."*

**Q1: What is the time complexity of retrieving item number 500 from an array of 1,000,000 items?**
O(1). The computer calculates the memory address directly from the index — it does not matter how large the array is.

**Q2: Why is searching an array for a specific value slow?**
The computer has no shortcut and must check items one by one until it finds a match, which is O(n) in the worst case. For a million items that could mean a million comparisons.

**Q3: What does a hash function do, and why does it make hash maps fast?**
A hash function converts a key (like a string) into a number that is used as an index into an internal array. Because the position is *computed* rather than searched for, lookup takes O(1) time on average — the same speed regardless of how many items the map holds.

## Connects to

[[big-o-time-complexity|Big-O / Time Complexity]] · [[indexing|Indexing]] · [[tables-keys-sql-basics|Tables, Keys & SQL Basics]]