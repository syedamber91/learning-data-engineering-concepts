---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
topic: Multidimensional and Full-Text Indexes
type: subtopic
tags: [ddia2, vector-embedding, semantic-search, hnsw, ivf, rag, pgvector]
sources:
  - raw/ch04.md
---
# Vector Embeddings
> "Cancelling your subscription" should be findable by someone searching "how to close my account." No word overlaps. That's the problem embeddings solve.

## The Idea
**Semantic search** goes beyond synonyms and typos to try to understand document concepts and user intentions. It is becoming an important part of AI applications such as **retrieval-augmented generation (RAG)**, which incorporates search results into a large language model's output. The book's example: a help page titled "canceling your subscription" should still be findable by users searching for "how to close my account" or "terminate contract" — close in meaning, completely different words.

To capture meaning, semantic search indexes use **embedding models** to translate a text document into a vector of floating-point values — a **vector embedding**, often produced by LLMs. The vector represents a point in a multidimensional space, each floating-point value giving the document's location along one dimension's axis. Embedding models are trained so that **vectors are near each other when their input documents are semantically similar**.

## How It Works
- A three-dimensional embedding for a Wikipedia page about agriculture might be `[0.38, 0.83, 0.41]`; a page about vegetables would be near it, perhaps `[0.36, 0.64, 0.67]`; a page about star schemas might be `[0.85, 0.10, -0.52]`, comparatively far away. You can tell by inspection that the first two are closer than the third. Real embedding models use **much larger vectors — often over 1,000 numbers** — but the principle is the same. **We don't try to understand what the individual numbers mean**; they are simply the model's way of pointing to a location in an abstract multidimensional space.
- Distance is measured with functions such as **cosine similarity** (the cosine of the angle between two vectors) or **Euclidean distance** (straight-line distance between two points).
- Many early embedding models — **Word2Vec, BERT, GPT** — worked with text and are usually implemented as neural networks. Researchers went on to build models for video, audio, and images, and more recently architectures have become **multimodal**: a single model generating embeddings for several modalities such as text and images.
- At query time the engine feeds the user's query and related context (such as their location) into the embedding model, then must find documents with similar embeddings using a **vector index**. A vector index stores the embeddings of a document collection; you pass in the query's embedding and it returns the documents whose vectors are closest.
- **R-trees don't work well for vectors with many dimensions**, so specialized vector indexes are used:
  - **Flat indexes** store vectors as they are. A query reads every vector and measures its distance to the query vector — **accurate, but slow**.
  - **Inverted file (IVF) indexes** cluster the vector space into partitions (**centroids**) to reduce how many vectors must be compared. Faster than flat, but **only approximate**: query and document may fall into different partitions even when close. A query defines **probes** — the number of partitions to check — and more probes means more accuracy and more comparisons, hence slower.
  - **Hierarchical Navigable Small World (HNSW) indexes** maintain multiple layers of the vector space, each a graph whose nodes are vectors and whose edges represent proximity. A query finds the nearest vector in the topmost, sparsest layer, moves to the same node in the layer below — more densely connected — and follows edges looking for something closer to the query vector, continuing until the last layer. **Also approximate.**

## Trade-offs & Pitfalls
- **Two unrelated meanings of "vector" appear in this chapter**, and the book flags the collision explicitly. In **vectorized processing** a vector is a batch of bits processed by specially optimised code. In **embedding models** a vector is an array of floating-point numbers representing a location in multidimensional space.
- Every practical vector index is **approximate**. Flat indexes are exact and too slow at scale; IVF and HNSW trade recall for speed, and the tuning knob (probes, layer connectivity) is the accuracy/latency dial.

## Examples & Systems
Word2Vec, BERT, GPT as embedding models; Facebook's **Faiss** library with several variations of IVF and HNSW; PostgreSQL's **pgvector**, which supports both.

## Since the 1st Edition
Entirely new, and the most obviously post-2017 material in the chapter — vector databases, embeddings, semantic search, and RAG did not exist as database-engineering topics in the 1st edition. Notably, the book keeps its usual restraint here: it explains the index structures and their approximation trade-offs, states that the full IVF and HNSW algorithms are beyond its scope, and points at the original papers rather than overselling.

## Related
- up: [[Multidimensional and Full-Text Indexes (2e)]] · chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Full-Text Search (2e)]] — keyword search, the thing this goes beyond
- [[Query Execution - Compilation and Vectorization (2e)]] — the other, unrelated "vector"
- [[DataFrames, Matrices, and Arrays (2e)]] — where these floating-point vectors come from
- [[Machine Learning (2e)]] — the batch workload that trains embedding models
