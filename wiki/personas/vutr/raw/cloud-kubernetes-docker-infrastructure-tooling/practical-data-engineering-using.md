---
title: "Practical Data Engineering using AWS Cloud Technologies"
channel: vutr
author: "Vu Trinh"
published: 2024-07-23
url: https://vutr.substack.com/p/practical-data-engineering-using
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Spark", "Lakehouse", "ETL"]
tags: [step, function, cloud, lambda, https, engineering]
---

# Practical Data Engineering using AWS Cloud Technologies

*Learn how to build end-to-end data engineering projects using pure AWS cloud technologies like S3, SNS, Lambda, Step Function, and more. *

> Source: [Open post](https://vutr.substack.com/p/practical-data-engineering-using)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[lakehouse|Lakehouse]] · [[etl|ETL]]

---

> *Today, we have a special treat for you—a guest post from*  *on building engineering project using AWS cloud technologies. His insights are sure to be valuable, and I hope you enjoy them!*

Thanks for reading VuTrinh.! Subscribe for free to receive new posts and support my work.

---

## Intro

Today, I will share a little more practical approach that anyone can easily implement whether you are new to Data Engineering and want to build side project for fun or you are a professional looking to build scalable solutions, these work for all.

AWS is a popular choice for cloud, and sometimes, I feel that the tech AWS provides is underrated or underused, mainly because of the other hyped tools in the market. We opt for modern tooling for some benefit vs. evaluating the existing cloud ecosystem, which is generally much easier to implement and works seamlessly. This pipeline may not be something you would prefer today. I will provide my answer at the end of the article.

## AWS Cloud Architecture

> *Let’s look into the below components with a simple design that can scale in multiple ways.*

[![Practical Data Engineering using AWS Cloud Technologies](https://substackcdn.com/image/fetch/$s_!mcDn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F79c104d5-f575-4cea-be17-df155febf175_1372x644.png "Practical Data Engineering using AWS Cloud Technologies")](https://substackcdn.com/image/fetch/$s_!mcDn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F79c104d5-f575-4cea-be17-df155febf175_1372x644.png)

Practical Data Engineering using AWS Cloud Technologies

### S3

One of the widely used AWS services is s3. Its object store is used heavily in Data Engineering for storing data as files either directly or through a Lakehouse.

### SNS

SNS is a great service for doing a Fan Out. It's basically a publish-subscribe pattern that works great with multiple downstream AWS services.

* Each SNS can be configured to trigger an S3 event, e.g., when a CSV file drops or when any file drops in the X prefix.
* SNS provides a native filtering mechanism for subscribers.

### SQS

SQS may be considered optional in this case. It is not a requirement, but it comes with many benefits, especially when the event volume is high.

* SQS provides decoupling between source SNS and downstream services, i.e., asynchronous processing.

  + Replaying of events becomes easy through SQS: e.g.

    - A DLQ can be set up for failed processing
    - Setting the message visibility to reappear at a later time
* SQS provides reliable options for scaling like:

  + Multiple SQS to consume the same SNS for different use cases
  + Same SQS to consume from multiple SNS for different use cases

### Lambda

Another popular and successful AWS serverless service for event-driven architecture. Lambda can be hooked directly to SNS or via SQS, as discussed above.

* For this particular architecture, Lambda listens to a single SNS attached to a single S3 bucket.
* Lambda works great as a centralized service for routing different types of events to diverse downstream services, providing you the ability to perform lightweight processing like parsing or transformation, e.g., if A, then trigger B; if Y, then trigger Z.

* If multiple Lambda’s are used, then a separate SQS would be required; read more about Messaging Systems 📖: Messaging Systems: [Queue Based vs Log Based](https://www.junaideffendi.com/p/messaging-systems-queue-based-vs?r=cqjft&utm_campaign=post&utm_medium=web)

### Step Function

Step Function is used to orchestrate the different types of processing into one place. It's much easier to set up a pipeline in Step Function for a few reasons: it's serverless, it seamlessly connects native AWS services, etc.

In our architecture, we have multiple Step Functions per data source, and Lambda works great as a proxy to trigger the required Step Function.

> 💡Step Function cannot be triggered directly from SQS or SNS.

To learn about the Orchestrators, checkout📖: [My Data Pipeline Orchestrators Journey](https://www.junaideffendi.com/p/my-data-pipeline-orchestrators-journey?r=cqjft&utm_campaign=post&utm_medium=web).

Inside the Step Function, you can call multiple different services; for this example, I am sharing a few below.

### Batch

Batch is another option for running custom code. It requires you to set up a shared computing environment. Batch can be used to run lightweight transformations, file downloads, file movements, etc.

In the image, after the successful execution of Batch, we send data to Dynamo for OLTP and Redshift for OLAP.

### EMR

For heavy workloads where MPP is required, Spark on EMR is a great option, Step Function can do all the stitching for you like Creating a cluster, Submitting the Spark Job, and terminating once done.

In the image, after successfully executing Spark Jobs, we send data to Dynamo for OLTP and Redshift for OLAP.

### Redshift

Redshift connector can also be called easily within Step Function to execute SQL statements to process data end-to-end or load data in a typical ETL fashion.

### Dynamo

Dynamo DB is another great example from experience, you can easily call functions like Update Dynamo Table, Run an Import Job etc. without writing a single line of code.

---

Further, after the step function run completes, you can trigger multiple downstream dependencies, such as SNS and Lambda.

### Alerting

Alerting can be done easily in AWS via SNS. SNS can be attached to each required component; for example, we have set it for Lambda and Step Functions.

---

## Outro

**Coming back to the question of whether I would prefer this today,** the answer would be *it depends**.***

* I would say if I am building something from scratch and have all the support I need, then modern orchestrators like Airflow can definitely do the job well within one centralized system.
* At my current work, I still use a similar pipeline as above due to limitations and support. Basically, it's better to evaluate rather than go directly to modern solutions. It's easier to add another AWS service to the existing workflow rather than thinking of migration.

---

If you like the article, you might enjoy other content from Junaid, subscribe here for his valuable work:

[![](https://substackcdn.com/image/fetch/$s_!iYad!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6aa39096-d454-439f-98b5-baea84b501aa_800x800.png)Junaid Effendi | Sharing knowledge for Engineers

Covering tech, career, data, growth experiences from my journey.](https://www.junaideffendi.com?utm_source=substack&utm_campaign=publication_embed&utm_medium=web)
