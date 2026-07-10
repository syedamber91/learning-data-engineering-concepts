---
persona: alex
kind: concept
sources:
- vutr/pull-based-consumption-and-offset-commit
last_updated: '2026-07-10'
qc: passed
slug: 006-pull-based-consumption-and-offset-commit
topics:
- kafka
learner: alex
source_note: pull-based-consumption-and-offset-commit
mastery: mastered
---

*What Alex understood:* Wait, so the broker is lazy on purpose. It never mails me anything — I show up and ask. It's like a library where the librarian refuses to ship books: I walk in with a bookmark that says "I'm at position 3,041, give me the next chunk," and she just jumps straight to that spot on the shelf and hands me a stack. That's why I can't get flooded — I only ever grab as much as I can carry, and if I fall behind, I just catch up on my own schedule, in batches.

And the weird part is the bookmark math is MY job. The messages don't have name tags — no IDs, because keeping an ID-to-location index would cost extra work. So when I finish a message, I compute my own next bookmark: where this message started plus how long it was. The broker never calculates anything; it just seeks to whatever number I hand it.

Because I always read a partition front-to-back, saying "I'm done through position N" secretly says a lot more — it says I got everything before N too. Like signing for page 500 of a book you can only read in order: nobody needs separate receipts for pages 1 through 499.

And here's the part I'd have gotten backwards: I don't keep my own diary of what I've read. I tell the librarian, and SHE writes it in her own notebook — a special internal topic called __consumer_offsets. That whole handshake is the offset commit. It exists because both dumb alternatives break: if she marks a book "read" the moment she hands it over and I trip on the way home, that book is lost forever. If she instead waits for my thank-you note before marking it, and my note gets lost, other people can pre-grab my book. The knobs are about WHEN I tell her: auto-commit is a timer that reports on a schedule whether or not I actually finished; commitSync stands there until she confirms she wrote it down; commitAsync shouts it over my shoulder and walks off — and if she didn't hear, I'll never know unless I left a callback.

## Follow-up questions

**Alex:** With auto-commit on a timer, couldn't the commit fire after I've pulled a batch but before my code actually finished processing it — so the broker's notebook says I'm done with messages I never really processed? Is that timing loophole the whole reason manual commit exists?

**vutr:** You've put your finger on exactly the trade-off the note names. Automatic commit means the consumer commits offsets at regular intervals — the note's verdict is 'least effort, least control over WHEN a commit lands.' A timer doesn't know or care where your processing is; it just fires. And remember what a commit MEANS: the broker assumes all messages before the committed point are processed. So yes — the entire point of manual commit (enable.auto.commit=false) is to close that timing loophole by letting the consumer decide when commits occur, so the commit can land at the moment of the consumer's choosing rather than the timer's. Then you pick your poison on the second axis: commitSync() waits until the commit succeeds or errors, while commitAsync() doesn't wait — faster, but a failed commit vanishes silently unless you wire up the error callback. The note doesn't walk through your specific crash-and-restart sequence step by step, but the control trade-off you spotted is precisely the one it describes.

**Alex:** You said the 'wait for confirmation' design fails because other instances can pre-consume a message when the ack goes missing. But Kafka's offset commit IS a confirmation the broker waits to record — so why doesn't the exact same pre-consume problem break Kafka's version?

**vutr:** Sharp question, and the difference is structural, not cosmetic. In the naive design, the broker's 'consumed' marking is a gate on delivery — the broker is deciding what to hand out based on what's been confirmed, so a missing ack leaves the message up for grabs by other instances. In Kafka, delivery never passes through that gate at all: every pull request itself carries the offset where consumption should begin, and the broker just seeks to that position and returns data. The commit isn't a gate — it's bookkeeping, a recorded position in __consumer_offsets. And your 'other instances' worry is handled by a different mechanism entirely: scaling reads across a topic is the job of consumer groups, where each partition is owned by exactly ONE consumer in the group — so there's no crowd of instances racing to pre-consume the same partition. The committed offset's job is the handoff: when membership changes and partition ownership moves, the committed offset is what lets the NEW owner resume where the old one stopped.
