---
persona: vutr
kind: entity
sources:
- raw/llms-ai-agents-and-vector-databases-additional/i-spent-8-hours-learning-about-vector.md
last_updated: '2026-07-15'
qc: passed
slug: hnsw
topics:
- llms-ai-agents-and-vector-databases
---

HNSW (Hierarchical Navigable Small World) is described as the most common implementation of the graph-based approach to [[approximate-nearest-neighbor-search|approximate nearest neighbor search]]: a way to find close vectors without comparing the query against every stored vector one by one.

The graph-based idea in general is to treat every stored vector as a node and draw an edge between a node and its closest neighbors; a search then "walks" the graph — start at an entry point, greedily jump to whichever neighbor is closest to the query vector, and keep going until no closer neighbor can be found, rather than scanning the whole vector set. HNSW builds this as *multiple layers* of such graphs, compared to a highway system: the top layer is sparse, with only a few nodes and long-distance links; the bottom layer is dense and connects every vector. A search starts at the top-most, sparsest layer and quickly narrows to the approximate region of the query; once it finds the best point in that layer, it "drops down" to the next layer using that point as its new starting position, refines the search on the denser graph below, and repeats the drop until it reaches the bottom layer and returns the nearest vectors.

Because ANN methods pre-calculate distances and organize close vectors together (via graphs like HNSW, or via the [[approximate-nearest-neighbor-search|spatial-partitioning]] alternative), the search space that must actually be scanned shrinks — at the cost of the result being only approximately the true nearest neighbors, not guaranteed exact matches the way a brute-force scan would be.

*See also: [[approximate-nearest-neighbor-search]] · [[vector-embedding]] · [[vector-quantization-and-compression]]*
