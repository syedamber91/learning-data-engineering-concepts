---
title: "My DS colleague spent a year studying AI agents. Here’s everything you should know."
channel: vutr
author: "Vu Trinh"
published: 2026-02-24
url: https://vutr.substack.com/p/my-ds-colleague-spent-one-year-learning
paid: true
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "BigQuery", "Orchestration"]
tags: [https, auto, agent, media, substackcdn, image]
---

# My DS colleague spent a year studying AI agents. Here’s everything you should know.

*A 10-minute explanation of the hottest technology in 2026.*

> Source: [Open post](https://vutr.substack.com/p/my-ds-colleague-spent-one-year-learning)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[bigquery|BigQuery]] · [[orchestration|Orchestration]]

---

> **🚨** I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!Igde!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F940d01bf-03df-42bb-a458-1764a8f7bdc2_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!Igde!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F940d01bf-03df-42bb-a458-1764a8f7bdc2_2000x1429.png)

---

# Intro

People are trying to offload as much of the human workflow as possible to agents, from answering customer questions and posting on social media to coding a shiny web application (even if you don’t know anything about HTML and JavaScript).

Fascinated by the power of the AI agent, I tried to dive deep into it to understand what's behind the scenes (just like I did with Spark, BigQuery, Kafka, and open table formats).

The more I researched, the more I feel this topic should be delivered by someone with experience building an agent workflow. So, I asked my DS colleague, Son Tran, to help me with this article.

At the end of this article, Son and I hope you guys have a high-level understanding of what an Agent is and what it can do, so that we can use, build, and maintain it better, not only as a data engineer but also as a human.

> ***Note 1**: All the technical details in this article are from Son alone. I only help make the delivery more user-friendly for blog readers by editing the draft and creating illustrations. That means from this moment, when you see “I” in the article, it’s Son.*
>
> ***Note 2**: If you guys prefer reading an article about AI like this, please let us know by dropping a like or a comment.*

We’ll start by breaking down the Anatomy of an Agent.

Then, we’ll walk through the Agentic Problem-Solving Process. I’ll explain what an agent does from the moment it receives a request until it delivers a result.

Finally, we’ll look at Five Levels of Agents. This framework helps us categorize everything from simple bots to fully autonomous systems, so you know exactly what level of complexity your project actually needs.

---

# The Anatomy of an AI Agent

Before we go deep on AI Agents, let’s define what they actually are.

Simply said, an agent is just a Language Model in a loop with the tools it needs to get a job done.

I like to think of it as a complete, goal-oriented system: the Brain (the reasoning model), the Hands (the tools), and the Nervous System (the orchestration layer) all work together to achieve an outcome.

## Model

> The Brain

In an agentic system, the Large Language Model (*LLM*) is the central reasoning engine. It’s the “Brain” that processes information and decides what to do next.

