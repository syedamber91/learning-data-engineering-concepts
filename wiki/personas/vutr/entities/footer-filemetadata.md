---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/file-formats-for-data-engineers.md
- raw/parquet-file-format/i-spent-8-understanding-how-parquet.md
- raw/parquet-file-format/the-overview-of-parquet-file-format.md
- raw/parquet-file-format/why-parquet-is-the-go-to-format-for.md
- raw/parquet-file-format/its-time-to-replace-parquet.md
- raw/parquet-file-format/why-there-are-so-many-parquets-alternative.md
last_updated: '2026-07-15'
qc: passed
slug: footer-filemetadata
topics:
- parquet
---

Parquet is a self-contained format: everything an application needs to read the file — schema, statistics, encodings — is stored inside it. A magic number (`PAR1`) at the very beginning and very end of the file verifies it's a valid Parquet file. The bulk of the actual metadata, FileMetadata, lives in the footer: number of rows, the data schema, and metadata for every row group. Each row group's metadata in turn carries ColumnMetadata per column chunk — encoding and compression scheme, compressed/uncompressed size, page offsets, and (for measurable types) the min/max value of the chunk — which is exactly what [[predicate-pushdown]] filters against to prune row groups and chunks before reading them.

The footer is also where Parquet's most-cited weakness for wide tables shows up. FileMetadata is encoded with Apache Thrift or Protocol Buffers, and neither format supports random access into the serialized structure. So even if a query only needs the schema for one column, the engine must deserialize the *entire* FileMetadata object to get at it. This is described as a serious problem for feature-store-style tables built for ML training, where thousands of descriptive columns get stitched into one wide row per entity — the bigger the FileMetadata object, the more wasted deserialization work every read pays, no matter how narrow the actual query is.

The three alternative formats each attack this differently. [[lance-file-format|Lance]] gives each column its own protobuf message near the end of the file, addressed through an offset array, so the engine loads metadata only for the columns it actually needs. [[nimble-file-format|Nimble]] and [[vortex-file-format|Vortex]] both replace Thrift with FlatBuffers, which can be read without fully deserializing the surrounding structure — so a query can pull one column's metadata directly rather than paying for the whole object.

*See also: [[predicate-pushdown]] · [[row-group]] · [[column-chunk]] · [[lance-file-format]]*
