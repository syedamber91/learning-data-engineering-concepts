---
persona: vutr
kind: entity
sources:
- raw/llms-ai-agents-and-vector-databases-additional/i-spent-8-hours-learning-about-vector.md
last_updated: '2026-07-15'
qc: passed
slug: product-quantization
topics:
- llms-ai-agents-and-vector-databases
---

Product Quantization (PQ) is named as a popular method for implementing Vector Quantization, the core compression technique vector databases use to tame the storage blow-up of [[vector-embedding|embeddings]] (see [[vector-quantization-and-compression]]). Where plain vector quantization just says "use fewer bits per dimension" (e.g., 8 bits instead of the 32 bits of an FP32 float), PQ describes a specific mechanism for getting there.

The process: take a large vector — the running example is 1536 dimensions — and chop it into a fixed number of smaller, independent sub-vectors (the example splits it into 32 sub-vectors of 48 dimensions each). Next, run a clustering algorithm (k-means is named) over the sub-vectors to produce a fixed number of centroids; the centroids collectively form a codebook. Each sub-vector is then assigned to whichever centroid in the codebook it is closest to, and is represented from then on not by its raw 48 numbers but by the index of that centroid. The full vector becomes a concatenated sequence of these small centroid-index codes rather than a long list of 32-bit floats — which is where the space savings comes from: you are storing a handful of small integers per vector instead of a stream of full-precision numbers, at the cost of only approximating each sub-vector's original value.

*See also: [[vector-quantization-and-compression]] · [[vector-embedding]] · [[approximate-nearest-neighbor-search]]*
