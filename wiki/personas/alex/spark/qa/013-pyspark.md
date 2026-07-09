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
mastery: familiar
---

*What Alex understood:* Alex: Let me try to say it back. PySpark isn't really Python doing the work, it's a wrapper. When I run it, two programs start up together, a Python one and a JVM (Java) one, and they chat through Py4J. If I write my own function in Python (a UDF), it's slow because the data has to be packed up and shipped between the two, that's serialization, and it doesn't get the Catalyst or Tungsten speed boosts. But they added faster versions: Pandas/vectorized UDFs in 2.3 and Arrow-optimized ones in 3.5, plus Spark Connect in 3.4 that splits the client off using gRPC/protobuf.

## Follow-up questions

**Alex:** vutr: Why is a plain Python UDF slower than just using Spark's built-in operations?

**vutr:** Alex: Because a Python UDF makes Spark pay serialization overhead, packing and shipping the data between the Python process and the JVM process, and it gets no benefit from Catalyst or Project Tungsten, Spark's optimization engines.

**Alex:** vutr: What are the two separate processes that start when you run a PySpark script, and what connects them?

**vutr:** Alex: A Python process and a JVM process, and they communicate over the Py4J library.
