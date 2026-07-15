---
persona: vutr
kind: entity
sources:
- raw/druid-pinot-real-time-olap/a-glimpse-of-apache-pinot-the-real.md
last_updated: '2026-07-15'
qc: passed
slug: star-tree-index
topics:
- apache-pinot-druid-and-real-time-olap
---

The star-tree index is Pinot's answer to iceberg queries — an aggregate function computed over a column (or set of attributes) that then discards aggregate values below a specified threshold. The canonical example: finding which top countries contribute the most page views, without caring about the long tail of every other country. Iceberg cubing extends traditional OLAP cubes to answer this kind of query, and star cubing is a particular advance in iceberg cubing that computes more efficiently than other approaches in most cases, by building a pruned hierarchical structure called a star-tree.

A star-tree's nodes hold pre-aggregated records: each level of the tree contains nodes that satisfy the iceberg condition for a given dimension, plus a "star node" representing all data at that level. Navigating the tree lets a query with multiple predicates get answered without touching raw records. The source's worked example is a two-dimensional split ordered Country, then Browser — each node in the tree holds the aggregated data for its dimension, and a query traverses the tree to reach the answer directly.

LinkedIn implemented the star-tree index for Pinot specifically to speed up internal analytics tools. When a query's shape can be answered by the index, Pinot returns the pre-aggregated result straight from the star-tree; when it can't, execution falls back to running on the original data.

Pinot also supports other index strategies alongside the star-tree: a range index for queries filtering over a range of values, and a bitmap inverted index, which maintains a map from a value to a bitmap of the rows containing it, making value lookups take constant time.

*See also: [[apache-pinot]] · [[pinot-pql]] · [[immutable-segment]] · [[real-time-olap]]*
