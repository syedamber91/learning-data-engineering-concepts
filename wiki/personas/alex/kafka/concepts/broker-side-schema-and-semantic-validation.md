---
persona: alex
kind: concept
sources:
- vutr/broker-side-schema-and-semantic-validation
last_updated: '2026-07-10'
qc: passed
slug: broker-side-schema-and-semantic-validation
topics:
- kafka
learner: alex
source_note: broker-side-schema-and-semantic-validation
mastery: mastered
---

Okay, let me try to rebuild this. Kafka's broker is basically a super-fast mail sorter that never opens the envelopes — it just sees bytes, 0s and 1s, on purpose, because opening envelopes would slow it down. That's the same reason it does batching and zero-copy: do less, go fast. So the broker literally *can't* be the bouncer that checks your data, because a bouncer has to look inside and it never does.

So they moved the checking to the clients using the Confluent Schema Registry. The producer is like someone who registers a form template with a central office, gets a template ID number, stamps that ID onto the front of the message, and ships it. The consumer reads the ID stamp, calls the same office to get the matching template, and uses it to unpack the bytes. The message layout is: 1 magic byte, then 4 bytes for the schema ID, then the real data from byte 5 on.

But here's the catch that clicked for me: this is all voluntary. "If data governance is opt-in, it's not data governance." Anyone can skip the check, turn off the compatibility rule, or auto-register some new schema, and nobody stops them. Even worse, the registry can *approve* a change that still breaks everything — like renaming a Protobuf field, because Protobuf tracks fields by tag number so the rename looks safe, but a consumer reading it as JSON keys on the name and blows up.

So Bufstream flips it: put the bouncer back at the door — the broker itself checks each message against the schema and rejects bad ones. It costs more CPU and a little latency because now the broker has to actually understand messages, but clients stop carrying validation code. And you can't sneak new schemas in at runtime anymore — changes go through git and CI with `buf breaking`. Plus there are three depths of checking: is the ID real, is the payload a valid encoding, and does it make *sense* (age can't be 1000 even though 1000 fits in a uint32) — that last one done with CEL rules the broker enforces.

*Source: [[broker-side-schema-and-semantic-validation]] (vutr)*
