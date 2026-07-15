---
title: "How Meta Solves Data Lineage At Scale"
channel: vutr
author: "Vu Trinh"
published: 2025-02-13
url: https://vutr.substack.com/p/how-meta-solves-data-lineage-at-scale
paid: false
topics: ["dbt", "Apache Spark"]
tags: [lineage, meta, https, auto, image, flows]
---

# How Meta Solves Data Lineage At Scale

*Meta’s Approach to Data Lineage: How They Did It and What We Can Learn*

> Source: [Open post](https://vutr.substack.com/p/how-meta-solves-data-lineage-at-scale)

## Topics

[[dbt|dbt]] · [[apache-spark|Apache Spark]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=156304307)

[![](https://substackcdn.com/image/fetch/$s_!qH69!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6494f0a7-8e18-4770-b797-f0ee64c75517_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!qH69!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6494f0a7-8e18-4770-b797-f0ee64c75517_2000x1429.png)

Image created by the author.

---

## Intro

When Meta recently published an article titled [How Meta discovers data flows via lineage at scale](https://engineering.fb.com/2025/01/22/security/how-meta-discovers-data-flows-via-lineage-at-scale/), it instantly caught my attention.

As data engineers, we often hear about data lineage, but how many of us deeply understand its implications or the challenges of implementing it at scale? Meta’s approach to solving data lineage problems within their privacy infrastructure offers fascinating lessons.

In this article, we’ll explore Meta's challenges with data lineage, their solutions, and the practical lessons we can adopt—even if we don’t operate at Meta’s scale.

---

## A Little Bit About Meta

> *Even my low-tech mom use Facebook.*

[![](https://substackcdn.com/image/fetch/$s_!4p_-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f63999c-fad1-42c8-b6ec-2061042ea8f1_376x362.png)](https://substackcdn.com/image/fetch/$s_!4p_-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f63999c-fad1-42c8-b6ec-2061042ea8f1_376x362.png)

Image created by the author.

With billions of users across Facebook, Instagram, WhatsApp, and more, the company handles petabytes of data daily. This data isn’t just about scale; it’s deeply interconnected. Every click, post, or message can flow through a complex web of systems—from user-facing apps to backend services and data warehouses. Managing and understanding these flows is no small feat, especially as Meta prioritizes user privacy.

At the heart of their efforts is the Privacy-Aware Infrastructure (PAI), a suite of technologies that ensures privacy controls across their systems. Data lineage is a cornerstone of PAI, allowing Meta to trace how data flows and ensure compliance with privacy requirements.

---

## But what is data lineage?

[![](https://substackcdn.com/image/fetch/$s_!UFgu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98dcd58d-1caa-469b-b9ab-bb5310d5135d_1278x586.png)](https://substackcdn.com/image/fetch/$s_!UFgu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98dcd58d-1caa-469b-b9ab-bb5310d5135d_1278x586.png)

Image created by the author.

Data lineage is the process of tracing data's journey through various systems, from its source to its final destination. It answers questions like: Where did this data originate? How has it been transformed? Where is it being used? It gives us:

1. **Transparency and Trust**: It clarifies how data flows through systems, essential for ensuring compliance with privacy regulations and building user trust.
2. **Troubleshooting**: Knowing the data's path helps engineers pinpoint the root cause when issues arise.
3. **Impact Analysis**: When making changes to systems, data lineage allows teams to assess potential downstream effects, minimizing unintended disruptions.
4. **Compliance**: In an era of stringent data privacy laws, like GDPR and CCPA, having a clear picture of data flows is mandatory to demonstrate compliance and protect user privacy.

Data lineage isn't just a "nice-to-have"—it's a foundational piece of modern data systems.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=156304307)

---

## The Problem At Meta

### Why Data Lineage Matters

For Meta, data lineage helps them understand how data—such as a user’s religious views on Facebook Dating—moves from the input stage to backend processing, storage, and usage in downstream systems.

This transparency is critical for implementing and validating privacy controls. The initial data lineage status at Meta:

* Understanding the data flows across the system is crucial to establishing privacy controls in the PAI.
* An important service is Policy Zones, which answers the question: “Where does my data come from, and where does it go?”
* Internal users can use the lineage graphs to explain the data flow and where they collect and process it.
* Meta developed the Policy Zone Manager (PZM), a tool based on data lineage that lets developers identify multiple downstream assets from a set of sources. This accelerates the rollout of privacy controls.
* Once they implement privacy requirements, data lineage helps monitor and validate data flows continuously and provides enforcement mechanisms.

However, as Meta scaled PAI across all its apps, its existing lineage solutions fell short.

[![](https://substackcdn.com/image/fetch/$s_!JPye!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F260a060b-b217-4b3d-ac6f-3f31436c5e35_1468x702.png)](https://substackcdn.com/image/fetch/$s_!JPye!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F260a060b-b217-4b3d-ac6f-3f31436c5e35_1468x702.png)

Image created by the author.

Expanding PAI to all of Meta’s apps introduced a massive challenge: ensuring high-quality, detailed data lineage across diverse systems. Manual methods couldn’t keep up with the pace of change or the sheer number of data flows. Manually authoring diagrams and spreadsheets couldn’t handle the complexity or volume of their data.

Meta risked delays in implementing privacy controls without robust lineage tools, which could impact user trust and regulatory compliance.

### Is This Problem Unique?

[![](https://substackcdn.com/image/fetch/$s_!aA_m!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47ce6dcd-9c71-4f28-9227-07ae33f0cc8f_796x462.png)](https://substackcdn.com/image/fetch/$s_!aA_m!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47ce6dcd-9c71-4f28-9227-07ae33f0cc8f_796x462.png)

Image created by the author.

While Meta’s scale is unparalleled, the core problem—managing data lineage efficiently—is something many companies face. As organizations grow, they often grapple with fragmented systems and incomplete lineage. This impacts everything from troubleshooting to compliance, making it a universal challenge for data teams.

---

## How Meta Solved It

Meta developed a comprehensive lineage solution integrated into their PAI to tackle their challenges. The Policy Zone Manager (PZM) is central to this effort. This tool builds on lineage data, enabling developers to trace data flows and implement privacy controls efficiently.

The solution has the following steps.

### **Collecting data flow signals** from many data activities

1. **Meta discovers data flows** **for the** **web system** activities by employing static and runtime analysis tools. It focuses on sensitive data, such as religious views. For instance, when users input data on the app, this data is transmitted to a web endpoint, written in the logging table, and stored in a database.

   Static analysis tools simulate code execution to map out potential data flows. Data at Meta can flow through stacks of function calls in different programming languages, such as C++ or Python, from web systems to backend services.

   [![](https://substackcdn.com/image/fetch/$s_!QfZu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1eb8237f-4875-4a33-8046-fc4ac25f9dde_1284x668.png)](https://substackcdn.com/image/fetch/$s_!QfZu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1eb8237f-4875-4a33-8046-fc4ac25f9dde_1284x668.png)

   Image created by the author.

   Static code analysis is a debugging method by examining the code without executing the program. In the lineage context, although it doesn't execute the code, static analysis simulates the logical paths a program might take; this simulation helps identify potential data flows, such as data being read from a source (e.g., a form or API endpoint), data being processed or transformed by various functions, data being written to a destination (e.g., a database table or log file)

   However, the static approach is not enough. It does not account for runtime-specific data flows, such as conditional logic based on user input.

   Meta collects real-time signals during request execution. It captures and compares payloads at source and sink points, categorizing data flow evidence into match sets (high-confidence matches) and complete sets (broader potential matches for human review).

   [![](https://substackcdn.com/image/fetch/$s_!KObj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0886fa36-c6a4-4d18-b5cd-3ef9e9c8e080_676x580.png)](https://substackcdn.com/image/fetch/$s_!KObj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0886fa36-c6a4-4d18-b5cd-3ef9e9c8e080_676x580.png)

   Image created by the author.

   For example, Meta collects two payloads from a source and a sink. The source payload is {“data”: “Buddhist”} and . the sink payload is {“data”: “Buddhist” “event\_timestamp“: “00:00:00“}, Meta sees this data likely flow from this source and sink.

   However, if the sink payload represents a “more compacted and abstracted” value such as {“religion\_count“: 1}, Meta is not sure if this data flows from the source to this sink. In such cases, Meta requires humans to review the flow result.

   Unfortunately, Meta doesn’t share detailed rules for defining the confidence level for a flow result.
2. **For the data warehousing activities**, they combine runtime instrumentation with static analysis of SQL queries (from tools like Presto and Spark). Contextual runtime information, such as job IDs, helps fill gaps where static analysis might miss connections.
3. **For AI systems**, lineage tracking involves tracking relationships between datasets, models, and workflows. These systems construct detailed lineage graphs by integrating runtime signals from libraries like PyTorch and workflow engines like FBLearner Flow.

### **Identifying Relevant Data Flows**

After building comprehensive lineage graphs, Meta needed a way to focus on specific data flows, like those involving religious views.

They developed an iterative analysis tool that allows developers to filter and refine these graphs efficiently. This tool uses a process of discovery, exclusion, and iteration to identify the most relevant flows.

### How It Helps

The result? Developers can now confidently trace granular data flows and implement privacy controls quickly. This has significantly reduced the time and effort required to ensure compliance while maintaining Meta’s commitment to user privacy.

---

## Lessons We Can Learn

[![](https://substackcdn.com/image/fetch/$s_!AF4d!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea76604b-abc4-4633-b2ce-7c87c41750d9_548x540.png)](https://substackcdn.com/image/fetch/$s_!AF4d!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea76604b-abc4-4633-b2ce-7c87c41750d9_548x540.png)

Image created by the author.

### Start Thinking About Data Lineage Early

I believe data lineage isn’t just for large companies. Even smaller teams can benefit from building lineage into their processes early. As your data ecosystem grows, having this foundation will save countless hours of debugging and compliance headaches.

### Implementing the data linage

If you’re not working at Meta’s scale, start small. Tools like dbt lineage or metadata platforms like DataHub offer a solid foundation. If these tools fall short, consider Meta’s approach of embedding tracking logic into the code. Just remember, starting simple and iterating gradually will always outperform building a complex system that doesn’t fit your organization.

### Lineage Graphs Alone Aren’t Enough

Meta’s case study also highlights an important point:

Simply having a lineage graph isn’t enough. You need tools that empower end-users to interact with and extract actionable insights from these graphs.

Start by leveraging existing interfaces from tools like dbt documentation or DataHub UI/API. Use these as a foundation to gather user feedback and iteratively enhance or customize solutions. This iterative approach ensures the tools meet user needs effectively, maximizing the value of your lineage data.

### Measure and Iterate

Data lineage, like any engineering effort, benefits from continuous improvement. Regularly measure the effectiveness of your lineage tools and processes, and iterate based on feedback.

---

## Outro

Above are my notes after learning how Meta does data lineage at a mega scale.

Meta’s journey with data lineage offers efficient ways to tackle complex challenges with innovative solutions. From scalable data flow collection to user-friendly tools, their approach provides valuable lessons for teams of all sizes.

As you reflect on these insights, consider how your organization handles data lineage. Are there gaps you can address? Tools you can adopt? Starting today can lead you to smoother operations and stronger compliance.

I’d love to hear from you if this has sparked ideas or questions.

---

## Reference

*[1] Facebook Engineering Blog, [How Meta discovers data flows via lineage at scale](https://engineering.fb.com/2025/01/22/security/how-meta-discovers-data-flows-via-lineage-at-scale/) (2025)*
