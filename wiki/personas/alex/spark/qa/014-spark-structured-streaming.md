---
persona: alex
kind: concept
sources:
- vutr/spark-structured-streaming
last_updated: '2026-07-09'
qc: passed
slug: 014-spark-structured-streaming
topics:
- spark
learner: alex
source_note: spark-structured-streaming
mastery: mastered
---

*What Alex understood:* Okay here is how I would say it to a friend. A stream is data that never stops. Spark's SQL engine was built to crunch finite tables. Instead of building a whole new engine for endless data, Spark pretends the stream is a bunch of tiny finite tables arriving one after another, and runs its normal table-crunching on each one forever. The clever bit that makes this actually pay off: in Spark a DataFrame isn't the data, it's a lazy plan of what to compute, and that plan gets fed to the Catalyst optimizer. Because the streaming query is written the same way as a batch query, it turns into the same plan, so the same optimizer squeezes it. So Spark gets to reuse ALL its batch optimizations on streams without rewriting them. That's why the 'a stream is just bounded data' idea is a big deal, it's not a philosophy thing, it's engineering reuse.

## Follow-up questions

**Alex:** If the stream is sliced into little bounded chunks and each chunk is run like an independent batch, how does Spark handle a running total, like a live count that has to remember what came before, when each slice is supposedly self-contained?

**vutr:** vutr: Good instinct, and you have spotted the real tension. The source I gave you does not actually spell out the running-total mechanism, so I will be honest about what the material supports versus what it does not. What the source DOES tell you: Structured Streaming reuses the Spark SQL engine and treats the stream as a subset of bounded data. The natural implication is that between slices Spark must carry some state forward so a slice is not truly amnesiac, but the exact machinery for that (the state store, watermarks) is NOT described in the text you were given. So the honest answer is: your slices are not fully self-contained in practice, the engine keeps running state across them, but I cannot ground the details from this source. Flag it as something to verify, do not invent it. That you noticed the abstraction has a hole here is exactly the right depth of thinking.

**Alex:** The source says a DataFrame is a lazy logical plan and nothing runs until an output operation. In batch, the output operation fires once. In streaming, what plays the role of that triggering output operation so the plan actually keeps executing over and over as new data arrives?

**vutr:** vutr: Sharp connection back to the laziness point. The source establishes that no execution happens until a special output operation is called on the plan. Extending that idea logically: in streaming the single one-shot output operation is replaced by something that keeps re-firing the plan as fresh bounded slices arrive, so the same lazy plan executes repeatedly instead of once. That is the conceptual answer the source supports. But the concrete name and configuration of that repeating trigger is NOT stated in the material you have, so I will not hand you a term the text does not contain. Conceptually: yes, an output operation still drives execution, it just fires on a loop instead of once. Mark the specific mechanism as unverified from this source.
