---
persona: vutr
kind: concept
sources:
- raw/spark/i-spent-6-hours-learning-pyspark.md
last_updated: '2026-07-11'
qc: passed
slug: pyspark-architecture-and-py4j
topics:
- spark
---

The misconception to correct first: PySpark is not a separate execution engine with a Python-native runtime bolted on. It is a wrapper. When a developer runs a PySpark script, two separate processes spawn — a Python process and a JVM process — and the two talk to each other over the [Py4j](https://www.py4j.org/) library, which lets Python code reach into and drive Java objects living inside a JVM.

Walk the sequence. You write and run a PySpark application; that Python process is the driver process from the user's point of view. When you instantiate `SparkSession`, the `SparkContext` (SC) is created inside that Python process. But creating SC is also the trigger that spawns the *real* Spark driver: Py4j launches a JVM process, and it is this JVM — not the Python process — that actually facilitates data processing. Inside the JVM, a matching `SparkSession`/`SparkContext` pair gets created, configured with the same settings as the Python-side objects.

From there the two processes communicate over Py4j using concrete, named defaults: the Python process listens on port 25334, and the JVM process listens on port 25333. They exchange data through inter-process communication (IPC), which means every payload crossing that boundary must be serialized by the sender and deserialized by the receiver. This IPC channel is what lets the Python side send commands to the JVM and read results back. So when you call something like `.read.load("yellow_tripdata_2024-01.parquet")`, that call doesn't execute in Python at all — it's routed across Py4j to the JVM driver process, which then runs the rest of the Spark application journey (logical plan → physical plan → task scheduling on executors) exactly as a Scala application would. Physical data processing still happens in the Spark JVM executors regardless of which language wrote the application.

The trade-off here is narrow but real: PySpark adds one extra step to the pipeline — spinning up the Py4j JVM driver — plus the serialization/deserialization cost of whatever crosses the IPC boundary. When that payload is a file path string, the overhead is negligible. It stops being negligible the moment you're pushing a large object, such as a Pandas DataFrame, across that boundary — that's where the cost actually bites.

This architecture is also the reason a Python [[python-udf-overhead-and-arrow-optimization|UDF]] is expensive in a way ordinary DataFrame code is not. In the driver-only picture above, execution stays entirely inside the JVM. Register a Python UDF, though, and Spark must spawn *additional* Python processes at the executor level to run that function. For each row, the JVM executor serializes the relevant data and ships it to a Python process via IPC; the Python process deserializes it, runs the user's function, and serializes the result back to the JVM. That round trip — not just the UDF logic itself — is why UDFs are slower than native Spark functions: they also can't benefit from Spark's own optimizations, [[catalyst-optimizer-phases|Catalyst]] and Tungsten, and they process one row at a time rather than in bulk.

Why any of this was worth building: the numbers Vu cites from Databricks show the shift in who actually uses Spark. In 2013, 92% of users wrote Scala, 5% Python, 3% SQL. By 2020 that had flipped — 47% Python, 41% SQL, 12% Scala and other. Python became the dominant Spark interface despite carrying this Py4j/IPC tax, because it's the language data analysts and scientists already know, with libraries like NumPy, Pandas, and Scikit-learn, and it covers the whole pipeline from orchestration (Airflow) to stakeholder-facing apps (Streamlit). Scala being "faster" on paper didn't outweigh accessibility in practice, which is also the throughline into everything the ecosystem subsequently built to shrink that Py4j/IPC tax rather than eliminate the two-process model: Arrow-optimized UDFs, Pandas/vectorized UDFs, and eventually [[spark-connect-architecture|Spark Connect]], which removes the Py4j JVM-driver step altogether by talking to a remote Spark server over gRPC instead.