[![](https://substackcdn.com/image/fetch/$s_!_Mt9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1e7d388-009c-47d5-bb1e-e5d88a1067e3_520x584.png)](https://substackcdn.com/image/fetch/$s_!_Mt9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1e7d388-009c-47d5-bb1e-e5d88a1067e3_520x584.png)

> *Vu Trinh: You can read more about LLM from my previous article [here](https://open.substack.com/pub/vutr/p/everything-you-need-to-know-about-bee?utm_campaign=post-expanded-share&utm_medium=web), which was also reviewed by Son.*

The key here is which LLM to use? It is actually a trade-off among cognitive capacity, operating cost, and speed. In practice, model selection should not be determined by online benchmarks. Instead, it should focus on task-specific performance.

[![](https://substackcdn.com/image/fetch/$s_!mF0t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc98abb7a-e6c1-4241-b6ea-e18d11db27fb_1014x678.png)](https://substackcdn.com/image/fetch/$s_!mF0t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc98abb7a-e6c1-4241-b6ea-e18d11db27fb_1014x678.png)

I recommend evaluating models against metrics that map directly to your business outcomes. For instance, when I test LLM capacity for a component of the Text2SQL feature, it is surprising that Gemini Flash matched the performance of other frontier models while operating at a much lower cost and at a much faster pace.

[![](https://substackcdn.com/image/fetch/$s_!Od95!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9f68f1a-5c32-4578-bfdd-b07f449d8f91_1032x352.png)](https://substackcdn.com/image/fetch/$s_!Od95!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9f68f1a-5c32-4578-bfdd-b07f449d8f91_1032x352.png)

You don’t always need the most expensive model for every single turn of a conversation. One strategy for optimizing performance and cost is Model Routing. In simple terms, the strategy uses frontier models for complex planning and routes simpler tasks to faster, cheaper models.

[![](https://substackcdn.com/image/fetch/$s_!NHYC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9157b84f-c804-41c3-9281-1db7709d2d0e_1152x720.png)](https://substackcdn.com/image/fetch/$s_!NHYC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9157b84f-c804-41c3-9281-1db7709d2d0e_1152x720.png)

One final note: the “model of the year” usually keeps the title for only six months. If your AI strategy is “set it and forget it,” you’re already falling behind.

Constantly tests new models against your actual business goals and makes upgrades (with the help of Agent Ops). This lets you swap in a better “brain” whenever one hits the market, ensuring your system stays fast and smart without breaking your architecture.

## Tools

> The Hands

If the brain of an AI agent is the language model, the Tools are its hands. Without them, your Agent can only ‘talk’.

While a standard language model is limited to its training data, an agentic system uses tools such as API extensions, code functions, and databases to retrieve real-time information and execute actions.

[![](https://substackcdn.com/image/fetch/$s_!0ksV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6462e4dd-8c5a-455c-8bf9-174582b80b76_1088x556.png)](https://substackcdn.com/image/fetch/$s_!0ksV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6462e4dd-8c5a-455c-8bf9-174582b80b76_1088x556.png)

To be effective, an AI agent needs two primary capabilities: knowing the right information and acting on it. So the common AI Agent tools are Retrieving Information and Executing Actions.

> **🚨**I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

### Retrieving Information

Because models are frozen at a specific “knowledge cutoff” date, they need tools to access the world in real-time. The goal here is accuracy: minimizing hallucinations (where models confidently lie, making you believe it’s correct) and ensuring the agent stays up to date. Here are the two foundational tools that make that possible:

* RAG (Retrieval-Augmented Generation): Think of this as your agent’s library card. It allows the AI to query external knowledge—like your company docs, a vector database, or a knowledge graph

  [![](https://substackcdn.com/image/fetch/$s_!If0V!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17e4e9c9-a7e0-46ea-b9bc-702ff692d5da_846x616.png)](https://substackcdn.com/image/fetch/$s_!If0V!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17e4e9c9-a7e0-46ea-b9bc-702ff692d5da_846x616.png)

* NL2SQL: This tool bridges the gap between human language and structured data. It allows an agent to “talk” to a database to answer analytical questions like, *“What were our top-selling products last quarter?”*

By forcing an agent to “fact-check” before it generates an outcome, you ground its responses in reality and reduce the risk of hallucinations.

### Executing Actions

It allows the AI to trigger workflows and impact external systems.

[![](https://substackcdn.com/image/fetch/$s_!itoq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbce0880-6aad-48e9-a39b-7e1e23f7bd56_448x628.png)](https://substackcdn.com/image/fetch/$s_!itoq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbce0880-6aad-48e9-a39b-7e1e23f7bd56_448x628.png)

* API Wrappers: These enable the agent to bridge the gap between text and action, allowing it to send emails, update CRMs, schedule meetings, or publish social media posts.
* Code Execution: By running Python or SQL, the agent can solve complex mathematical problems or perform data analysis that is too difficult for a language model to do through text alone.
* Human-in-the-Loop (HITL): A safety layer where the agent pauses for a “nod” from a human before performing high-stakes actions.

## The Orchestration Layer

> Nervous System

While the model serves as the “brain” and the tools as the “hands,” the orchestration layer serves as the “nervous system,” coordinating everything.

[![](https://substackcdn.com/image/fetch/$s_!2N-4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19ec02ef-35e0-4dd1-9107-1690e9b205a6_1246x712.png)](https://substackcdn.com/image/fetch/$s_!2N-4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19ec02ef-35e0-4dd1-9107-1690e9b205a6_1246x712.png)

It is the governing process that keeps everything running. This is the place where a developer’s carefully crafted logic comes to life. It determines when the model engages in reasoning, triggers specific tool executions, and integrates those outputs to guide the next phase of the workflow.

Here is how it works:

* Smart Planning: It breaks complex goals into small, manageable steps using prompt engineering like [\*\*Chain-of-Thought](https://arxiv.org/pdf/2201.11903).\*\*
* Memory Management: It gives agents the power to “remember” previous steps and stay on track.
* Tool Control: It decides exactly when to stop and think versus when to use a tool using the [ReAct](https://arxiv.org/abs/2210.03629) framework.

### Core Design Choices

The first decision you’ll face when building this layer is how much freedom your agent should have. There isn’t always a “right” answer. You have two main choices: a deterministic, predictable workflow or an agent that can dynamically adapt, plan, and execute tasks to achieve a goal.

[![](https://substackcdn.com/image/fetch/$s_!d1sP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5fbbf5e-17b2-4661-bd49-cb53c19698bb_1290x370.png)](https://substackcdn.com/image/fetch/$s_!d1sP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5fbbf5e-17b2-4661-bd49-cb53c19698bb_1290x370.png)

The second decision you’ll have to make is the implementation method: No-code or code first. For rapid automation of standard tasks, no-code builders allow business users to lead the way. For sophisticated, mission-critical applications, code-first tools like Google’s ADK/LangGraph give developers the power and flexibility required to build highly customized, integrated solutions.

### Instruct with Domain Knowledge and Persona

[![](https://substackcdn.com/image/fetch/$s_!lk3k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F059dc786-8aeb-4b41-b2e5-ee974630c63d_948x930.png)](https://substackcdn.com/image/fetch/$s_!lk3k!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F059dc786-8aeb-4b41-b2e5-ee974630c63d_948x930.png)

An agent needs a personality and a set of rules. This is its system prompt. The prompt will give it a persona, telling it who it is, what its tone should be, and exactly when it should use its tools.

### Augment with Context

AI agents need memory to stay on track. This memory is loaded into the “context window” whenever the agent is working.

There are two main types:

[![](https://substackcdn.com/image/fetch/$s_!jN8b!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa224c39c-17da-452e-b553-fc98a93d3798_906x746.png)](https://substackcdn.com/image/fetch/$s_!jN8b!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa224c39c-17da-452e-b553-fc98a93d3798_906x746.png)

* Short-Term Memory, this is for the here and now.

  + It tracks your current conversation.
  + It remembers every action the agent just took.
  + It records what the agent saw.
  + This helps the model decide its very next step.
  + Developers often call this “state,” “sessions,” or “threads.”
* Long-Term Memory: this stays with the agent across different sessions.

  + It helps the agent remember your preferences from weeks ago.
  + It acts like a search engine for the agent’s own history.
  + Technically, this is usually a RAG system or a vector database.
  + This is what makes an AI feel personalized and continuous.

### Multi-Agent Systems and Design Patterns

Building a single “agent” to handle everything is often a mistake. It becomes too complex and slow.

Instead, use a team of specialists. This mirrors a real human organization. You break a big process into small tasks. Then assign each task to a dedicated agent. This makes agents easier to build, test, and maintain.

Common Design Patterns to organize these teams:

* **The Coordinator** (The Manager): One agent acts as the boss. It analyzes the request and splits it up. It sends work to specialists—like a researcher or a coder—and then combines their answers.

  [![](https://substackcdn.com/image/fetch/$s_!4VUn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa7f6909f-ce1f-41f7-bea4-8fd4fa55bdac_670x384.png)](https://substackcdn.com/image/fetch/$s_!4VUn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa7f6909f-ce1f-41f7-bea4-8fd4fa55bdac_670x384.png)

* **Sequential**: This is for linear work. The output of the first agent becomes the input for the next.

  [![](https://substackcdn.com/image/fetch/$s_!L-Gx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85bd299e-5168-4f02-8b6b-5b12086e7c1d_1024x256.png)](https://substackcdn.com/image/fetch/$s_!L-Gx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85bd299e-5168-4f02-8b6b-5b12086e7c1d_1024x256.png)

* **Iterative Refinement** (The Quality Loop): One agent creates the content. A second “critic” agent reviews it. They go back and forth until the work is perfect.

  [![](https://substackcdn.com/image/fetch/$s_!acsn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ded1582-d79c-41d3-8307-41f50f6c9c2d_800x602.png)](https://substackcdn.com/image/fetch/$s_!acsn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ded1582-d79c-41d3-8307-41f50f6c9c2d_800x602.png)

* **Human-in-the-Loop** (The Safety Check): For high-stakes tasks, the agent pauses. It asks a person for approval before taking a big action.

  [![](https://substackcdn.com/image/fetch/$s_!sJ6_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f76fc78-13e2-486e-897d-1b61f47e5e74_760x276.png)](https://substackcdn.com/image/fetch/$s_!sJ6_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f76fc78-13e2-486e-897d-1b61f47e5e74_760x276.png)

---

# How Agents Think

[![](https://substackcdn.com/image/fetch/$s_!IJ-_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ccb1e3f-c3f0-4cd6-881c-b3b7a362ce7d_902x596.png)](https://substackcdn.com/image/fetch/$s_!IJ-_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ccb1e3f-c3f0-4cd6-881c-b3b7a362ce7d_902x596.png)

When writing code, we write linearly: if this, then that.

But agents are dynamic. Understanding the agent’s problem-solving helps you build systems that actually solve problems without hard-coding every edge case.

Once you look under the hood at how these systems actually solve a problem, it makes a lot of sense.

The agentic problem-solving process has 5 steps.

## Step 1: Get the Mission

Every Agentic Journey starts with a high-level goal, or what we call the Mission. This might come from a user asking to book, the trigger of a high-priority support ticket, or a user request to vibe-coding a web-app

## Step 2: Scan the Scene

Before doing anything, the agent scans its environment to gather Context. It looks at the request, checks its Memory for past interactions, and determines which Tools (such as APIs) are available.

## Step 3: Think It Through

This is the agent’s core “think” loop, driven by the reasoning model (LLM model). The agent analyzes the Mission (Step 1) against the Scene (Step 2) and devises a plan. There will be a Chain of Thought.

## Step 4: Take Action

The orchestration layer now executes the first step of that plan. The agent doesn’t just “chat” anymore; it acts on the world by using its hands: calling an API, running code, or querying a database.

## Step 5: Observe and Iterate

The agent observes the outcome of its action and adds that new info to its context. Then, it loops back to the “Think” step (Step 3) to decide what to do next based on what it just learned.

---

# A Taxonomy of Intelligence

After spending time looking at how AI is currently built, I’ve realized that knowing where your agent sits on the “intelligence ladder” changes everything about how you build it.

## Level 0: The Core Reasoning System

At its simplest form, an agent is just a Large Language Model (LM) sitting in a room by itself.

Here, the LM works alone. It answers using only what it learned during training, without access to the internet, extra tools, or long-term memory. The model has no way of knowing what is happening right now; it is limited entirely to what it learned during its initial training.

## Level 1: The Connected Problem-Solver

At level 1, we give the model “hands” by connecting it to tools such as APIs or databases, providing it the ability to interact with the world. No longer limited to historical training data, the agent uses the Agentic Problem-Solving Process (5-step loop) above to solve real-world problems.

## Level 2: The Strategic Problem-Solver

At Level 2, agents move beyond simple tasks to strategic planning.

This stage introduces context engineering, the ability to intelligently curate and manage specific information required for complex, multi-part goals.

Context engineering boosts agent accuracy by distilling information into a high-quality prompt. This prevents “attention fatigue” and ensures the model performs at its peak.

What is the key point here? You no longer have to hard-code every edge case. You define the “what” (the outcome), and the agent engineers the “how” (the strategy).

## Level 3: The Collaborative Multi-Agent System

In the early days of LLM apps, we all tried to build a single “super-prompt” that could do everything. It was a mess.

If you ask one model to do market research, write code, and draft a press release, it usually gets distracted or starts hallucinating.

At this level, we move to a team of specialists, known as Multi-Agent Systems. The system’s power is in its specialization.

## Level 4: The Self-Evolving System

At this level, the system recognizes what it can’t do and builds its own solutions. Instead of relying on a pre-set toolkit, it creates new tools and agents to solve problems on the fly.

This is the ultimate goal: a system that learns and grows without you having to push a new deployment every time the requirements change.

---

# Outro

I just delivered my understanding of an AI agent, from its anatomy and how it “thinks” to the intelligence ladder. Hope you can learn, use, and build your own AI workflow agents that could actually solve your problem.

We’ve covered a lot of ground, from the Anatomy of an agent (Brain, Hands, and Nervous System) to the 5-step loop of how they actually “think,” and finally, the Intelligence ladder that helps us categorize their complexity.

—

In a world where AI headlines change every week, and new frameworks like MCP (Model Context Protocol) or specialized Agent Skills pop up overnight, it’s easy to feel like you’re falling behind.

However, the tools change, the logic remains.

By understanding the “why” behind the orchestration and the “how” of the reasoning loop, you’ll understand exactly where it fits into the architecture. Whether you are a data engineer looking to automate a pipeline or a curious human trying to stay relevant, mastering these fundamentals helps you build systems that are not just “cool” but truly reliable.

What level of agent are you currently building? Let us know in the comments.

See you in the next articles
