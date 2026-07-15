---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/file-formats-for-data-engineers.md
- raw/parquet-file-format/i-spent-8-understanding-how-parquet.md
- raw/parquet-file-format/the-overview-of-parquet-file-format.md
- raw/parquet-file-format/why-parquet-is-the-go-to-format-for.md
- raw/parquet-file-format/its-time-to-replace-parquet.md
last_updated: '2026-07-15'
qc: passed
slug: page
topics:
- parquet
---

A page is Parquet's smallest data unit, and it is the actual unit of encoding *and* compression — not the row group, not the column chunk. There are several page types: data pages hold the real values, dictionary pages hold the dictionary-encoded values built by [[rle-dictionary]], and index pages exist for faster lookup. Every page carries a PageHeader alongside its data, recording the page's row count and its value/definition/repetition encoding; the reader consults this header to know how to decode the page.

Making the page the unit of decompression is precisely what makes Parquet expensive for random access. To read even a single value inside a page, the engine must fetch and decompress the *entire* page, then decode past whatever precedes the target value within it — there's no way to reach into the middle of a compressed page. That single mechanical fact is the physical root of [[parquet-random-access-limitation]]: a query engine can skip whole row groups and column chunks cheaply using footer statistics, but once it has decided a page is relevant, it pays the full page's decode cost regardless of how many of the page's values it actually needs.

*See also: [[row-group]] · [[column-chunk]] · [[parquet-random-access-limitation]] · [[rle-dictionary]]*
