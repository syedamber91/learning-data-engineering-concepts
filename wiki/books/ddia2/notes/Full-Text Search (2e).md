---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
topic: Multidimensional and Full-Text Indexes
type: subtopic
tags: [ddia2, full-text-search, inverted-index, postings-list, lucene, n-gram, edit-distance]
sources:
  - raw/ch04.md
---
# Full-Text Search
> Treat every possible word as a dimension. Then "documents containing red AND apples" is a bitwise AND — the same operation the warehouse query engine was doing two sections ago.

## The Idea
Full-text search lets you search a collection of text documents — web pages, product descriptions — by keywords that might appear anywhere in the text. **Information retrieval is a big specialist topic** that often involves language-specific processing: several Asian languages are written without spaces or punctuation between words, so splitting text into words requires a model of which character sequences constitute a word. It also often involves matching words that are similar but not identical (typos, different grammatical forms) and synonyms. The book declares those problems out of scope.

At its core, though, full-text search is **another kind of multidimensional query**. Each word that might appear in a text (a **term**) is a dimension: a document containing term *x* has value 1 in dimension *x*, and one without has 0. Searching for documents mentioning "red apples" is a query for a 1 in the *red* dimension and simultaneously a 1 in the *apples* dimension. **The number of dimensions may thus be very large.**

## How It Works
- The structure search engines use is an **inverted index**: a key-value structure where the key is a term and the value is the list of IDs of all documents containing it — the **postings list**. If document IDs are sequential numbers, the postings list can also be represented as a **sparse bitmap**, with the nth bit for term *x* set to 1 if document n contains *x*.
- Finding all documents containing both *x* and *y* is then exactly the vectorized warehouse query pattern: **load the two bitmaps and compute their bitwise AND**. Even run-length encoded, this is very efficient.
- **Lucene** — the full-text indexing engine behind Elasticsearch and Solr — works this way. It stores the term→postings-list mapping in **SSTable-like sorted files merged in the background using the same log-structured approach** described earlier in the chapter. PostgreSQL's **GIN** index type also uses postings lists, supporting full-text search and indexing inside JSON documents.
- **n-grams.** Instead of breaking text into words, you can index all substrings of length n. The trigrams (n = 3) of `hello` are `hel`, `ell`, and `llo`. An inverted index of all trigrams lets you search for **arbitrary substrings at least three characters long**, and trigram indexes even allow **regular expressions** in search queries. The downside is that they are quite large.
- **Edit distance.** To cope with typos in documents or queries, Lucene can search for words within a certain **edit distance** (a distance of 1 means one letter added, removed, or replaced). It does this by storing the set of terms as a **finite state automaton** over the characters in the keys, similar to a trie, and transforming it into a **Levenshtein automaton**, which supports efficient search within a given edit distance.

## Trade-offs & Pitfalls
- The n-gram trade is explicit: arbitrary substring and regex search, paid for with a much larger index.
- The framing as a multidimensional query is not a metaphor — it is why the same bitmap machinery works, and it is the connective tissue between the analytics half of the chapter and this one.

## Examples & Systems
Lucene (behind Elasticsearch and Solr), PostgreSQL GIN indexes; Levenshtein automata for fuzzy matching; trigram indexes for substring and regex search.

## Since the 1st Edition
The 1st edition mentioned fuzzy and full-text indexes in a few paragraphs inside [[Other Indexing Structures]], noting Lucene's use of an in-memory finite state automaton and Levenshtein automata. The 2nd edition gives it a proper subtopic and adds: the framing as a multidimensional query, **inverted indexes and postings lists as sparse bitmaps** (explicitly connecting to the columnar bitmap machinery), Lucene's SSTable-like log-structured merging, PostgreSQL GIN, and **n-gram/trigram indexes with regex support**.

## Related
- up: [[Multidimensional and Full-Text Indexes (2e)]] · chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Column-Oriented Storage (2e)]] — where sparse bitmaps and run-length encoding come from
- [[Log-Structured Storage (2e)]] — the merge strategy Lucene reuses
- [[Vector Embeddings (2e)]] — what you reach for when keyword matching isn't enough
- 1st edition: [[Other Indexing Structures]] — where this used to be a few paragraphs
