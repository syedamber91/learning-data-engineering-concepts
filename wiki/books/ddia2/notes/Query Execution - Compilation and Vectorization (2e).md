---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
topic: Data Storage for Analytics
type: subtopic
tags: [ddia2, query-compilation, vectorization, simd, llvm, operators]
sources:
  - raw/ch04.md
---
# Query Execution: Compilation and Vectorization
> Scanning millions of rows means CPU time matters as much as disk time. A naive row-at-a-time interpreter is too slow, and there are exactly two escapes.

## The Idea
A complex analytical SQL query is broken into a **query plan** of stages called **operators**, which may be distributed across machines for parallel execution. Query planners optimise a lot by choosing which operators to use, in which order, and where to run each one.

Within an operator, the engine does things with column values: finding all rows whose value is among a particular set (perhaps as part of a join), or checking whether a value exceeds 15. It will likely also need to look at several columns for the same row — all sales where the product is "bananas" and the store is a particular one.

For queries scanning millions of rows, we must worry not only about bytes read off disk but about **CPU time spent executing complex operators**. The simplest operator is like an **interpreter**: while iterating over each row it consults a data structure representing the query to find which comparisons or calculations to perform on which columns. That is **too slow for many analytics purposes**. Two alternatives have emerged.

## How It Works
- **Query compilation.** The engine takes the SQL query and **generates code** to execute it. The code iterates over rows one by one, looks at the values in the columns of interest, performs the needed comparisons or calculations, and copies values to an output buffer when conditions are satisfied. The generated code is then **compiled to machine code — often with an existing compiler such as LLVM** — and run against the column-encoded data loaded into memory. This is similar to the **just-in-time (JIT)** compilation used by the JVM and similar runtimes.
- **Vectorized processing.** The query is **interpreted, not compiled**, but made fast by **processing many values from a column in a batch** instead of iterating row by row. A fixed set of predefined operators is built into the database; you pass arguments and get back a batch of results. Pass the `product_sk` column and the ID for "bananas" to an equality operator and get back a bitmap (one bit per input value, 1 where it matches). Pass `store_sk` and the store of interest to the same operator for a second bitmap. Pass both bitmaps to a **bitwise AND** operator, and the result is a bitmap with a 1 for every sale of bananas in that store.

The two are very different in implementation, but **both are used in practice**, and both achieve very good performance by exploiting the characteristics of modern CPUs:
- Preferring **sequential memory access** over random access, to reduce cache misses.
- Doing most of the work in **tight inner loops** — few instructions, no function calls — to keep the instruction pipeline busy and avoid branch mispredictions.
- Using **parallelism**: multiple threads and **SIMD** (single instruction, multiple data) instructions.
- **Operating directly on compressed data** without decoding it into a separate in-memory representation, saving memory allocation and copying costs.

## Trade-offs & Pitfalls
- The bitwise-AND example is exactly the bitmap encoding from [[Column-Oriented Storage (2e)]] paying off at execution time; **the storage format and the execution strategy are co-designed**, not independent choices.
- Compilation adds a code-generation and compilation step per query, which is wasted on short queries; vectorization avoids that but is limited to the predefined operator set. The book declines to declare a winner.

## Examples & Systems
LLVM as the compiler back end for query compilation; SIMD instructions; the equality-operator-then-bitwise-AND pipeline as the worked vectorization example.

## Since the 1st Edition
Entirely new as a subtopic. The 1st edition mentioned vectorized processing in a paragraph inside [[Column Compression]] and did not cover query compilation, JIT, SIMD, or the CPU-characteristics argument at all. Its promotion here reflects that for analytics engines, **CPU efficiency became as central a design axis as I/O efficiency**.

## Related
- up: [[Data Storage for Analytics (2e)]] · chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Column-Oriented Storage (2e)]] — the bitmaps this operates on
- [[Vector Embeddings (2e)]] — a different, unrelated meaning of "vector" in the same chapter
- [[Cloud Data Warehouses (2e)]] — where query engines became separable components
