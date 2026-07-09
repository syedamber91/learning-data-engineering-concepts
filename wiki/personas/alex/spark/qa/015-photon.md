---
persona: alex
kind: concept
sources:
- vutr/photon
last_updated: '2026-07-09'
qc: passed
slug: 015-photon
topics:
- spark
learner: alex
source_note: photon
mastery: learning
---

*What Alex understood:* So Photon is a fast C++ engine bolted onto Databricks that reads data column-by-column and chews through it in batches instead of one row at a time — same batch idea as BigQuery and Snowflake. And the team chose the simpler 'interpreted/vectorized' way over auto-generating code because it was quicker to build and easier to debug, and the cost of jumping between Java and C++ turned out to be almost zero (0.06%).

## Follow-up questions

**Alex:** Why did processing data in batches (vectorized) make debugging so much easier than the code-generation approach?

**vutr:** The note ties the easy debugging to the choice of vectorized (interpreted) execution over code generation: with the interpreted C++ approach you can print-debug native C++ code directly, while debugging runtime-generated code was far harder. So the batching approach came bundled with plain C++ you could inspect, instead of code the program writes on the fly that you can't easily read. (The note credits the vectorized/interpreted choice for the easier debugging; it doesn't spell out the low-level mechanics of why batching itself helps.)

**Alex:** What actually is the 'JNI overhead,' and why were people worried about it before finding out it was only 0.06%?

**vutr:** The note says JNI overhead 'came out at just 0.06% of execution time' — JNI is the boundary Databricks crosses to run native C++ from the Java-based Spark world, and the worry (implied) was that crossing that boundary would be expensive. It turned out to cost only 0.06%, so it wasn't a real problem. The note doesn't fully define JNI or explain the mechanism, so the 'why people worried' part is my inference.
