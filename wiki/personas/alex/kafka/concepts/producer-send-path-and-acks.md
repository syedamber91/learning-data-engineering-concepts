---
persona: alex
kind: concept
sources:
- vutr/producer-send-path-and-acks
last_updated: '2026-07-10'
qc: passed
slug: producer-send-path-and-acks
topics:
- kafka
learner: alex
source_note: producer-send-path-and-acks
mastery: mastered
---

Okay, let me try to rebuild this. So when I "send" a message, it's like dropping a letter in my *own house's* outbox, not directly into the post office. Inside my house a whole assembly line runs first. I write the letter (the ProducerRecord — it needs at least what I want to say and which mailbox/topic it's going to). Then a translator turns my words into a standard byte-language the network understands (serialize), because you can't mail a thought, you mail written bytes. Then if I didn't say which exact slot it goes in, a sorter (the partitioner) picks the slot based on the key. Then — and this surprised me — the letter doesn't leave right away. It waits in a bin with other letters going to the same place until the bin is full enough or a timer runs out (batch.size and linger.ms). That's on purpose: one fat envelope beats a hundred tiny ones, and it lets the post office (broker) write everything down in one smooth motion instead of lots of little scribbles. And crucially, *I* don't carry the bin to the post office — a different worker thread does that, so I'm free to keep writing more letters. When the post office gets it, it mails me back a receipt saying which mailbox and what position (offset) my letter landed in, or an error. And 'acks' is basically how paranoid I am about the receipt: acks=0 is 'I trust it arrived, don't send a receipt' (fast but I'm blind if it's lost); acks=1 is 'tell me once the main clerk (leader) has it' (but if that clerk drops dead before making copies, my letter's gone); acks=all is 'wait until every backup clerk has a copy too' (safe but slow). DoorDash basically decided being a bit less paranoid — acks=1, fewer copies, don't wait around — was worth 30-40% less CPU.

*Source: [[producer-send-path-and-acks]] (vutr)*
