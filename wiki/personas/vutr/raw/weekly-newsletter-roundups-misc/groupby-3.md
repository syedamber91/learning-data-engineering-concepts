---
title: "GroupBy #3"
channel: vutr
author: "Vu Trinh"
published: 2023-09-22
url: https://vutr.substack.com/p/groupby-3
paid: false
topics: ["Apache Kafka", "Apache Spark", "Streaming", "Batch Processing"]
tags: [https, auto, spark, image, media, kafka]
---

# GroupBy #3

*My Docker cheat sheet, original stories on Spark and Kafka, "Why is Hadoop slower than Spark?," HDFS vs. S3, and finally, Kimball vs. Inmon.*

> Source: [Open post](https://vutr.substack.com/p/groupby-3)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]]

---

### My docker command cheatsheet

You can visit my original post on linkedin [here](https://www.linkedin.com/posts/vutr27_docker-softwareengineering-dataengineering-activity-7110223581619384320-YQ17?utm_source=share&utm_medium=member_desktop).

(Is it weird that I put my own content in here?)

[![](https://substackcdn.com/image/fetch/$s_!tN9t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3b847f3-699a-4373-bbf1-60f2654ddc02_1111x1571.gif)](https://substackcdn.com/image/fetch/$s_!tN9t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3b847f3-699a-4373-bbf1-60f2654ddc02_1111x1571.gif)

### History of Apache Spark : Journey from Academia to Industry

[![](https://substackcdn.com/image/fetch/$s_!G-m8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1a7c034-ca9f-421d-9a96-4cccdb164752_942x402.png)](https://substackcdn.com/image/fetch/$s_!G-m8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1a7c034-ca9f-421d-9a96-4cccdb164752_942x402.png)

If you are a data engineer, you must have (at least) heard of Spark throughout your career.

Let’s set aside how fast Spark is and how it became one of the most popular data processing engines out there. Instead, let's focus on 'How Apache Spark started?' and the problem it aimed to solve at that time.

An 8-year-old blog post by [Madhukara Phatak](https://madhukaraphatak.com/) captures some of the interesting questions from an interview in which [Ion Stoica,](http://people.eecs.berkeley.edu/~istoica/) a UC Berkeley professor, discussed the history of Apache Spark - might give you the answer.

Spark was started as a class project at [UC Berkeley](https://www.berkeley.edu/). The idea was to build a cluster management framework that could support various types of cluster computing systems.

They also aimed to differentiate themselves from existing cluster computing systems. At that time, Hadoop was primarily focused on batch processing, so they shifted their focus to [interactive](https://en.wikipedia.org/wiki/Interactive_computation) [iterative](https://en.wikipedia.org/wiki/Iterative_method#:~:text=In%20computational%20mathematics%2C%20an%20iterative,derived%20from%20the%20previous%20ones.) computations.

You can read the full blog (which also contains the full interview)

<https://blog.madhukaraphatak.com/history-of-spark>

---

Subscribe to **SELECT \*** receive cool content that could make your life as a data engineer less boring.

---

### **“Why is Hadoop slower than Spark?”**

Trying to figure out the reason behind Spark's wide adoption in the data processing field, and this Quora question caught my attention.

(The correct question might be 'Why is MapReduce slower than Spark?')

Back to the question on Quora: I clicked it, scrolled a little bit, and stopped right at an interesting answer from [Travis Addair](https://www.quora.com/profile/Travis-Addair).

His emphasis on **why MapReduce was designed this way at Google** and **why Spark is appealing to the industry as 'the MapReduce for the rest of us'** is really worth your time reading (by the way, it’s quite short).

Here’s a link:

<https://www.quora.com/Why-is-Hadoop-slower-than-Spark/answer/Travis-Addair?ch=10&oid=173920889&share=8bc70da5&srid=uIVXeO&target_type=answer>

*This image is from the article link.*

[![](https://substackcdn.com/image/fetch/$s_!V0n9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feae2fcc9-000a-4d71-a9b8-7d85b79137b9_600x247.jpeg)](https://substackcdn.com/image/fetch/$s_!V0n9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feae2fcc9-000a-4d71-a9b8-7d85b79137b9_600x247.jpeg)

### **HDFS vs S3**

If there is an article about 'MapReduce vs Spark,' why not continue with 'HDFS vs S3'?

Can say that while Spark has become a more popular choice when people consider a solution for (big) data processing, the same has happened with cloud storage (S3, for example) in terms of data lakes.

> *I am very annoyed that all sorts of big data engineers confuse S3 and HDFS systems, assuming that S3 is the same as HDFS. That’s not true.*

The author bring a very informative blog post by comparing HDFS and S3 on multiple criteria like architecture, atomicity, consistency, scalability and latency and come with conclusion at the end why “*the benefits of HDFS have become minimal and not worth the complexity it brings.*“

Read the blog at: <https://luminousmen.com/post/hdfs-vs-cloud-based-object-storage-s3>

*This image is from the blog post. (not sure if he’s a Naruto fan)*

[![](https://substackcdn.com/image/fetch/$s_!iTpH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf8927d5-b250-49f9-b56f-9f5d69392608_800x599.jpeg)](https://substackcdn.com/image/fetch/$s_!iTpH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf8927d5-b250-49f9-b56f-9f5d69392608_800x599.jpeg)

### **Another original story, this one is about Apache Kafka at Linkedin**

[![](https://substackcdn.com/image/fetch/$s_!mdZ9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e962c76-b0ca-4b52-9e97-763c4aba808c_942x364.png)](https://substackcdn.com/image/fetch/$s_!mdZ9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e962c76-b0ca-4b52-9e97-763c4aba808c_942x364.png)

Apache Kafka is a distributed event streaming platform designed for high-throughput, fault-tolerant, and real-time data streaming.

(Do you know that [Jay Kreps](https://www.linkedin.com/in/jaykreps/) - one of the co-creators of Kafka chose to name the software after the author [Franz Kafka](https://en.m.wikipedia.org/wiki/Franz_Kafka) because it is "a system optimized for writing", and he liked Kafka's work.)

This article is a contribution by Joel Koshy, a member of the Kafka team, about the story of why they developed Kafka in the first place.

<https://insidebigdata.com/2016/04/28/a-brief-history-of-kafka-linkedins-messaging-platform/>

### **[Kimball](https://www.amazon.com/Data-Warehouse-Toolkit-Definitive-Dimensional/dp/1118530802) and [Inmon](https://www.amazon.com/Building-Data-Warehouse-W-Inmon/dp/0764599445)**

If you know [A ‘Cage Match’ Between Elon Musk and Mark Zuckerberg](https://www.nytimes.com/2023/07/01/technology/elon-musk-mark-zuckerberg-cage-match.html) (the winner, I guess, would have the best social media in the world), you will find this relevant.

[In a short video on the possibility of “Cage Match“](https://www.linkedin.com/posts/eczachly_dataengineering-dataarchitecture-activity-7109283315697819648-yxdd?utm_source=share&utm_medium=member_desktop) between [Ralph Kimball](https://en.wikipedia.org/wiki/Ralph_Kimball) and himself, [Bill Inmon](https://en.wikipedia.org/wiki/Bill_Inmon) points out that these two approach answer different questions. With Kimball, the question is “how do you get reports up and done quickly“. Meanwhile, with Inmon, you might want to focus on the "believability" of your data.

If you want to delve deeper into the differences between these two, I have an article for you:

<https://tdan.com/data-warehouse-design-inmon-versus-kimball/20300>

---

Thanks for reading **SELECT \***! Subscribe for free to receive new posts weekly.

---

###
