---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Processing in Distributed Systems
type: subtopic
tags: [ddia2, s3, object-storage, immutability, buckets, prefix-listing]
sources:
  - raw/ch11.md
---
# Object Stores
> They look like filesystems and they are not. No directories, no atomic renames, no file handles — and objects are immutable once written.

## The Idea
**Object storage services — Amazon S3, Google Cloud Storage, Azure Blob Storage, OpenStack Swift — have become a popular alternative to distributed filesystems for batch jobs.** **In fact the line between the two is somewhat blurry**: **FUSE drivers let users treat object stores as filesystems**, and **some DFS implementations such as JuiceFS and Ceph offer both object storage and filesystem APIs.** **However, their APIs, performance, and consistency guarantees are very different.** **Care must be taken when adopting such systems to make sure they behave as expected, even if they seem to implement the requisite APIs.**

## How It Works
**Each object has a URL** such as `s3://my-photo-bucket/2025/04/01/birthday.png`. **The host portion is the bucket; the rest is the object's key.** **A bucket has a globally unique name, and each object's key must be unique within its bucket.** **Objects are read with a get call and written with a put call.**

**Unlike files on a filesystem, objects are immutable once written.** **To update one it must be fully rewritten with a put, similarly to a key-value store.** **Azure Blob Storage and S3 Express One Zone support appends, but most other stores do not.** **There are no file handle APIs with functions like `fopen` and `fseek`.**

**Objects may look as if they are organized into directories, which is confusing because object stores have no concept of directories.** **The path structure is simply a convention, and the slashes are part of the key.** This lets you do something like a directory listing by **requesting a list of objects with a particular prefix** — **but prefix listing differs from a filesystem directory listing in two ways:**
- **A prefix list behaves like a recursive `ls -R`**: it returns **all objects starting with the prefix, including those in subpaths.**
- **Empty directories are not possible.** Remove all objects under `s3://my-photo-bucket/2025/04/01` and **`01` no longer appears when you list `s3://my-photo-bucket/2025/04`.** **It's common practice to create a zero-byte object to represent an empty directory.**

**DFS implementations often support hard links, symbolic links, file locking, and atomic renames. Such features are missing from object stores.** **Linking and locks are typically unsupported, and renames are nonatomic** — **accomplished by copying the object to the new key and deleting the old one.** **To rename a "directory" you must individually rename every object within it, since the directory name is part of the key.**

## Trade-offs & Pitfalls
- **Key-value stores are optimized for small values (kilobytes) and frequent low-latency reads/writes; distributed filesystems and object stores are generally optimized for large objects (megabytes to gigabytes) and less frequent, larger reads.** **Recently object stores have begun adding support for frequent and smaller reads/writes** — **S3 Express One Zone now offers single-millisecond latency and a pricing model more similar to key-value stores.**
- **Data locality is the other difference.** **DFSs such as HDFS allow computing tasks to run on the machine storing a copy of a file**, letting the task read it without sending it over the network — **saving bandwidth if the task's executable code is smaller than the file.** **Object stores usually keep storage and computation separate.** **This might use more bandwidth, but modern datacenter networks are very fast, so it is often acceptable** — **and it lets CPU and memory be scaled independently of storage since the two are decoupled.**

## Examples & Systems
S3, Google Cloud Storage, Azure Blob Storage, OpenStack Swift; S3 Express One Zone for low-latency access; JuiceFS and Ceph offering both APIs.

## Since the 1st Edition
**Entirely new as a subtopic.** The 1st edition mentioned object storage only in passing as an alternative to HDFS. **The 2nd edition treats it as a co-equal storage layer and — crucially — spells out the ways it is *not* a filesystem**: immutability, no directories, prefix listing semantics, nonatomic renames, no links or locks. **These differences are exactly what breaks batch jobs ported from HDFS to S3**, so the subtopic is practical rather than descriptive.

## Related
- up: [[Batch Processing in Distributed Systems (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Distributed Filesystems (2e)]] — the alternative, and what it offers that this doesn't
- [[Setting Up New Followers (2e)]] — databases backed by object storage
- [[Cloud Data Warehouses (2e)]] — the warehouse stack built on object storage
