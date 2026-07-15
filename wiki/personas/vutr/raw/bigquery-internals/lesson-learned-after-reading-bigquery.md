---
title: "You don't know this for sure: How BigQuery stores semi-structured data?"
channel: vutr
author: "Vu Trinh"
published: 2024-01-13
url: https://vutr.substack.com/p/lesson-learned-after-reading-bigquery
paid: false
topics: ["Data Engineering", "BigQuery"]
tags: [https, repeated, level, definition, nested, auto]
---

# You don't know this for sure: How BigQuery stores semi-structured data?

*Fact: Apache Parquet also implements this approach.*

> Source: [Open post](https://vutr.substack.com/p/lesson-learned-after-reading-bigquery)

## Topics

[[data-engineering|Data Engineering]] · [[bigquery|BigQuery]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

> *TL;DR: To store and retrieve nested and repeated field in columnar storage, Dremel introduced the notion of **definition** and **repetition** level.*
>
> *This allow reading the nested field independently without care the ancestor path (like when you reading JSON field) which help reduce the I/O but result in larger file size.*

---

[![](https://substackcdn.com/image/fetch/$s_!FqnZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d10037c-b2ef-4f87-8ede-a67289b6e3c0_1029x635.png)](https://substackcdn.com/image/fetch/$s_!FqnZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d10037c-b2ef-4f87-8ede-a67289b6e3c0_1029x635.png)

---

## Intro

Due to the daily boredom of inputting SQL into the BigQuery console, I decided to delve into [Google's paper on BigQuery's processing engine - Dremel.](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf)

[I proudly proclaimed to the world that I had finished the paper.](https://open.substack.com/pub/vutr/p/bigquery-processing-engine-shuffle?r=2rj6sg&utm_campaign=post&utm_medium=web)

But the truth is, I skipped a section.

The one explaining how Dremel (also BigQuery) handles nested and repeated fields in columnar storage.

It seemed too challenging, so I gave up without any hesitation.

A few days later, in my daily work, I encountered a problem with nested fields in Parquet, so I explored the Parquet homepage a little bit…

Here's what I found:

> *To encode nested columns, **Parquet** uses the **Dremel** encoding with definition and repetition levels.*

This sentence made me realize that I had overlooked one of the most important parts of the BigQuery paper, which influences the way Apache Parquet file formats handles nested and repeated fields.

Therefore, I have decided to revisit the part that I initially skipped: Nested and Repeated fields in Dremel.

> *Material from this paper will be used in this article to explain the how Dremel (BigQuery) store Nested and Repeated fields*

---

## Columnar Storage

Columnar storage is a data storage format where data is stored in columns rather than rows. In a traditional row-based storage system, all the values for a single row are stored together, while in columnar storage, all the values for a single column are stored together.

This format is particularly well-suited for Online Analytical Processing (OLAP) databases due to its advantages in terms of query performance and analytics.

In the OLAP world, you only need a subset of columns. With columnar storage, the database only needs to scan columns independently without the need to load the full record.

This leads to the fact that nested and repeated fields, when stored in columnar storage, should follow their natural characteristic: allowing efficient reading and writing in a "column" style.

---

## Nested

So, What does it means when I said:

> *allow being read and written efficiently in “column” style.“*

(Sorry If you feel confused)

Imagine you have a nested field like this:

> `”Person”: {`
>
> `“Country“: “America“,`
>
> `“Info“: {`
>
> `“Name“: “ Bruce “,`
>
> `“Phone“:`
>
> `[“123456“, “78910“]`
>
> `}`
>
> `}`

How can you stored `Country` as an independent column but also keeping the hierarchical information (which it belong to `Person` field).

Google has introduced the concept of ***definition level*** to deal with this.

Allow me to borrow a definition of the term "definition level" from Google:

> *Each value of a field with path p, esp. every NULL, has a definition level specifying how many fields in p that could be undefined (because they are optional or repeated) are actually present in the record.*

Difficult to comprehend, isn't it?

Here is my version:

> *The maximum level at which the path is defined.*

(This might be oversimplified, but it helped me grasp the idea, so I hope it helps you too.)

Back to the example above, consider the full path of field `Name` is:

> `Person.Info.Name`

Let point out the definition level of `Name` in below scenario:

[![](https://substackcdn.com/image/fetch/$s_!APtP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb1e5e70-95fd-4c3f-9b48-6ef1b879b324_1164x436.png)](https://substackcdn.com/image/fetch/$s_!APtP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb1e5e70-95fd-4c3f-9b48-6ef1b879b324_1164x436.png)

* We can see there are total of 3 level here: `Person`, `Info` and `Name`.
* If the level `Name` has defined value it will have the definition level of 3.
* In case the `Name` is NULL, but we have `Info` level is defined, the definition level of `Name` is 2. Because “*the maximum level at which the path is defined*” is at `Info`, which is level 2.
* With the same logic, if both `Info` and `Name` areNULL but `Person` is defined, the definition level of `Name` is now 1.
* Even `Person` is NULL, the definition level of `Name` is0.

Simple huh?

Now let's move on to how Google dealt with repeated fields.

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

## Repeated

> *Array-alike*

The problem statement here is quite similar to nested fields.

How can you store an array as an independent column while also retaining information that values belong to the same array?

Imagine you have a repeated field like this:

> `[[1,2,3],[4,5,6]]`

How you stored this in columnar storage.

From Google, they introduced the ***repetition level***, which is:

> *It tells us at what repeated field in the field’s path the value has repeated.*
>
> *… level 0 denotes the start of a new record.*

Very straight forward.

With the example of the repeated field above, we can identify two repeated levels: the parent array (outermost [ ]), and two child arrays inside:`[1,2,3]` and `[4,5,6]`.

Following Google's definition, let's manually encode this repeated field:

[![](https://substackcdn.com/image/fetch/$s_!BIXq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc1142b3-53e1-4010-9424-3e0fadc5df29_1076x782.png)](https://substackcdn.com/image/fetch/$s_!BIXq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc1142b3-53e1-4010-9424-3e0fadc5df29_1076x782.png)

by myself

---

## So, what now?

Using the definition and repeated system, we can now encode nested and repeated fields efficiently.

I will borrow (again) a complete example from Google and put it here to consolidate all the knowledge above.

Given nested records R1 and R2 with schema and values:

[![](https://substackcdn.com/image/fetch/$s_!plBF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e81924f-6564-45f7-ba9a-6839e5b89e13_1180x828.png)](https://substackcdn.com/image/fetch/$s_!plBF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e81924f-6564-45f7-ba9a-6839e5b89e13_1180x828.png)

[source](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf)

Before begin, I will put the definition here so don’t have to scroll up and down.

**Definition level**:

> *The maximum level at which the path is defined.*

**Repetition Level:**

> *It tells us at what repeated field in the field’s path the value has repeated.*
>
> *… level 0 denotes the start of a new record.*

Now, zoom in to see how `Forward` field are stored using definition and repetition encoding.

Following the schema, here's what we expect from the `Forward` field:

> * `Forward` *is nested inside the* `Links`
> * `Forward` is a repeated field.

Following definition from above, this means:

> * Definition level of `Forward` with range from 0 to 2
>
>   + 0 if `Links` is NULL
>   + 1 if `Forward` is NULL but `Links` is not NULL
>   + 2 if `Forward` is defined
> * Repetition level of `Forward` with range from 0 to 1:
>
>   + 0 if this is a new record
>   + 1 if it repeated.

Now, just apply the rules and now we get the result (I also borrow from the paper):

[![](https://substackcdn.com/image/fetch/$s_!6Azt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d3a2c4f-37dc-4eab-b497-1993bfad29c3_274x374.png)](https://substackcdn.com/image/fetch/$s_!6Azt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d3a2c4f-37dc-4eab-b497-1993bfad29c3_274x374.png)

r is repetition level and d is definition level. [source](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf)

Let's go through this result line by line to make sure we’re on the same page:

* Value 20:

  + repetition: 0 → because it’s a new record (begin of record 1)
  + definition: 2→ because `Forward` is defined

* Value 40:

  + repetition: 1→ because it’s repeated
  + definition: 2→ because `Forward` is defined
* Value 60:

  + repetition: 1→ because it’s repeated
  + definition: 2→ because `Forward` is defined

* Value 80:

  + repetition: 0 → because it’s a new record (begin of record 2)
  + definition: 2→ because `Forward` is defined

With this encoding system, Google can now store nested and repeated field values efficiently while still maintaining the hierarchical and array-like information.

---

## Outro

The ultimate goal of Dremel when storing nested and repeated field is

> *…to encode all structure information within the column itself, so it can be accessed without reading ancestor fields.*

However, this has a tradeoff:

> *…this scheme leads to redundant data storage, since each child repeats the same information about the structure of common ancestors. The deeper and wider the structure of the message, the more redundancy is introduced.*

When comparing it to the approach of ORC or Arrow, the Dremel approach will result in a larger file size due to the space required for definition and repetition fields.

In return, because Dremel allows reading nested fields without traversing the ancestor path, it will result in lower I/O.

—

Few.

I think that’s it.

I've just explained the basic idea of how Dremel stores nested and repeated fields in columnar storage, a concept also applied by Twitter to the Parquet file format initially.

Now, it's time to say goodbye.

See you next time.

---

Reference:

* [Dremel: Interactive Analysis of Web-Scale Datasets](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf)
* [Dremel: A Decade of Interactive SQL Analysis at Web](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf)
* [Dremel made simple with Parquet](https://blog.twitter.com/engineering/en_us/a/2013/dremel-made-simple-with-parquet) - A very detailed blog from Twitter (the pioneers of Parquet) explains nested and repeated fields. You can skip my article and go straight to this blog to save time. (Please don't.)

---

## Before you leave

Leave comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/lesson-learned-after-reading-bigquery/comments)

It might take you 3 minutes to read but it took me more than 3 days to prepare, so it will motivate me a lot if you consider subscribe to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
