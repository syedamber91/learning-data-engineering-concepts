---
title: "Batch and Stream Processing"
channel: vutr
author: "Vu Trinh"
published: 2025-09-16
url: https://vutr.substack.com/p/batch-and-stream-processing
paid: true
topics: ["Data Engineering", "dbt", "Apache Spark", "Apache Flink", "Data Warehouse", "Streaming", "Batch Processing"]
tags: [https, auto, processing, time, media, substackcdn]
---

# Batch and Stream Processing

*What they are and how they're implemented. Fundamental knowledge that can be applied to any processing framework.*

> Source: [Open post](https://vutr.substack.com/p/batch-and-stream-processing)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[data-warehouse|Data Warehouse]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]]

---

> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!tsPk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fccd79bde-c3d2-46d5-b2f4-88fa2153c5e3_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!tsPk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fccd79bde-c3d2-46d5-b2f4-88fa2153c5e3_2000x1428.png)

---

## Intro

One of the data engineer's responsibilities is to capture the real-life data, add spices, cook, and serve it. There are different ways to do it. We wait for the collected data to reach a certain threshold (e.g., daily, weekly,…), then process them all at once. This is called batch processing.

That might be too long. Instead of waiting, we can process a piece of data right after it happens. After completing this piece, the next one will follow, and things will continue to unfold in this manner. This is called stream processing.

In this article, we delve deep into these data processing concepts, what they are, how they differ, the trade-offs, and the key considerations.

---

## tl;dr

* **Batch**: A Simple and more familiar data processing paradigm. The complete view of the data simplifies the data processing and re-processing. However, users have to wait → High latency.
* **Stream:** Far lower latency and treat data as an unbounded flow. To facilitate efficient and reliable data processing, users must consider several key aspects, including windowing, event-time vs processing time, watermark state, and checkpointing. This approach, however, introduces a higher learning curve. Implement this only if your organization truly gets benefit from stream processing.

---

## Batch

Batch processing is the most straightforward to understand. You assemble the data over a period and then process it in a single operation.

You read a CSV file, load it into memory, process it with Spark, and then write the results to the database. That is batch processing. You take a snapshot of an OLTP database, transform it with SQL, and load it into the data warehouse. That is batch processing.

