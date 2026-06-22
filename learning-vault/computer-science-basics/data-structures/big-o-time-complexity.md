---
title: "Big-O / Time Complexity"
area: "Computer Science Basics"
topic: "Data Structures"
tags: [big-o, complexity, performance, scaling]
---

# Big-O / Time Complexity

*Part of [[data-structures-moc|Data Structures]] · [[computer-science-basics-moc|Computer Science Basics]]*

**In one line:** Big-O is a simple label for how much *slower* your code gets as the amount of data grows.

**Picture this:** Finding a friend's name in a phone book. If you flip page by page from the start, doubling the book doubles your work — that's "linear". If you open the middle and keep halving, even a giant book takes only a few steps — that's "logarithmic". Big-O names these patterns.

**How it actually works:** We describe the *shape* of the growth, ignoring exact seconds. `O(1)` means constant — same effort no matter the size (grabbing array item #5). `O(n)` means effort grows in step with the data (checking every item once). `O(n²)` means it explodes — comparing every item to every other item. Small inputs hide the difference; big inputs expose it brutally.

**In the real world:** Google must search billions of web pages in milliseconds. An `O(n)` scan would take minutes, so they use indexes that turn it into something far closer to `O(1)`. Choosing the right complexity is the difference between an app that feels instant and one that times out.

**Why you'd use it (and when not to):** Use Big-O thinking when data could get large, to compare two approaches before coding. Don't obsess over it for tiny, fixed datasets — clarity matters more there.

**Connects to:** [[arrays-hash-maps]] · [[indexing]]
