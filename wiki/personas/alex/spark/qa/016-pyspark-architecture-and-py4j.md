---
persona: alex
kind: concept
sources:
- vutr/pyspark-architecture-and-py4j
last_updated: '2026-07-10'
qc: passed
slug: 016-pyspark-architecture-and-py4j
topics:
- spark
learner: alex
source_note: pyspark-architecture-and-py4j
mastery: mastered
---

*What Alex understood:* Okay wait, so... it's basically like I'm not actually driving the car -- I'm sitting in the passenger seat texting instructions to a driver in another car, and that driver is the one who actually knows how to drive and has the engine. My Python process is just the messenger. The moment I do SparkSession(), that's like sending a text that says "start the car," and that starts up a WHOLE separate JVM car with its own engine, which is the one that actually does the driving -- plans the route, drives it, everything. My Python side just sits there listening on its little walkie-talkie channel (port 25334) while the JVM listens on its own channel (25333), and every message between us has to get translated (serialized) into a form the other side understands and then translated back (deserialized) -- like we're speaking through an interpreter every single time.

So when I call `.read.load(...)`, I'm not doing anything myself -- I'm just texting "hey, load this file" over to the JVM driver, and it does the actual reading, planning, and scheduling across all the executor workers, same as if I'd written the whole thing in Scala.

And that's why UDFs are the expensive part -- it's not that my function is slow, it's that for every SINGLE ROW, the JVM executor has to stop, translate the row into a message, send it over to yet another Python process, wait for that process to translate it back, run my function, translate the answer, and send it back. Imagine doing that interpreter hand-off for every row in a million-row table instead of just handling the whole table in one bulk operation -- that's the real cost, not my code.

## Follow-up questions

**Alex:** Wait -- if every Python UDF call has to pay the row-by-row serialize-deserialize IPC tax, why doesn't a normal operation like .filter() or .groupBy() pay that same tax, since I wrote that in Python too?

**vutr:** Because normal DataFrame operations like .filter() or .groupBy() never leave the JVM once they've been kicked off. Your Python driver call is just the instruction that gets shipped once, across Py4j, to the JVM driver -- after that, the entire logical plan to physical plan to task scheduling to execution runs entirely inside the JVM and its executors, exactly as it would for a Scala job. There's no row-by-row hop back to Python. A UDF is different because Spark has to spawn additional Python processes AT THE EXECUTOR level specifically to run your function, and that forces a serialize-ship-deserialize round trip for every row. The tax only shows up where Python code has to run on a per-row basis at the executor level -- and ordinary DataFrame code never does that.

**Alex:** You said Spark Connect removes the Py4j JVM-driver step by talking to a remote server over gRPC instead -- does that mean UDFs stop paying the serialization tax under Spark Connect, or does gRPC just move where that same cost happens?

**vutr:** (the wiki does not cover this — see open questions)
