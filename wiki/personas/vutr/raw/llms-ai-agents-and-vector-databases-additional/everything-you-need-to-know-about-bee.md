---
title: "Everything you need to know about LLMs"
channel: vutr
author: "Vu Trinh"
published: 2025-12-16
url: https://vutr.substack.com/p/everything-you-need-to-know-about-bee
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Data Quality"]
tags: [https, auto, substackcdn, image, fetch, good]
---

# Everything you need to know about LLMs

*...as a data engineer*

> Source: [Open post](https://vutr.substack.com/p/everything-you-need-to-know-about-bee)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[data-quality|Data Quality]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=181653873)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!h4Du!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37caca32-e713-478a-a324-d4d39fc6c8c6_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!h4Du!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37caca32-e713-478a-a324-d4d39fc6c8c6_2000x1428.png)

---

> *This article is validated and reviewed by my data science colleague**, [Tran Bao Son](https://www.linkedin.com/in/son-tran-bao/).***

# Intro

ChatGPT was first introduced in 2022.

Since then, the world has changed forever.

The rise of tools built on Large Language Models (LLMs), a branch of deep learning, such as ChatGPT, Gemini, Claude, Grok, and Cursor, has transformed how we communicate with machines and solve problems. People don’t read books or papers page by page as often, we use Google less, and we write code with fewer programming syntax details.

[![](https://substackcdn.com/image/fetch/$s_!sM-i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf96e2cf-e94c-4093-8ae5-3fd81624bc14_954x568.png)](https://substackcdn.com/image/fetch/$s_!sM-i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf96e2cf-e94c-4093-8ae5-3fd81624bc14_954x568.png)

We chat with them.

Just input what you need in human language, and you will get what you want.

That’s powerful because it saves time, a lot of time.

And time is the most valuable resource in the world. Companies know that. They need faster time-to-market and more agility to adapt to market changes.

They hope to leverage LLMs in their original form from the internet (e.g., using Cursor to boost developer productivity) or to customize them to suit their needs (e.g., to act as salespersons).

This is where companies need us, the data engineers, because the foundation of any LLM (or any AI model) is data. Our customers are no longer business users; we now need to collect, store, and serve data for AI models.

To work effectively, understanding the end users is essential. What can LLMs do? What are their limitations? What data do they need? What does quality data look like to them? And much more. In this article, I will do my best to explain what data engineers need to know about LLMs.

# What you will expect

Since the target audience is data engineers, this article won’t explain every detail of how LLMs work, especially the underlying mathematics.

[![](https://substackcdn.com/image/fetch/$s_!WVGI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a18bb86-1e69-442f-8b69-49278f6ebb84_1210x446.png)](https://substackcdn.com/image/fetch/$s_!WVGI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a18bb86-1e69-442f-8b69-49278f6ebb84_1210x446.png)

You won’t see any math equations here simply because I don’t understand them. What you can expect is an explanation of the relationship between LLMs and AI, machine learning, and deep learning; whether LLMs are simply the result of a few years of breakthroughs; what the input data looks like; and how LLMs generate their output.

If you want a deeper dive, here are two articles I recommend:

* [An Intuitive Guide to How LLMs Work](https://www.jlowin.dev/blog/an-intuitive-guide-to-how-llms-work)
* [How Large Language Models work](https://medium.com/data-science-at-microsoft/how-large-language-models-work-91c362f5b78f)

# What are LLMs?

## AI, ML, DL, LLM?

First, let’s try to understand where LLMs fit.

At the broadest level, Artificial Intelligence (AI) is the field of computer science dedicated to creating systems that simulate human intelligence.

Machine Learning (ML) is a subfield of AI.

In traditional programming, a human defines the logic that processes data to produce an output. In Machine Learning, the human provides the system with input data and the desired output, and the machine derives the algorithm (the logic) needed to link the two.

ML models are tasked with recognizing patterns.

[![](https://substackcdn.com/image/fetch/$s_!ffDp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10be7da8-1b88-4ca2-948a-94540cd01a58_718x574.png)](https://substackcdn.com/image/fetch/$s_!ffDp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10be7da8-1b88-4ca2-948a-94540cd01a58_718x574.png)

Within ML, Deep Learning (DL) shifts the focus toward unstructured data such as videos, text, images, and audio. It leverages Artificial Neural Networks (ANNs), architectures inspired by the structure of the human brain, to automatically discover patterns in data.

Finally, we come to LLM, part of the Deep Learning category.

It is a deep learning model that generates the next text sequence based on statistical patterns learned from its training data. In simple words, LLM is trying to predict the next token of a sentence like this: “Batman is driving \_\_.”

> ***Note**: For the sake of this article, we can think of tokens as words.*

## Probability Distribution

Essentially, LLMs don’t know about facts; they are probability distributions of language.

They do not “know” that Ha Noi is the capital of Vietnam. Instead, they have learned from analyzing billions of sentences that when the sequence “The capital of Vietnam is...” appears, the word with the “highest chance” to be the correct one is “Hanoi.”

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=181653873)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

Before we continue, let’s slow it down a bit and revisit one of the most important statistical concepts in how LLMs work: the probability distribution.

Imagine a loaded die.

A standard die has six sides, each with an equal chance (16.6%) of landing. We can say that each time we throw a die, each side has a 16.6% chance of appearing. The distribution, the map of how likely different outcomes of throwing a dice will look like this:

[![](https://substackcdn.com/image/fetch/$s_!Md5K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa313466c-9a72-403d-9076-7bfafd40bdee_892x506.png)](https://substackcdn.com/image/fetch/$s_!Md5K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa313466c-9a72-403d-9076-7bfafd40bdee_892x506.png)

As each outcome has the same chance of happening, we say that throwing a die has a uniform probability distribution. In real life, we usually don’t have many models that are uniformly distributed.

For example, in a population, the distribution of heights or ages is not uniform; if you pick a random person, the probability that they are 7 years old versus 56 years old differs. One of the most well-known ones is the normal distribution, which is visualized as a bell curve; the highest point of the curve represents the average value, and outcomes closer to it are more likely.

[![](https://substackcdn.com/image/fetch/$s_!7GgK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb971a0bf-6db1-4313-8a60-4eadbd6e80a7_846x570.png)](https://substackcdn.com/image/fetch/$s_!7GgK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb971a0bf-6db1-4313-8a60-4eadbd6e80a7_846x570.png)

Given a normal distribution of ages in an imaginary country with an average of 37, selecting a random person and asking for their age would most likely yield an age close to 37.

However, this might not entirely reflect reality, as real-world observations often depend on additional conditions. What if I want to model only women’s ages in that country, or only football players’?

This is where **conditional probability distributions** become useful.

[![](https://substackcdn.com/image/fetch/$s_!ZNac!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46048d2d-17be-4ad2-ba10-4565269d900a_1522x1026.png)](https://substackcdn.com/image/fetch/$s_!ZNac!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46048d2d-17be-4ad2-ba10-4565269d900a_1522x1026.png)

They describe the probability of an event occurring given that another event has already occurred (e.g., the probability of selecting **a man** who is 42 years old). In essence, a conditional probability distribution focuses your attention on a **subset** of the sample space in which the conditioning event, the event that has already occurred, is true.

## LLM, a probabilistic engine.

Now, back to LLMs.

They essentially work by examining word distributions (we just need to know that it is feasible to model word distributions). Conditional distributions are also used here, but the conditions are not simple categories like male/female or football player/non-football player. Instead, the probability of a word depends on many factors, such as the preceding context.

In brief, to generate a sentence, an LLM starts with an initial context (which may be derived from user input, such as a chat message). It then forms the conditional probability distribution for the next word. It “picks” a word from this distribution, adds it to the current context, and repeats the process.

[![](https://substackcdn.com/image/fetch/$s_!Oxgl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94ea4866-b9b8-49a6-a400-8465a00636b8_900x542.png)](https://substackcdn.com/image/fetch/$s_!Oxgl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94ea4866-b9b8-49a6-a400-8465a00636b8_900x542.png)

Each time the model “**picks”** the next word, there’s a high chance that different words will be chosen because it relies on a probability distribution. This explains why you get non-deterministic answers when you ask the model the same question more than once.

That’s it.

There are improved mechanisms and state-of-the-art techniques that make modern LLMs as powerful as they are today, but the core mechanism behind how they work is fundamentally based on a previously discussed architecture.

## Are LLMs the breakthrough in the 2020s?

The introduction of ChatGPT in 2022 often leads people (who do not work in AI fields) to believe that LLMs are just a breakthrough of the 2020s.

[![](https://substackcdn.com/image/fetch/$s_!8jQv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc977fe95-9834-4c99-8bd1-a519fc7d449d_972x366.png)](https://substackcdn.com/image/fetch/$s_!8jQv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc977fe95-9834-4c99-8bd1-a519fc7d449d_972x366.png)

It’s a compounding process that lasts over many decades.

In the past, AI models (more specifically, the RNN-based models) processed language like a human memorizing a book, reading it one word at a time in strict order.

> A Recurrent Neural Network (RNN) is a type of neural network designed to handle sequential data; it processes information in which the current input depends on previous ones.

Imagine you are reading a very long sentence:

> “The red fox, who had been hiding in the bushes all morning because he was afraid of the dog, finally jumped over the big dog.”

The AI had to read “The,” then “red,” then “fox,” and so on. It couldn’t easily skip ahead or look back. This was slow. By the time the AI got to the end of the sentence (the “dog”), it had often “forgotten” the beginning (the “fox”). It struggled to understand that the fox was the one jumping. It lost the context.

[![](https://substackcdn.com/image/fetch/$s_!z-bj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e0c346a-0175-49c7-b75d-1bbbbe33a8c0_882x408.png)](https://substackcdn.com/image/fetch/$s_!z-bj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e0c346a-0175-49c7-b75d-1bbbbe33a8c0_882x408.png)

Because these models had to process data one step at a time, you couldn’t make them very big. Training a huge model would take a lot of time.

In 2017, [a team at Google introduced the Transformer.](https://arxiv.org/abs/1706.03762)

This changed everything because Transformers replaced sequential processing with self-attention, enabling the model to consider all tokens in a sequence at once during training.

[![](https://substackcdn.com/image/fetch/$s_!ekba!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8dbabd87-840c-47d8-9f53-17bd5cc80fad_936x474.png)](https://substackcdn.com/image/fetch/$s_!ekba!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8dbabd87-840c-47d8-9f53-17bd5cc80fad_936x474.png)

> In the spirit of this article, I won’t dive into how Transformers work here. Even if I wanted to, I couldn’t. :D

The Transformer introduced two things that fix the old problems.

### **Attention**

Attention enables the AI to understand context and relationships of words, not just proximity. It allows the model to weigh the significance of different parts of the input independently of their position. Given a sentence:

“The dog didn’t cross the street because **it** was too tired.”

To a human, it’s obvious that “it” refers to the dog, not the street. However, with the AI models, that is a different story:

[![](https://substackcdn.com/image/fetch/$s_!O4G6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b04c6c1-d67a-4862-ba09-fbfa5df63be9_1274x604.png)](https://substackcdn.com/image/fetch/$s_!O4G6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b04c6c1-d67a-4862-ba09-fbfa5df63be9_1274x604.png)

* **Without Attention:** The AI sees “it” and looks at the nearest word, “street.” It might mistakenly associate the “it” with “street.”
* **With Attention**: When the model processes the word “it,” it scans the whole sentence. It sees the word “tired.” It knows from its training that dogs get tired, but *streets* do not.

This is only a very simple explanation of attention; the mechanism is much more complicated in reality. The key point to note is that attention can model relationships between words regardless of their distance.

### Parallel Processing

While other approaches process data sequentially, Transformers “digest” the entire sequence at once, enabling parallel data processing. This means Transformers train faster and use hardware resources more efficiently (e.g., GPUs, TPUs).

[![](https://substackcdn.com/image/fetch/$s_!vbxb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdcb9d879-1b94-4078-a117-121c75ab0dd7_1350x626.png)](https://substackcdn.com/image/fetch/$s_!vbxb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdcb9d879-1b94-4078-a117-121c75ab0dd7_1350x626.png)

The actual mechanisms that enable Transformers to process data in parallel are more complex; this is only a high-level idea. This advantage comes at a cost: Transformers introduce significant computational and memory overhead, particularly in the self-attention mechanism, and are often deployed with huge parameter counts.

# How does an organization leverage LLMs?

In this article, we will not discuss how LLMs can improve productivity through existing applications such as ChatGPT, Gemini, Cursor, or Copilot; instead, we will focus on how organizations customize LLMs to meet their needs.

Before discussing that, we must first understand how LLMs are trained.

They’re first pre-trained, which is the most computationally expensive and time-consuming phase. LLMs are fed massive amounts of data to develop broad, general-purpose understanding capabilities. This is practical because Transformer architectures are faster to train and more hardware-efficient. OpenAI and Google literally feed their models with data from the whole internet.

[![](https://substackcdn.com/image/fetch/$s_!o0VP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb30ac8a-9481-4306-a748-19d02cae90c4_1080x672.png)](https://substackcdn.com/image/fetch/$s_!o0VP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb30ac8a-9481-4306-a748-19d02cae90c4_1080x672.png)

The result of the pre-training process is the base models (a giant autocomplete machine).

The next phase is fine-tuning, in which a base model is further trained on a more specific dataset. This dataset is much smaller than the pre-training dataset. The goal is to enable the model to perform better on specific tasks and follow instructions.

[![](https://substackcdn.com/image/fetch/$s_!DdUl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6045d323-b58c-44ad-acf5-9eb7a8be5d95_1212x442.png)](https://substackcdn.com/image/fetch/$s_!DdUl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6045d323-b58c-44ad-acf5-9eb7a8be5d95_1212x442.png)

There is a final stage called Reinforcement Learning from Human Feedback (RLHF). This stage aligns the model with complex human values or safety guidelines (e.g., how ChatGPT answers you politely).

To meet an organization’s needs, AI engineers can leverage a pre-trained model and adapt it through fine-tuning, in some cases, RLHF, to improve performance on specific tasks.

[![](https://substackcdn.com/image/fetch/$s_!46c_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda5fcdd7-09b8-438b-a070-4085701b5c2c_1186x332.png)](https://substackcdn.com/image/fetch/$s_!46c_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda5fcdd7-09b8-438b-a070-4085701b5c2c_1186x332.png)

This process also involves a data engineer, as we need to collect, store, and provide the data for training. This is very important as the quality of the input dataset will determine the reliability and behavior of the resulting model.

> *How the data pipeline will change when we try to serve the LLM model, as well as ensuring the quality of the training data, will be discussed in a different article.*

# RAG

While fine-tuning is great for modifying a model’s behavior for a specific task, it is inefficient for teaching a model new, rapidly changing facts. However, fine-tuning relies on the training process, which is time-consuming and highly dependent on the quality of the input data.

> If you’re a data engineer, you will know that ensuring data quality is one of the most challenging tasks.

Traditionally, LLMs rely entirely on their internal “memory,” which is the data they absorb during training. It’s similar to studying for an exam: if the questions fall within the material you prepared, you can answer them. However, if you studied chapters 1 through 8 and the exam asks about chapter 9, you will fail. Likewise, if a model was trained on data from two years ago and you ask for a recent fact, it will produce an incorrect result.

[![](https://substackcdn.com/image/fetch/$s_!YCNe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70d57625-7b7a-427d-a77d-8af573b0a6c2_988x292.png)](https://substackcdn.com/image/fetch/$s_!YCNe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70d57625-7b7a-427d-a77d-8af573b0a6c2_988x292.png)

Retrieval-Augmented Generation (RAG) fundamentally changes that dynamic.

It’s like being allowed to ‘cheat’ on an exam; you can use an open book or even search online. When a user asks a question, the AI can consult a ‘library’ (which could be a document, a blog, or a database) and retrieve the relevant information to answer it. The model doesn’t need to memorize the facts; it only needs to know how to consume and synthesize the retrieved information.

[![](https://substackcdn.com/image/fetch/$s_!If0V!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17e4e9c9-a7e0-46ea-b9bc-702ff692d5da_846x616.png)](https://substackcdn.com/image/fetch/$s_!If0V!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17e4e9c9-a7e0-46ea-b9bc-702ff692d5da_846x616.png)

To enable RAG to work, organizations must also prepare the input data for the LLM to consume. The pipeline may need to operate on continuous data with low latency (real-time processing) to reflect real-world changes in the input data. As mentioned in the fine-tuning, how the data pipeline will change when we try to serve the LLM model will be discussed in a different article.

[![](https://substackcdn.com/image/fetch/$s_!NqTz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15502338-8322-4a6f-b11d-bf0476e5791c_1184x314.png)](https://substackcdn.com/image/fetch/$s_!NqTz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15502338-8322-4a6f-b11d-bf0476e5791c_1184x314.png)

One more thing: choosing between fine-tuning and RAG is not a binary decision. As data engineers, we rarely know which approach is best for an organization’s needs because it depends on many factors. The decision should be made by those who are more proficient in the field, such as AI/ML engineers or data scientists.

In practice, many systems combine both approaches: fine-tuning to shape model behavior and RAG to provide fresh, domain-specific knowledge.

# Outro

One aspect you might think I missed is how LLMs reason. I planned to include it, but during my research, I found that the topic is complex and difficult to explain without deeper domain knowledge. So I think it’s fine to stop at understanding that reasoning ability is essentially about answering a question by breaking the problem into multiple stages.

—

In this article, I’ve done my best to present the LLM knowledge I believe we, as data engineers, should be equipped with to better understand our “new customer” in this era. I covered where LLMs fit within AI, ML, and DL; explored them through the lens of simple statistics; explained how they became practical with the introduction of Transformers; described their training process; and discussed how organizations can customize them through fine-tuning or RAG.

Thank you for reading this far. If you’d like to see more articles on AI knowledge, specifically those relevant to data engineering, please let me know.

# Reference

[1] Andreas Stöffelbauer, [How Large Language Models Work](https://medium.com/data-science-at-microsoft/how-large-language-models-work-91c362f5b78f), 2024

[2] Jeremiah Lowin, [An Intuitive Guide to How LLMs Work](https://www.jlowin.dev/blog/an-intuitive-guide-to-how-llms-work), 2024
