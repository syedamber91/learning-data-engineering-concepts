---
title: "If I could travel back to 5 years ago, what would I talk to myself about Docker?"
channel: vutr
author: "Vu Trinh"
published: 2024-03-09
url: https://vutr.substack.com/p/i-spent-3-hours-to-understand-more
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark"]
tags: [docker, https, image, auto, container, substackcdn]
---

# If I could travel back to 5 years ago, what would I talk to myself about Docker?

*This is a friendly note for someone to begin with Docker plus my Docker cheatsheet.*

> Source: [Open post](https://vutr.substack.com/p/i-spent-3-hours-to-understand-more)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=141885092)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!dIGt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37ba199a-a064-4d0b-97e9-3ce8b77b3a5c_1399x998.png)](https://substackcdn.com/image/fetch/$s_!dIGt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37ba199a-a064-4d0b-97e9-3ce8b77b3a5c_1399x998.png)

Image created by the author.

---

## Intro

I like the time travel theory. As a child, I watched [Terminator](https://en.wikipedia.org/wiki/The_Terminator) or [Back to the Future](https://en.wikipedia.org/wiki/Back_to_the_Future) over and over again. The idea of getting on a weirdo machine so you can return to when you were a child always excites me.

If I could time travel, one of the first things I would do is go back five years to September 23rd, 2019, and give my past self a brief note on [Docker](https://www.docker.com/resources/what-container/#:~:text=A%20Docker%20container%20image%20is,tools%2C%20system%20libraries%20and%20settings.).

That day was my first day with my first “data“ job; I - a know-nothing-just-graduated guy excited for the onboarding, hoping to work around with cool technology like [Spark](https://spark.apache.org/), [Hadoop](https://hadoop.apache.org/), or [Kafka](https://kafka.apache.org/).

But life was not as expected; my first task was to understand and implement a technology I had never heard of - Docker (we were planning a POC then). ***I’ve struggled for two weeks straight***. (In the end, I completed the task quite successfully and obtained one of the most critical skills for my career: working with Docker containers).

To help myself (five years ago) and somebody else begin with the container world more easily, I decided to write a blog post on Docker. I hope it sheds some light.

> *I’m writing this article while believing I can time travel someday.*

---

## Why Docker

> *My biggest mistake was not researching which problem Docker Container solves; I just jumped straight to the implementation and tried to make things run.*

Before going with the “Why question“, let's start with the “What“ first:

> *Docker is a software platform that allows you to build, test, and deploy applications quickly. Docker packages software into standardized units called [containers](https://aws.amazon.com/containers/) with everything the software needs to run, including libraries, system tools, code, and runtime. Using Docker, you can quickly deploy and scale applications into any environment and know your code will run.*
>
> [— source —](https://aws.amazon.com/docker/)

Does the “container” make you think of a [virtual machine](https://www.vmware.com/topics/glossary/content/virtual-machine.html.html#:~:text=A%20Virtual%20Machine%20(VM)%20is,a%20physical%20%E2%80%9Chost%E2%80%9D%20machine.)? If yes, you’re not alone.

Virtual Machine (VM) was born to solve the painful problem for the IT department. Instead of investing in a new server for a new application (which can lead to resource underuse or overuse due to the challenge of predicting the utilization), with a virtual machine, multiple applications can run on the same machine securely and isolatedly.

VM was the game-changer then, but it had some flaws: the VM requested a dedicated [OS system](https://en.wikipedia.org/wiki/Operating_system), and the resources (CPU and RAM) consumed by the OS could otherwise make room for more applications. Moreover, the OS also needs patching and monitoring and requires a license fee, which might be inconvenient for some use cases.

[![](https://substackcdn.com/image/fetch/$s_!2FCI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70f9a2bd-da69-417f-b5fb-e93cb0c35b43_776x487.png)](https://substackcdn.com/image/fetch/$s_!2FCI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70f9a2bd-da69-417f-b5fb-e93cb0c35b43_776x487.png)

Image created by the author. [Reference](https://bi-insider.com/posts/virtual-machines-vs-containers/).

The world needs a more lightweight approach. Container technologies come to the rescue. In the container world, the container is quite similar to the VM. The most significant difference is that containers do not require a dedicated OS: all containers on a host share will share the host’s OS. Users don’t need to care about the CPU and RAM for the OS, the patching and monitoring process, or the license fee.

Despite all the container advances, they remained complex and not so user-friendly. It wasn’t until the Docker was in the town. [Docker, Inc. is the technology company that rebranded in 2013](https://en.wikipedia.org/wiki/Docker,_Inc.) to democratize container technology.

---

## Docker: What is it?

When you hear people mention “Docker”, there is a high chance that they want to refer to the Docker technology, not the Docker, Inc. company. Docker is the software that creates, manages, and orchestrates containers. It’s built from various tools from the [Moby open-source project](https://mobyproject.org/). Docker allows users to focus on applications without caring much about the infrastructure.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=141885092)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

## The Docker architecture

> *A brief*

[![](https://substackcdn.com/image/fetch/$s_!XjxK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bb8cb94-3828-441e-a1fd-ab76cf5e2220_647x284.png)](https://substackcdn.com/image/fetch/$s_!XjxK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bb8cb94-3828-441e-a1fd-ab76cf5e2220_647x284.png)

I created the image on my own based on [the reference](https://docs.docker.com/get-started/overview/#docker-architecture).

Let's check out the Docker architecture first:

* Docker is implemented using a client-server architecture.
* The client communicates to the Docker daemon (`dockerd`). Whenever you run a docker command, for example, `docker run`, the client will send this command to the `dockerd`.
* The client and the daemon can deploy on the same or separate systems. The two communicate using a REST API, over UNIX sockets, or a network interface.
* The Docker daemon is responsible for building, running, and managing the Docker containers.

---

## The Docker registry

A Docker registry is simply the storage of Docker images. The most famous registry is the [Docker Hub](https://hub.docker.com/), which is public, and everyone can use it. However, you can also have your own private registry.

When you run commands like `docker run` or `docker pull`, Docker will look for the image in your desired registry (you can configure this.)

> ***Note**: Don’t worry if you aren’t familiar with the command; we will get to that soon.*

[![](https://substackcdn.com/image/fetch/$s_!6Pqf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b06aa95-4360-443b-b2e8-835045662ae0_2578x1368.png)](https://substackcdn.com/image/fetch/$s_!6Pqf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b06aa95-4360-443b-b2e8-835045662ae0_2578x1368.png)

Screenshot on Apache Spark docker registry. [Source](https://hub.docker.com/_/spark/tags).

---

## The Image

> *The blueprint*

Here is an analogy. When building a house, you need an architect's blueprint to represent how you want your building to look. An image is the blueprint, whereas the application is the house.

An image is a template containing instructions for building a Docker container. You can obtain the image in the two following ways:

* Existed images created by others or on public registries.
* Build your image using `Dockerfile` (A file with a simple syntax that allows you to define the necessary steps to create a Docker image ); you can build the image from scratch or add customization to the existing image. For example, you can build a Python image using Ubuntu with the Python installation instructions in the `Dockerfile`

[![](https://substackcdn.com/image/fetch/$s_!-_b_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2cdd841f-2e23-4252-9de4-2586dc997c47_798x408.png)](https://substackcdn.com/image/fetch/$s_!-_b_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2cdd841f-2e23-4252-9de4-2586dc997c47_798x408.png)

A sample Dockerfile, which uses the base image Ubuntu, copies the current host folder to the docker app folder and runs the Python script. [Source](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/).

Behind the scenes, images contain multiple layers stacked on each other; each layer is roughly translated from each instruction in the `Dockerfile`. When we change the `Dockerfile` and rebuild the image, only those modified layers are rebuilt, which saves us time developing the image.

[![](https://substackcdn.com/image/fetch/$s_!WAGt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01d1793d-7548-4fda-988e-48ee3949636a_455x458.png)](https://substackcdn.com/image/fetch/$s_!WAGt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01d1793d-7548-4fda-988e-48ee3949636a_455x458.png)

Image created by the author.

---

## The container

> *The building*

A container is a runnable instance of an image. Theoretically, you can build multiple houses using the exact blueprint, the container is the same, and you can create more than one container using the same image. Docker containers can be managed using the Docker API or CLI.

[![](https://substackcdn.com/image/fetch/$s_!tTz6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03859b59-35c8-42cd-9ab9-cfea2a8761e2_565x320.png)](https://substackcdn.com/image/fetch/$s_!tTz6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03859b59-35c8-42cd-9ab9-cfea2a8761e2_565x320.png)

Image created by the author.

A more straightforward way to express the relationship between the image and the container:

* You define everything you need to run in the image for your application.
* Then, you create the container that runs your desired application using that image.

The runtime layer handles the container (which has a lower level than the docker engine ). Docker implements a runtime architecture with high-level ([containerd](https://containerd.io/)`)` and lower ([runc](https://github.com/opencontainers/runc)`)`runtime.

* The `containerd` manages the entire container lifecycle, including pulling images and managing `runc` instances. Typically, `containerd` is a long-running process.
* `runc` is the reference implementation of [Open Containers Initiative (OCI)](https://opencontainers.org/) spec. Its job is to start the container by communicating with the underlying OS. Every container was created by an instance of `runc`. Process `runc` exits as soon as the container is started.

[![](https://substackcdn.com/image/fetch/$s_!xZ_W!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa8beff65-3c50-4d70-84e5-a47919214886_625x908.png)](https://substackcdn.com/image/fetch/$s_!xZ_W!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa8beff65-3c50-4d70-84e5-a47919214886_625x908.png)

Image created by the author.

Let checkout the container creation flow to have a better imagination:

* Using Docker CLI to run the container:

  ```
  docker run hello-world
  ```
* Docker client will covert the command into API payload and send the POST request to the Docker daemon.
* Once the Docker daemon receives the request, it contacts `containerd`.
* `containerd` converts the required Docker image into an OCI bundle and tells `runc` to use this image to create a new container.
* `runc` communicates with the OS kernel to assemble the needed constructs to create the container. Right after the container starts, the `runc` will exit.

---

## The docker-compose

Docker also provides docker-compose, a tool for managing multiple container applications. Compose makes your life easier by allowing you to control your entire application stack.

Imagine a scenario like this: you want to deploy an Airflow environment using Docker containers on your laptop. The [Airflow deployment](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html) requires a bunch of components: scheduler, webserver, metadata database, worker, and a Redis instance, each requiring a dedicated container. Docker will help you manage the deployment of the whole Airflow stack; you don’t need separate commands to manage individual containers. Docker composes helps control the application stack through declaration using the [YAML compose file](https://docs.docker.com/compose/compose-file/).

[![](https://substackcdn.com/image/fetch/$s_!vjC3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c2c6450-19e5-44c5-9dd7-7633bcb3f37c_1134x762.png)](https://substackcdn.com/image/fetch/$s_!vjC3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c2c6450-19e5-44c5-9dd7-7633bcb3f37c_1134x762.png)

Image created by the author.

---

## How to get started with Docker

> *Open the terminal and start typing the command.*

The first thing is Docker installation; I will put [the link here](https://docs.docker.com/engine/install/) so you can do it yourself; follow the exact document, and you will get there.

Remember to verify that your docker is already installed:

```
docker --version
```

Now start your first container ever:

```
docker run hello-world
```

* The command will pull the `hello-world` image from the Docker hub.
* After that, it will run the container from the retrieved image.

That’s it. Your first container is up and running. To help you a little bit further, I have created a Docker commands cheat sheet to help you guys with the most common commands. (Although I have nearly five years of working with Docker, I sometimes forget even the most basic ones.)

[![](https://substackcdn.com/image/fetch/$s_!L9Ev!,w_5760,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21896ed5-b4a7-47d8-a6bc-b5fefe3dbc26_1166x821.png)](https://substackcdn.com/image/fetch/$s_!L9Ev!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21896ed5-b4a7-47d8-a6bc-b5fefe3dbc26_1166x821.png)

Image created by the author.

---

## My humble suggestion

> *How do you go to the next step after getting some “Docker“?*

Now, I will suggest some next steps you can consider to level up your Docker skill:

* Build your own [Docker image](https://docs.docker.com/reference/dockerfile/).
* Start a complete [Airflow environment using docker-compose](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/).
* Deep dive into understanding the [docker’s network](https://docs.docker.com/network/) (77% of the Docker bugs I caught are containers that do not see each other.)
* Deep dive into understanding [docker’s volume](https://docs.docker.com/storage/volumes/). (e.g., How to sync two files between your container and your host).
* First taste with [Kubernetes](https://kubernetes.io/docs/concepts/overview/).

---

## Outro

Before I say goodbye, if you follow my work, you know I spent most of the time writing about the knowledge I learned about the OLAP database system; this article is different. It combines my self-research note and a little bit of my memoir. I plan to write more blogs with a similar style, so I hope to get your feedback; e.g., should I put a more personal story into my writing and share more of my experience?

Any feedback or correction from you guys would be really helpful.

Thank you for reading my writing.

Now, it’s time to say goodbye. See you next week.

---

***Reference**:*

* *[Book: Docker Deep Dive - Nigel Poulton - 2023 Edition](https://www.amazon.com/Docker-Deep-Dive-Nigel-Poulton/dp/1916585256)*
* *[Document: Docker overview](https://docs.docker.com/get-started/overview/)*
* *[Document: Docker Engine overview](https://docs.docker.com/engine/)*
* *[Document: Docker Compose overview](https://docs.docker.com/compose/)*

---

## Before you leave

I’m launching a referral program to grow the community by giving you guys valuable gifts whenever you reach a referral milestone. The condition is simple: you refer friends to subscribe to my newsletter, and you will receive a gift based on the number of friends you refer. Here are the reward milestones:

[![](https://substackcdn.com/image/fetch/$s_!lf_-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4c72d52-a2c4-4e24-9714-04e72a4dc087_756x361.png)](https://substackcdn.com/image/fetch/$s_!lf_-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4c72d52-a2c4-4e24-9714-04e72a4dc087_756x361.png)

Now, let’s refer friends and claim exciting rewards ;)

[Refer a friend](https://vutr.substack.com/leaderboard?&referrer_token=1xrjxy&utm_source=post)

---

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/i-spent-3-hours-to-understand-more/comments)

It might take 3 minutes to read, but it took me more than three days to prepare, so it will motivate me greatly if you consider subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
