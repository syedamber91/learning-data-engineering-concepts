---
persona: vutr
kind: concept
sources:
- raw/llms-ai-agents-and-vector-databases-additional/i-spent-8-hours-learning-about-vector.md
last_updated: '2026-07-15'
qc: passed
slug: approximate-nearest-neighbor-search
topics:
- llms-ai-agents-and-vector-databases
---

The most straightforward way to find vectors similar to a query is brute force: compare the input vector to every stored vector one by one using a distance metric such as Euclidean distance, and return the closest matches. This works, and is genuinely implemented in vector databases — but it's an O(n) algorithm in the number of stored vectors, so at a scale of 10 million vectors it slows down enough to be impractical for interactive workloads.

The fix vector databases converge on is an index built around approximate nearest neighbor (ANN) search — explicitly not the same kind of index as an OLTP point-lookup index (like a B-Tree) or an OLAP min-max index. The shared core idea across ANN approaches is to pre-calculate distances between vectors so that ones which are close together can be organized for cheap retrieval, and then let a search skip over vectors that are far from the query, shrinking the space that must actually be scanned — in exchange for results that are only approximately correct rather than the guaranteed exact matches brute force provides.

Two approaches are named as the most common:

**Graph-based** methods build a graph where each vector is a node and edges connect a node to its closest neighbors; a search "walks" the graph greedily from an entry point toward whichever neighbor is closest to the query, stopping once no closer neighbor exists rather than checking every vector. [[hnsw|HNSW]] is named as the most common graph-based implementation, layering multiple such graphs from sparse (top) to dense (bottom) so a search narrows region-by-region before it reaches the fully connected bottom layer.

**Spatial partitioning** instead divides the vector space into partitions, each represented by a point (typically the centroid of the vectors it contains, drawing on the same distance-and-clustering machinery as [[product-quantization|Product Quantization's]] codebook approach). A query first finds the closest representative centroid, then loads only the partition(s) associated with it to search for matches, rather than touching the whole dataset.

Putting ANN in context of a full request: after raw data is embedded and stored (and used to build or adjust the ANN index), a new query is itself embedded into a vector, parsed and validated the way a traditional database query would be, planned by an optimizer, and only then matched against the indexed vectors — with post-processing (such as ranking candidates by similarity to the query) applied to the retrieved set before it's returned. ANN indexing is the step in that lifecycle that makes the retrieval half of a vector database's workload tractable at scale, the same way [[vector-quantization-and-compression|quantization]] makes the storage half tractable.

*See also: [[hnsw]] · [[product-quantization]] · [[vector-quantization-and-compression]] · [[vector-embedding]] · [[vector-database-storage-row-vs-column]]*
