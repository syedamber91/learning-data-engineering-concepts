---
persona: alex
kind: concept
sources:
- vutr/pull-based-consumption-and-offset-commit
last_updated: '2026-07-10'
qc: passed
slug: pull-based-consumption-and-offset-commit
topics:
- kafka
learner: alex
source_note: pull-based-consumption-and-offset-commit
mastery: mastered
---

Wait, so the broker is lazy on purpose. It never mails me anything — I show up and ask. It's like a library where the librarian refuses to ship books: I walk in with a bookmark that says "I'm at position 3,041, give me the next chunk," and she just jumps straight to that spot on the shelf and hands me a stack. That's why I can't get flooded — I only ever grab as much as I can carry, and if I fall behind, I just catch up on my own schedule, in batches.

And the weird part is the bookmark math is MY job. The messages don't have name tags — no IDs, because keeping an ID-to-location index would cost extra work. So when I finish a message, I compute my own next bookmark: where this message started plus how long it was. The broker never calculates anything; it just seeks to whatever number I hand it.

Because I always read a partition front-to-back, saying "I'm done through position N" secretly says a lot more — it says I got everything before N too. Like signing for page 500 of a book you can only read in order: nobody needs separate receipts for pages 1 through 499.

And here's the part I'd have gotten backwards: I don't keep my own diary of what I've read. I tell the librarian, and SHE writes it in her own notebook — a special internal topic called __consumer_offsets. That whole handshake is the offset commit. It exists because both dumb alternatives break: if she marks a book "read" the moment she hands it over and I trip on the way home, that book is lost forever. If she instead waits for my thank-you note before marking it, and my note gets lost, other people can pre-grab my book. The knobs are about WHEN I tell her: auto-commit is a timer that reports on a schedule whether or not I actually finished; commitSync stands there until she confirms she wrote it down; commitAsync shouts it over my shoulder and walks off — and if she didn't hear, I'll never know unless I left a callback.

*Source: [[pull-based-consumption-and-offset-commit]] (vutr)*
