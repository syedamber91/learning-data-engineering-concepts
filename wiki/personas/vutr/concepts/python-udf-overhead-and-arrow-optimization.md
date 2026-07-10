---
persona: vutr
kind: concept
sources:
- raw/spark/i-spent-6-hours-learning-pyspark.md
last_updated: '2026-07-11'
qc: passed
slug: python-udf-overhead-and-arrow-optimization
topics:
- spark
---

The mistake people make is assuming a Python UDF just "runs in Python" the way a normal Python function does. It doesn't — it runs across a process boundary that isn't there for native Spark code, and that boundary is where the cost comes from.

Start from the baseline PySpark setup covered in [[pyspark-architecture-and-py4j]]: a PySpark script spawns two processes, a Python process and a JVM process, wired together by Py4j — the Python side listens on a default port of 25334, the JVM side on 25333, and the two talk over IPC. When your PySpark code is just calling built-in operations like `.read.load(...)`, the call gets routed straight to the JVM driver, and the only thing crossing that IPC channel is small stuff like a file path string. The serialization/deserialization tax on that is trivial. It only starts to matter once you're pushing something heavier across, like a Pandas DataFrame.

A Python UDF changes the shape of execution entirely. Without a UDF, physical data processing stays inside the Spark JVM executors end to end. With one, Spark can't run your custom Python function inside the JVM, so it spins up additional Python processes on the executor side specifically to run it. The mechanism, step by step: the JVM executor serializes the relevant data and sends it over IPC to a Python process; the Python process also receives the function definition itself from the driver; it deserializes the data, executes the function, then serializes the result and ships it back to the JVM. That's a full serialize → cross-process transfer → deserialize round trip, twice (once for the input, once for the result), for every batch of data the UDF touches — and it scales with how much data has to move, not with how complex your function is.

That round trip is one of two separate performance hits, and it's worth keeping them distinct because the source is explicit that Python UDFs are slower for two independent reasons. First, the serialize/deserialize overhead itself. Second — and this one has nothing to do with crossing processes — a Python UDF can't benefit from Spark's own optimizations: not [[catalyst-optimizer-phases]] (the Spark SQL optimizer), and not [[tungsten-and-jvm-object-overhead]] (the project that gets performance by operating on binary data directly instead of Java objects). On top of that, a plain Python UDF processes one row at a time, which is the slowest access pattern Spark has.

Arrow-optimized Python UDFs, added in Spark 3.5, attack the first problem — the transfer cost — not the row-at-a-time problem. The fix is that both the JVM and the Python process represent the data in Apache Arrow format instead of Pickle, and Arrow's format is what lets them skip the costly serialize/deserialize step rather than just making it faster. It's opt-in, not a default. The secondary win the source calls out: because Arrow lays data out in columnar form rather than the row-wise layout Pickle uses, processing itself is faster on top of avoiding the (de)serialization cost.

Pandas UDFs (Vectorized UDFs), which actually predate this — introduced in Spark 2.3 — solve the row-at-a-time problem instead. They still require a separate Python process; the difference is that Pandas does the computation and, because Arrow handles the data exchange, the serialize/deserialize step is skipped there too. The combination — Arrow's columnar layout plus Pandas doing the actual computation — is what lets execution happen in a vectorized batch manner rather than row by row, which is the real reason Pandas UDFs outperform plain Python UDFs, not just the Arrow transfer savings alone.

Read together: plain Python UDF pays both the IPC serialization tax and the no-Catalyst/no-Tungsten/row-at-a-time tax. Arrow-optimized Python UDF removes the serialization tax but is still row-at-a-time. Pandas UDF, via Arrow, removes both.
