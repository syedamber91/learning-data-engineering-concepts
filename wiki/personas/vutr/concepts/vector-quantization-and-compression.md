---
persona: vutr
kind: concept
sources:
- raw/llms-ai-agents-and-vector-databases-additional/i-spent-8-hours-learning-about-vector.md
last_updated: '2026-07-15'
qc: passed
slug: vector-quantization-and-compression
topics:
- llms-ai-agents-and-vector-databases
---

Retrieving [[vector-embedding|vector embeddings]] efficiently needs [[approximate-nearest-neighbor-search|an ANN index]], but storing them efficiently is a separate problem, with its own worked numeric example: an 11-byte piece of text ("the red fox," one byte per ASCII character in UTF-8) fed through an embedding model can produce a 1536-dimensional output vector. At the standard 4 bytes per dimension (32-bit floating point, FP32), that single vector costs about 6KB to store — a greater-than-500x blow-up (6,000 bytes versus 11). Scaled to 1 billion vectors at 6KB each, that's 6TB of disk just for the embeddings, before any of the rest of the system.

Vector Quantization (VQ) is named as the core compression technique vector databases use to attack this. Instead of spending a full 32 bits per dimension, VQ represents each number with fewer bits (8 bits is the example given) — some quantization techniques additionally reduce the number of dimensions outright. Product Quantization is named as a popular way to implement VQ (see [[product-quantization]] for the sub-vector/codebook mechanism itself). The trade being made across all of this is the same one that runs through vector database design generally: accept an approximate, lossy representation of the vector in exchange for keeping storage and search costs from growing linearly (or worse) with the number of embeddings a system needs to hold.

*See also: [[product-quantization]] · [[vector-embedding]] · [[approximate-nearest-neighbor-search]]*
