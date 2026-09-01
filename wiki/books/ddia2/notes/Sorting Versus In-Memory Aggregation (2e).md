---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Processing with Unix Tools
type: subtopic
tags: [ddia2, working-set, mergesort, spilling, coreutils]
sources:
  - raw/ch11.md
---
# Sorting Versus In-Memory Aggregation
> The hash table is faster until your working set exceeds memory. Then the sorting approach wins, because mergesort is happy on disk.

## The Idea
**The Python script keeps an in-memory hash table of URLs to counts. The Unix pipeline has no hash table but instead sorts a list of URLs in which multiple occurrences are simply repeated.** **Which is better? It depends on the number of URLs you have.**

## How It Works
**For most small to mid-sized websites you can probably fit all distinct URLs and a counter for each in, say, 1 GB of memory.** **The working set of the job — the amount of memory to which the job needs random access — depends only on the number of distinct URLs.** **If there are a million log entries for a single URL, the space required is still just one URL plus a counter.** **If the working set is small enough, an in-memory hash table works fine, even on a laptop.**

**If the working set is larger than available memory, the sorting approach has the advantage that it can make efficient use of disks.** **It's the same principle as log-structured storage**: chunks of data are **sorted in memory and written out as segment files**, then **multiple sorted segments are merged into a larger sorted file.** **Mergesort has sequential access patterns that perform well on disks.**

**The `sort` utility in GNU Coreutils automatically handles larger-than-memory datasets by spilling to disk and automatically parallelizes sorting across multiple CPU cores.** **So the simple chain of Unix commands easily scales to large datasets without running out of memory — the bottleneck is likely the rate at which the input file can be read from disk.**

## Trade-offs & Pitfalls
**The limitation of Unix tools is that they run on a single machine.** **Datasets too large to fit in memory or on the local disk present a problem — and that's where distributed batch processing frameworks come in.**

## Examples & Systems
GNU Coreutils `sort` with automatic spilling and parallelisation; mergesort as the underlying algorithm.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Simple Log Analysis]] — the same working-set argument, the same mergesort explanation, and the same Coreutils note. The forward reference now points at the SSD write-pattern discussion in [[Comparing B-Trees and LSM-Trees (2e)]], which the 1st edition did not have as a separate discussion.

## Related
- up: [[Batch Processing with Unix Tools (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Log-Structured Storage (2e)]] — the same sort-and-merge principle
- [[Shuffling Data (2e)]] — the distributed version of this sort
- 1st edition: [[Simple Log Analysis]] — where the 1st edition made the same argument
