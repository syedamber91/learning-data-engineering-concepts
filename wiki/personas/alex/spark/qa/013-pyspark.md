---
persona: alex
kind: concept
sources:
- vutr/pyspark
last_updated: '2026-07-09'
qc: passed
slug: 013-pyspark
topics:
- spark
learner: alex
source_note: pyspark
mastery: mastered
---

*What Alex understood:* Okay let me say it back the way it actually clicked. PySpark is a wrapper — TWO processes, a Python one (my code) and a JVM one (real Spark), and Py4J is the bridge letting Python poke Java objects. For normal DataFrame stuff my Python is just a remote control: it ships instructions over Py4J, the JVM does the work with Catalyst and Tungsten, so it's basically as fast as Scala. The trap is Python UDFs. The JVM can't run Python, so for my custom function it has to serialize each row, ship it to Python, Python deserializes it, runs my code, serializes the answer, ships it back — a full round trip across the boundary. Plus Catalyst treats my UDF as a black box it can't optimize through, and my data balloons from compact Tungsten bytes into fat objects (that 4-byte string -> 48+ bytes point). Three taxes: serialization, lost optimization, object bloat = slow. The fix isn't 'make Python fast,' it's 'stop crossing the boundary so often.' Pandas UDFs (2.3) send a whole BATCH at once via Apache Arrow — a columnar format both sides share so almost no re-serialization — and I process the vector with Pandas/NumPy C code, one crossing per batch instead of per row. Arrow-optimized UDFs (3.5) bolt that Arrow transport onto regular Python UDFs too. And Spark Connect (3.4) swaps the local Py4J glue for a gRPC/protobuf client-server link so a thin client sends the plan to a remote cluster. The mechanism I'm proudest of grasping: the overhead is per-crossing, so vectorization wins by amortizing one fixed boundary cost over many rows.

## Follow-up questions

**Alex:** If plain PySpark DataFrame operations are 'as fast as Scala' because the JVM does everything and Python just sends instructions over Py4J — then in a chain like df.filter(x).groupBy(y).count(), is ANY data actually moving across the Py4J bridge during execution, or is Py4J only used at plan-build time and again to hand back the final small result? I want to know whether the bridge is on the hot path for non-UDF work at all.

**vutr:** Great instinct, and you've spotted the exact reason PySpark can match Scala. The source says the JVM process is where Spark actually runs and Python is 'simply a wrapper' communicating via Py4J. For a filter->groupBy->count chain, Py4J is used at PLAN-BUILD time — each Python call adds a node to the logical plan that lives JVM-side — and then again only to hand back the final small result (a count is one number). The bulk data — the rows being filtered, shuffled, aggregated — never touches the Py4J bridge or the Python process; it stays inside the JVM where Catalyst optimizes the plan and Tungsten manages the memory. So no, the bridge is NOT on the hot path for non-UDF work; that's precisely why there's no per-row Python tax and why it runs like Scala. The bridge only becomes a hot path the moment you introduce a plain Python UDF, because then real row data must cross it. You reasoned that out correctly from the mechanism rather than memorizing it — that's the right level.

**Alex:** Arrow is described as a shared columnar format, and Tungsten is also columnar/off-heap. So when a Pandas UDF runs, is Spark converting Tungsten's format INTO Arrow (still a conversion cost, just cheaper), or are Tungsten and Arrow close enough that it's nearly a zero-copy handoff? Basically — where did the serialization cost actually go, is it eliminated or just shrunk?

**vutr:** Sharp question — this is the crux of vectorized UDFs. The source gives us the pieces: plain Python UDFs suffer 'serialization overhead' and Tungsten uses a compact representation (the '4-byte string -> 48+ bytes in the JVM object' line shows how different in-memory formats and object bloat cost you). Pandas UDFs are 'vectorized' and, per the broader Arrow design the source points to, use Apache Arrow. Here's the honest split: the cost is SHRUNK dramatically, not perfectly zero. Arrow is a columnar format designed so both the JVM side and Python/Pandas side agree on the same memory layout, so the transfer avoids the expensive object-by-object serialize/deserialize that plain UDFs pay — it's close to a bulk columnar copy rather than a per-object translation. But I'll be candid where the source stops: it does NOT claim true zero-copy or that Tungsten's internal format is byte-identical to Arrow, so I won't assert there's literally no conversion. What the source DOES firmly support is the winning mechanism you already named: the boundary crossing is amortized over a whole batch and uses a shared columnar format, so the per-row serialization tax that dominates plain Python UDFs is largely eliminated. So: shrunk to near-negligible via a columnar bulk handoff + batching, with the exact 'zero-copy vs cheap-copy' detail being beyond what this source states.
