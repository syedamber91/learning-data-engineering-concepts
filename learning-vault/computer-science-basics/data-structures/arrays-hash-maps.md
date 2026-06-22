---
title: "Arrays & Hash Maps"
area: "Computer Science Basics"
topic: "Data Structures"
tags: [array, hash-map, dictionary, lookup]
---

# Arrays & Hash Maps

*Part of [[data-structures-moc|Data Structures]] · [[computer-science-basics-moc|Computer Science Basics]]*

**In one line:** An array stores items in a numbered row; a hash map stores items by a *name* (key) so you can grab them instantly.

**Picture this:** An array is like lockers in a school hallway — locker #1, #2, #3. If you know the number, you go straight there. A hash map is like a contacts app: you don't remember "the 47th contact", you type "Mum" and her number appears.

**How it actually works:** In an array, items sit in order and you reach any one by its position (index) in a single step. A hash map turns each key (like "Mum") into a position behind the scenes using a *hash function*, so looking up by key is also nearly instant — but the items aren't kept in any tidy order.

**In the real world:** When you log in, a website often uses a hash map to look up your account by username in one quick step, instead of scanning millions of users one by one. Phone contact lists and language dictionaries work the same way.

**Why you'd use it (and when not to):** Use an array when order and position matter (a leaderboard). Use a hash map when you look things up by a key (username → account). Hash maps don't keep order, so they're a poor fit when sequence matters.

**Connects to:** [[big-o-time-complexity]] · [[indexing]]
