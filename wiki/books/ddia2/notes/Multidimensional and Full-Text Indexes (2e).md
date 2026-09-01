---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
type: topic
tags: [ddia2, multidimensional-index, concatenated-index, r-tree, geospatial]
sources:
  - raw/ch04.md
---
# Multidimensional and Full-Text Indexes
B-trees and LSM-trees allow **range queries over a single attribute** — if the key is a username, you can efficiently find all names starting with L. Sometimes searching by a single attribute is not enough.

The most common multi-column index is a **concatenated index**, which combines several fields into one key by appending one column to another, in an order the index definition specifies. It is like an old-fashioned paper phone book, indexing from (lastname, firstname) to phone number: because of the sort order you can find all people with a particular last name, or a particular lastname–firstname combination — but **the index is useless if you want all people with a particular first name**.

**Multidimensional indexes** let you query several columns at once. This is particularly important for geospatial data. A restaurant search website storing each restaurant's latitude and longitude needs, when a user looks at a map, to find all restaurants within the rectangular area being viewed — a two-dimensional range query:

```sql
SELECT * FROM restaurants
 WHERE latitude  >  51.4946 AND latitude  <  51.5079
   AND longitude >  -0.1162 AND longitude <  -0.1004;
```

A concatenated index on latitude and longitude cannot answer this efficiently. It can give you all restaurants in a latitude range (at *any* longitude) or all in a longitude range (anywhere between the poles), **but not both simultaneously**.

## Subtopics
- [[Full-Text Search (2e)]] — inverted indexes, postings lists, n-grams, and edit distance.
- [[Vector Embeddings (2e)]] — semantic search, and the index families that make it fast.

## Key Takeaways
- One option is to **translate a two-dimensional location into a single number via a space-filling curve**, then use a regular B-tree index.
- More commonly, **specialized spatial indexes** are used — **R-trees** or **Bkd-trees** — which divide up the space so nearby data points tend to be grouped in the same subtree. **PostGIS** implements geospatial indexes as R-trees using PostgreSQL's Generalized Search Tree indexing facility. It is also possible to use **regularly spaced grids of triangles, squares, or hexagons**.
- **These are not just for geography.** On an ecommerce site, a three-dimensional index on (red, green, blue) searches for products in a colour range. In a weather-observation database, a two-dimensional index on (date, temperature) efficiently finds all observations in a given year where the temperature was between 25°C and 30°C. With a one-dimensional index you would have to scan all records from that year and filter by temperature, or vice versa; **a two-dimensional index narrows by both simultaneously**.
- Full-text search is framed here as **another kind of multidimensional query** — one where every possible term is a dimension — which is why it lives under this topic rather than on its own.

## Since the 1st Edition
Promoted from a short passage inside the 1st edition's [[Other Indexing Structures]] to a full topic with two substantial subtopics. The 1st edition mentioned multi-column and geospatial indexes and fuzzy/full-text search briefly; the 2nd edition adds Bkd-trees, the hexagonal/triangular grid option, PostGIS's GiST-based implementation, and the non-geographic examples — and then devotes real space to full-text search and vector embeddings, which is where the genuinely new material lies.

## Related
- chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Multicolumn and Secondary Indexes (2e)]] — the single-key indexes this extends
- [[Column-Oriented Storage (2e)]] — bitmaps as a different answer to multi-condition queries
- 1st edition: [[Other Indexing Structures]] — where this used to be a paragraph
