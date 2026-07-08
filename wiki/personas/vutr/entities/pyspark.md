---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: pyspark
topics:
- spark
---

PySpark is simply a wrapper: running a PySpark script spawns two separate processes — a Python process and a JVM process — communicating over the Py4J library. Python UDFs pay serialization overhead and get no benefit from Catalyst or Project Tungsten, though Pandas (vectorized) UDFs arrived in Spark 2.3 and Arrow-optimized Python UDFs in Spark 3.5. Spark Connect (Spark 3.4) further decouples the client via gRPC/protobuf.
