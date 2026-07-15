---
title: "Lesson learned after reading the BigQuery academic paper: Shuffle operation"
channel: vutr
author: "Vu Trinh"
published: 2024-01-06
url: https://vutr.substack.com/p/bigquery-processing-engine-shuffle
paid: false
topics: ["Data Engineering", "Apache Spark", "BigQuery"]
tags: [shuffle, https, dremel, google, worker, bigquery]
---

# Lesson learned after reading the BigQuery academic paper: Shuffle operation

*You don't know this.*

> Source: [Open post](https://vutr.substack.com/p/bigquery-processing-engine-shuffle)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[bigquery|BigQuery]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

> *TL;DR:*
>
> * *Dremel is BigQuery processing engine which inspired by the MapReduce shuffle implementation.*
> * *For Spark or MapReduce, traditionally shuffle data will be persisted temporarily on the worker before being shuffled to other workers.*
> * *For Dremel, RAM and disk resources needed to store intermediate shuffle data were managed separately to execute shuffle operation more efficiently.*

---

## Intro

I used to hate reading academic papers.

All the jargon and mathematical formulas made me feel... stupid.

But it changed.

On 15th August 2023...

The day when I first finished reading a paper.

(The "finish" is important here; I had tried many times before, but it always ended the same way: I stopped after finishing the "Abstract" section).

So, what motivated me?

The answer is simple: I was bored with the pleasant experience when working with BigQuery.

Just need to input SQL query, configure this, configure that using the UI console, and voila.

Google hides all the complexity from the user.

(Don’t get me wrong; I thank Google every day for this convenience).

But the easier it became for me to operate on BigQuery, the more curious I became about what Google was hiding.

That brings me to Google’s paper about Dremel - the BigQuery processing engine:

> *[Dremel: A Decade of Interactive SQL Analysis at Web Scale.](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf)*

(It's quite easy to read, no mathematical formulas, trust me.)

(Google does not open-source BigQuery, so the only way I can know how things work internally is by reading their paper).

It took me 3 days to finish the paper, and this article is a small note about the main idea of the BigQuery processing engine: Shuffle.

> *Material from this paper will be used in this article to explain how Google implements shuffle for Dremel.*

---

## Dremel

> *Let make friend with Dremel first.*

[BigQuery is a combination of many technology](https://cloud.google.com/blog/products/bigquery/bigquery-under-the-hood).

(Google loves to… separate things)

They use [Colossus](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system) for storage, [Borg](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) for compute management and …

[Dremel](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf) for query processing engine.

Simply said, when you feed you SQL query into BigQuery, Dremel will handle executing the query and return the result for you.

Following the [paper](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf) I mentioned above, here is the basic idea of Dremel:

> *Inspired by the MapReduce shuffle implementation, Dremel’s shuffle utilized local RAM and disk to store sorted intermediate results.*

(Sound like Spark huh?)

The keyword here is “MapReduce Shuffle“ so it make sense if we revisit it a little bit.

---

## Shuffle

The definition from Wikipedia is a good start, so I will bring it here:

> ***MapReduce** is a framework for processing parallel problems across large datasets using a large number of computers, usually composed of three operations:*
>
> ***Map:** each worker node applies the* `map` *function to the local data, and writes the output to a temporary storage. (RAM or hard disk)*
>
> ***Shuffle:** worker nodes redistribute data based on the output keys (produced by the* `map` *function), such that all data belonging to one key is located on the same worker node.*
>
> ***Reduce:** worker nodes now process each group of output data, per key, in parallel.*
>
> —*[Wikipedia](https://en.wikipedia.org/wiki/MapReduce)—*

If you still confused, I have an illustration here:

[![](https://substackcdn.com/image/fetch/$s_!VdPE!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafdb62ea-852c-4d33-abdc-278803948dc2_1236x852.png)](https://substackcdn.com/image/fetch/$s_!VdPE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafdb62ea-852c-4d33-abdc-278803948dc2_1236x852.png)

drawn by myself

Because Dremel is inspired by the MapReduce implementation, the main idea is still the same: data, after being processed by a worker, will be moved (shuffled) to the next worker it belongs to.

The idea is quite straightforward, but life is not simple like that,…

Everything is fine until you put PBs of data into it…

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

## How Google Implemented Dremel’s Shuffle

### Problems

As you can see from above section, in traditional MapReduce approach, the data will be shuffled directly from the mapper’s temporary storage to the reducer.

The tight-coupling architecture, such as this, causes serious problems for Google, especially when processing an enormous amount of data.

Here some insights straight from the paper:

> * *It is not possible to efficiently mitigate the quadratic scaling characteristics of shuffle operations as the number of data producers and consumers grew.*
> * *The coupling inherently led to resource fragmentation and stranding and provides poor isolation. This became a major bottleneck in scalability.*

Here is my understand (feel free to correct me):

* When dealing with very very large data, the scaling of “mapper“ and “reducer” is not predictable. Beside that, the shuffle output are depends on the characteristic of the input data

  + For example, if you dataset contains 1 millions distinct user, `GROUP BY` by `USER_ID` will roughly resulted in 1 million “bucket“.

    → This even make the system dealing with internet-scale of data like Dremel harder to operate efficiently.
* Compute and the temporary storage can not be scaled independently.

So, how does Google deal with it?

### Solutions

Realizing the problem is the coupling between compute and temporary storage, Google simply said:

“Let’s separate it“.

Instead of colocating shuffle temporary storage with the worker, they proposed:

> *…RAM and disk resources needed to store intermediate shuffle data were managed separately in a distributed transient storage system.*

To help you better imagine:

[![](https://substackcdn.com/image/fetch/$s_!PFW7!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9380ddc-88d4-4836-9d91-11f35314cfd4_1232x826.png)](https://substackcdn.com/image/fetch/$s_!PFW7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9380ddc-88d4-4836-9d91-11f35314cfd4_1232x826.png)

The separate in-memory shuffle act like a “queue“ where multiple worker publish shuffle data to it and multiple worker actively consume it. Reference: [paper](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf)

Google give some advantages of this approach:

> * *Reduced the shuffle latency.*
> * *Enabled an order of magnitude larger shuffles.*
> * *Reduced the resource cost of the service by more than 20%.*

Unfortunately, the paper didn’t go more deeply into it, so I’ve to look for [another resource](https://www.youtube.com/watch?v=4m1-QdumkwU&t=2782s), and here what I found:

* First of all, the temporary storage can now be scaled independently.
* This will achieve better fault tolerance: if a worker fails, a new worker can be brought up without losing intermediate shuffle data because it is already persisted in a separate place.
* It enables more flexible execution: now they can allocate the number of workers based on the intermediate shuffle output at runtime.

---

## Outro

I think that's all for my first attempt at writing long-form content like this.

(Although it's not so long)

From a high-level view, Google simply separates the shuffle intermediate layer from the worker in Dremel to make it easier to scale.

One thing to understand is that relocating temporary storage far from the worker is not an easy task.

Google admitted this in the paper. (I will share the details with you guys when I fully grasp it.)

Moreover, the problem with shuffle not only happens with Dremel; other big tech companies like Uber and Facebook (now Meta) also faced similar problems with Spark.

If you're interested, here are two resources on how they dealt with it (the main idea is the separation of the shuffle layer, similar to Dremel):

* Uber: [Highly Scalable and Distributed Shuffle as a Service](https://www.uber.com/en-SG/blog/ubers-highly-scalable-and-distributed-shuffle-as-a-service/)
* Facebook: [Riffle: Optimized Shuffle Service for Large-Scale Data Analytics](https://haoyuzhang.org/publications/riffle-eurosys18.pdf)

Now, it time to say goodbye.

See you next time, maybe with another cool insight from the Dremel paper about BigQuery. 😉

---

## Before you leave

Leave comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/bigquery-processing-engine-shuffle/comments)

It might take you 3 minutes to read but it took me more than 3 days to prepare, so it will motivate me a lot if you consider subscribe to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
