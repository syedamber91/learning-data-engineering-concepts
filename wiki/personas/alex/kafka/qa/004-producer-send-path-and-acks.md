---
persona: alex
kind: concept
sources:
- vutr/producer-send-path-and-acks
last_updated: '2026-07-10'
qc: passed
slug: 004-producer-send-path-and-acks
topics:
- kafka
learner: alex
source_note: producer-send-path-and-acks
mastery: mastered
---

*What Alex understood:* Okay, let me try to rebuild this. So when I "send" a message, it's like dropping a letter in my *own house's* outbox, not directly into the post office. Inside my house a whole assembly line runs first. I write the letter (the ProducerRecord — it needs at least what I want to say and which mailbox/topic it's going to). Then a translator turns my words into a standard byte-language the network understands (serialize), because you can't mail a thought, you mail written bytes. Then if I didn't say which exact slot it goes in, a sorter (the partitioner) picks the slot based on the key. Then — and this surprised me — the letter doesn't leave right away. It waits in a bin with other letters going to the same place until the bin is full enough or a timer runs out (batch.size and linger.ms). That's on purpose: one fat envelope beats a hundred tiny ones, and it lets the post office (broker) write everything down in one smooth motion instead of lots of little scribbles. And crucially, *I* don't carry the bin to the post office — a different worker thread does that, so I'm free to keep writing more letters. When the post office gets it, it mails me back a receipt saying which mailbox and what position (offset) my letter landed in, or an error. And 'acks' is basically how paranoid I am about the receipt: acks=0 is 'I trust it arrived, don't send a receipt' (fast but I'm blind if it's lost); acks=1 is 'tell me once the main clerk (leader) has it' (but if that clerk drops dead before making copies, my letter's gone); acks=all is 'wait until every backup clerk has a copy too' (safe but slow). DoorDash basically decided being a bit less paranoid — acks=1, fewer copies, don't wait around — was worth 30-40% less CPU.

## Follow-up questions

**Alex:** With acks=1, the message can be lost if the leader crashes before replicating — but the producer already got its success ack. So doesn't that mean the producer thinks the message was delivered when it's actually gone? How is that different from the silent loss in acks=0, other than acks=0 not waiting at all?

**vutr:** Good catch — you've found the real seam. With acks=1 the producer does get its success ack the moment the leader has the message, so yes, if the leader then crashes before replicating to its followers, the producer already believes the write succeeded and the message is lost — a false-positive success. The difference from acks=0 is *where* the blindness lives. With acks=0 the producer never waits for any reply at all and simply assumes success, so it's blind to *every* failure, including the broker never receiving the message. With acks=1 the producer does wait, and it will catch the common failure — if the leader can't take the write, it gets an error and can retry, which reduces loss risk. The narrow window that acks=1 can't protect against is the leader accepting the write and then crashing before replicating. acks=all is what closes that window, because success only counts once all replicas have the message, so it survives a broker crash — at the cost of higher latency from waiting on every replica-holding broker.

**Alex:** The batching thread waits until batch.size fills OR linger.ms runs out before sending. But if I send synchronously and wait for the response on every single message, how does batching even help — aren't I forced to wait through the linger delay every time, making it slower rather than faster?

**vutr:** You've spotted exactly why synchronous send is rare in production. The note is explicit that waiting on every message hurts performance, which is the trade-off you're describing — and batching's whole point is the opposite: accumulate records in memory and send larger batches in a single request to avoid too many small requests. Async send fits that model naturally: you send everything without waiting, which takes almost no time, and attach a callback for errors, so the batching thread is free to fill and flush batches on its own schedule. Synchronous send, where you wait for the response on every message, works against that grain — which is why the note calls it rare in production.