[![](https://substackcdn.com/image/fetch/$s_!UWdz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4827ee19-7aeb-4d7d-a774-50fd689179fa_448x338.png)](https://substackcdn.com/image/fetch/$s_!UWdz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4827ee19-7aeb-4d7d-a774-50fd689179fa_448x338.png)

A CSV file or a database snapshot shares a characteristic: they capture the data in a defined boundary, which might be an hour, a day, 3 days, or a week of data. When a system processes data in a batch, it knows the size of the processed data beforehand. This finite view significantly simplifies the data processing.

Essentially, aggregation and joining are searching for records with the same key. With batch processing, the system knows beforehand the scope of the searching process. This is sound obvious, but when it comes to stream processing (the system doesn’t see the scope for search), you will understand clearly this advantage of batch processing.

[![](https://substackcdn.com/image/fetch/$s_!b4_k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4bf12e7-0c64-46f1-9bb9-ae8c2d1f88f1_790x512.png)](https://substackcdn.com/image/fetch/$s_!b4_k!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4bf12e7-0c64-46f1-9bb9-ae8c2d1f88f1_790x512.png)

In addition, achieving fault tolerance or the re-processing ability is straightforward if we have these three conditions:

* The data source is available when we need to reprocess.

  + We can control this by keeping the data source for a while (placing the CSV data or database snapshot in the object storage)
* The processing is deterministic. With the same input, the processing guarantees to produce the same output no matter how many times it runs. This guarantees we can reproduce the output with the same process logic and input data.

  [![](https://substackcdn.com/image/fetch/$s_!SDOF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15e7c4f8-87bd-4138-b1dc-1299fb77f8d4_516x298.png)](https://substackcdn.com/image/fetch/$s_!SDOF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15e7c4f8-87bd-4138-b1dc-1299fb77f8d4_516x298.png)
* The effect of the processing is idempotent. In simpler terms, idempotence means that doing something once has the same effect as doing it many times.

  [![](https://substackcdn.com/image/fetch/$s_!rN9K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0397d6a1-e667-4368-a406-c09d4797ecdb_828x398.png)](https://substackcdn.com/image/fetch/$s_!rN9K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0397d6a1-e667-4368-a406-c09d4797ecdb_828x398.png)

  + For example, f(x) = 1\*x is an idempotent function, as we can get the same result when running this function multiple times for the same input.
  + In batch processing, to achieve idempotence, the next run with the same input must replace entirely any previous output of the prior run
  + This guarantees we don’t cause side effects with subsequent runs (e.g., append duplicate data or mix up data between runs)
  + We can control this by using an idempotent operation to materialize the data. `CREATE OR REPLACE TABLE` and [dbt’s insert overwrite strategy](http://dbt’s insert overwrite) are examples.

> ***Note**: Deterministic refers to the output, while idempotence pertains to the effect of the output on the system.*

Systems like Spark enhance fault tolerance efficiency by re-processing only the affected data, rather than all of it. [Spark’s unit of computation is RDD](https://vutr.substack.com/i/166248471/spark-rdd). Spark keeps track of each RDD’s dependencies on other RDDs, the series of transformations that created it.

Suppose any partition of an RDD is lost due to a node failure or other issues. Spark can reconstruct the lost data by reapplying the transformations to the original dataset described by the lineage.

Batch processing is implemented quite similarly in many systems. From being aware of the boundary dataset, planning the processing (in the most optimized way), to scheduling the physical processing on the worker(s).

---

## The data boundary

Batch processing is excellent in terms of operational complexity and ease of use. However, it's bad at one thing: it has to wait for the data to reach a threshold. Sometimes, users don’t want to wait (too long). Some businesses require the data to be processed as soon as it happens: a recommendation system needs to react to the user's actions, or a payment service needs to detect an anomalous transaction as quickly as possible.

[![](https://substackcdn.com/image/fetch/$s_!zMsb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b62953f-8bda-44d4-8edc-a2f4a427deeb_1036x576.png)](https://substackcdn.com/image/fetch/$s_!zMsb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b62953f-8bda-44d4-8edc-a2f4a427deeb_1036x576.png)

We enter the realm of stream processing, which promises far lower latency compared to batch and enables us to deal with the data in its natural form, a continuous flow.

Let’s take a look around and think about it. Most of the data we work with doesn’t have a natural boundary; in other words, it is unbounded: from the user interaction on the website (unless the website is down) to data from IoT sensors (unless the sensor runs out of power).

With batch processing, we impose artificial boundaries (e.g., one day of data) to simplify the data processing. Unbounded or bounded data is a crucial characteristic when it comes to distinguishing between batch and real-time processing.

---

## Stream processing

> *There are two approaches to implement stream processing: the first is micro-batching (Spark Structured Streaming) and record-by-record, which is also referred to as accurate stream processing, or Flink. The insight in this section could be applied to both of the approaches.*

### Source and the sink

[![](https://substackcdn.com/image/fetch/$s_!IcLh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c8419fc-f335-4bf9-957d-16cca2e20f1a_718x164.png)](https://substackcdn.com/image/fetch/$s_!IcLh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c8419fc-f335-4bf9-957d-16cca2e20f1a_718x164.png)

Because this processing paradigm sees the data as a continuous stream, the data source and the sink must also produce and accept the stream of unbounded data. For example, if you want to read a file in stream processing, you have to stream the content of the file (e.g., row by row) to the processing engine.

### Time

In Batch processing, we don’t have to deal with the time. The start and end boundaries already give us enough information. However, when dealing with the continuous flow of data, the notion of time becomes the critical factor. There are two kinds of time:

[![](https://substackcdn.com/image/fetch/$s_!CqLI!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d006dfe-1bbd-4926-83ea-466d8d7a8059_964x302.png)](https://substackcdn.com/image/fetch/$s_!CqLI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d006dfe-1bbd-4926-83ea-466d8d7a8059_964x302.png)

* **Event Time**: the time the event itself happened. For example, if the system recorded you purchasing a game item at **12:30**, this is considered the event time.
* **Processing Time**: The time at which an event is observed at any given point during processing. For example, the purchased game item is recorded at 11:30 but only arrives at the stream processing system at 11:35; this **“11:35“** is the processing time.

Event time remains constant, but processing time varies with each step the data takes. This is a critical factor when analyzing events in the context of when they occurred. In fact, logging the time at which the event actually happens (I mean down to nano or microseconds) is nearly impossible. That said, the time the system assigns for an event when observed is widely accepted.

### Watermarks

The difference between the event and the processing time is called time skew. The skew can result from many potential reasons, such as network communication delays.

[![](https://substackcdn.com/image/fetch/$s_!kY3L!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd9f3307-f674-4e72-a8da-bc2bf31884c0_884x882.png)](https://substackcdn.com/image/fetch/$s_!kY3L!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd9f3307-f674-4e72-a8da-bc2bf31884c0_884x882.png)

Watermark is the typical way to measure the skew. The watermarks tell the system that ***“no more data which have an event time earlier than this time will arrive.”*** If the watermark is X, the system can assume that no events with a timestamp less than X will appear.

[![](https://substackcdn.com/image/fetch/$s_!7xu9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe7b63f6-fa81-4b4d-b3c1-5fdc69f7beeb_502x274.png)](https://substackcdn.com/image/fetch/$s_!7xu9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe7b63f6-fa81-4b4d-b3c1-5fdc69f7beeb_502x274.png)

> ***Note 1**: In a super-ideal world, the skew would always be zero; we could always process all events right when they happen.*
>
> ***Note 2**: As I know, the watermark is an estimated indication; it is not absolute. For example, if a watermark is at 10:15, there is a chance that data with an event time of 10:13 arrives.*

The watermark offers a configurable tradeoff between accuracy and latency

* Eager watermarks ensure low latency but potentially lower accuracy, as late events might arrive after the watermark.
* If watermarks are too relaxed, data might have a chance to catch up, but might increase processing latency due to the time spent waiting.

> ***Note:** Spark Structured Streaming and Flink implement the watermark differently. Please consider this when implementing the streaming job.*

### Windowing

As we discussed in the batch section, aggregation and joining involve searching for records with the same key. That said, the space for searching must be finite; the system looks for an ad click event for the same user to calculate the total click. The space must have a limited size, in one day or one week. If it doesn’t, how does the system know it can stop doing the searching?

With batch processing, the system knows the searching space beforehand. It is simply the whole batch that the system is processing. Given the (theoretically) infinite data stream, how do we know the size of the searching space? We place the boundaries by windowing.

Windowing divides the infinite stream into finite chunks. Usually, the system uses time notions to organize data into the window (e.g., all data in the last 1 hour will belong to one window). Now, the searching space for the aggregation and join has a known size.

There are three major types of windows:

[![](https://substackcdn.com/image/fetch/$s_!ARk1!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffe615c0-899a-41cd-8a52-ce620c7e5c68_1424x612.png)](https://substackcdn.com/image/fetch/$s_!ARk1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffe615c0-899a-41cd-8a52-ce620c7e5c68_1424x612.png)

* **Fixed (Tumbling)**: The windows are defined as static window size, e.g., hourly windows.
* **Sliding:** The windows are defined by a window size and slide period, e.g., 30-minute windows starting every five minutes.
* **Session:** The windows capture some period of activity over a subset of the data, in this case, per key. Typically, they are defined by a timeout gap.

### Example of session windows.

In the three types of windows above, the **session** does not seem straightforward at first. So, here is an example for better understanding

Imagine you're tracking user clicks on a website to analyze their behavior. You'd like to know how many pages a user visited in a single browsing session. You set a session window with a 10-minute gap:

[![](https://substackcdn.com/image/fetch/$s_!9Z28!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9973281-0107-423a-aeba-ac9da1381138_1392x374.png)](https://substackcdn.com/image/fetch/$s_!9Z28!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9973281-0107-423a-aeba-ac9da1381138_1392x374.png)

* **10:00:00**: User clicks on the homepage. This is the **first event**, which **starts a new session window**. The window's end time is provisionally set to 10:10:00 (10:00:00 + 10 minutes).
* **10:05:00**: User clicks on a product page. This event arrives within the 10-minute inactivity gap of the previous event. The window **expands to include this event**, and its end time is reset to 10:15:00 (10:05:00 + 10 minutes).
* **10:08:00**: User adds the product to their cart. This event is also within the gap. The window **expands again**, and its end time is reset to 10:18:00 (10:08:00 + 10 minutes).
* **10:25:00**: User performs no activity for 17 minutes. This gap (from 10:08 to 10:25) is **greater than the 10-minute inactivity gap**. The session window that started at 10:00:00 is now **closed and finalized**.
* **10:25:00**: The user returns and clicks on the checkout page. This event, arriving after the inactivity gap, **starts a brand new session window**, with its end time set to 10:35:00.

### Triggers

Windowing could divide the stream into a concrete batch. However, the system requires a signal to indicate that the window is ready for processing. This is where the trigger comes.

A trigger determines when the results of a windowed aggregation should be computed and emitted. While the window defines which events are grouped (e.g., all events in a 1-minute interval), the trigger dictates the specific moment when the calculation for that window is performed and its output is sent downstream.

Think of it like this:

* **Windowing** is like collecting salad ingredients in a bowl. It defines the set of events you will be working with.
* **Triggering** is like deciding when to finish mixing the ingredients and serve the salad. It's the action that causes the calculation to happen.

There are several common trigger types you will see:

[![](https://substackcdn.com/image/fetch/$s_!2H7O!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57da901f-e331-42db-8f68-0fa2d35419e5_1452x612.png)](https://substackcdn.com/image/fetch/$s_!2H7O!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57da901f-e331-42db-8f68-0fa2d35419e5_1452x612.png)

* **Event-time trigger**: It fires based on the progress of event-time. This type is usually implemented with the watermark.
* **Process-time trigger**: It fires at the point in processing time.
* **Data-arriving characteristics trigger**: Triggering based on factors such as counts, bytes, data punctuations, pattern matching, etc.
* **Composite trigger:** It combines triggers in some way.

### Example of an even-time trigger

With a fixed window of 10 minutes and an event-time trigger, the data occurring within the 1:05 to 1:15 interval will belong to that window. The window is triggered when the event time passes 1:15. However, without knowing the time the data happens, how does the system determine that the event time has passed 1:15?

[![](https://substackcdn.com/image/fetch/$s_!_2Ds!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c156f94-9ffc-43d0-a2cd-50dd1ce45555_906x634.png)](https://substackcdn.com/image/fetch/$s_!_2Ds!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c156f94-9ffc-43d0-a2cd-50dd1ce45555_906x634.png)

Tweaking the question a bit, the problem is far simpler: “How do I know that data with event time less than 1:15 has all arrived?“ This is where the watermark comes to the rescue.

Recall that if the watermark is X, the system can assume that no events with a timestamp less than X will appear. In this case, the system waits for the watermark to advance to 1:15 to trigger the window safely.

### Late event

With the example above, data with the event time between 1:05 and 1:15, but that comes after the time when the watermark is passed the end of the window, is considered late and is dropped by default.

[![](https://substackcdn.com/image/fetch/$s_!QRdf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1918b5cb-b153-4c14-a59b-5144c0ba2479_530x518.png)](https://substackcdn.com/image/fetch/$s_!QRdf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1918b5cb-b153-4c14-a59b-5144c0ba2479_530x518.png)

However, in most streaming frameworks, we can define a grace period to allow for late data. For example, “let’s wait for another 2 minutes.“Late events that come in this extra period will be included in the window.

The late boundary is relative to the watermark. Back to the example above with the 1:05 - 1:15 window, assume we allow for the event to be 1 minute late, the watermark will form the late boundary at 1:16 (1:15 + 1 min) event time plus the associated processing time.

If the data has an event time between 1:05 and 1:15, it will be accepted if it arrives after the watermark passes the end of the window (1:15) but still below the late boundary.

[![](https://substackcdn.com/image/fetch/$s_!ueAo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fccd22f76-4709-4a07-864c-bc6d2a3f045c_614x634.png)](https://substackcdn.com/image/fetch/$s_!ueAo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fccd22f76-4709-4a07-864c-bc6d2a3f045c_614x634.png)

### State

For stateful operation, we need a … state. Simply put, it is a variable that is updated with new data to yield the final result. For example, to calculate the count of the ad clicks in a window, the worker must store the counter somewhere to accumulate the ad clicks count.

[![](https://substackcdn.com/image/fetch/$s_!iM6h!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5eca2cf-03ef-4fe8-9fd2-c069ea7d4d01_544x362.png)](https://substackcdn.com/image/fetch/$s_!iM6h!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5eca2cf-03ef-4fe8-9fd2-c069ea7d4d01_544x362.png)

And that’s it, the idea of the state is that simple. However, managing it efficiently is another story, as it involves ensuring fault-tolerance (what happens to the state if a worker dies), scalability (how to distribute the state between workers), and cleaning up the state storage for new incoming data.

Luckily, all the stream processing engines that support stateful operations provide the necessary tools for us to manage state. We don’t have to do it from scratch. Flink also lets you choose your preferred state backend, which could be the worker’s memory, the RockDB instance, or, recently, it allows you to [store the state in object storage](https://www.vldb.org/pvldb/vol18/p4846-mei.pdf).

### Fault tolerance

This is when we see the clear advantage of batch processing here. In the worst case (if we don’t have a mechanism like Spark RDD lineage to re-process only the affected data), we re-process the whole batch when failure happens.

However, with stream processing, it’s a different story.

“In what position in the stream will we start re-processing?“

[![](https://substackcdn.com/image/fetch/$s_!4iPt!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f2f7260-1a72-4160-9418-e4d282e36554_1322x696.png)](https://substackcdn.com/image/fetch/$s_!4iPt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f2f7260-1a72-4160-9418-e4d282e36554_1322x696.png)

Most stream processing frameworks achieve fault tolerance primarily through checkpointing. Checkpointing is a mechanism that periodically saves the entire state of a streaming job to an external and durable storage (e.g., HDFS, S3). If there is a failure, the framework can restart the job from the last checkpoint, ensuring that no data is lost and processing continues from a consistent state.

---

## Outro

In this article, we first discuss batch processing, the paradigm that I believe most of us are familiar with. We talk about the simplicity of this paradigm and the importance of idempotence. The downside of batch processing is that users have to wait.

This led to stream processing, with a guarantee for low latency by processing the data as soon as it happens. Unlike batch processing, this paradigm sees the data as a continuous flow. This makes users consider all aspects, such as the time, the windowing, the trigger, handling late events, the state management, and making the stream job fault-tolerant via checkpointing.

Thank you for reading this far. See you in my next article.

---

## Reference

*[1] [Flink Official Documentation](https://nightlies.apache.org/flink/flink-docs-master/)*

*[2] [Spark Streaming Programming Guide](https://spark.apache.org/docs/latest/streaming-programming-guide.html#spark-streaming-programming-guide)*

*[3] Google, [The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43864.pdf) (2015)*

*[4] Tyler Akidau, Slava Chernyak, Reuven Lax, [Streaming Systems](https://www.oreilly.com/library/view/streaming-systems/9781491983867/) (2018)*
