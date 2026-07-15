---
title: "I spent 12 Hours rebuilding my Junior year project: Part 1 - The Extract Load"
channel: vutr
author: "Vu Trinh"
published: 2026-05-14
url: https://vutr.substack.com/p/i-spent-12-hours-rebuilding-my-junior
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Snowflake", "Data Warehouse", "Orchestration", "Data Quality"]
tags: [snowflake, https, auto, terraform, airflow, skytrax]
---

# I spent 12 Hours rebuilding my Junior year project: Part 1 - The Extract Load

*A Guess post from Minh Pham. A weekend project to boost your data engineer career. *

> Source: [Open post](https://vutr.substack.com/p/i-spent-12-hours-rebuilding-my-junior)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[data-warehouse|Data Warehouse]] · [[orchestration|Orchestration]] · [[data-quality|Data Quality]]

---

> *I invite you to join my paid membership list for only **7$/month** (pay annually) to get access to:*
>
> [![](https://substackcdn.com/image/fetch/$s_!L1VM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ecb5b15-1a2b-4440-a5f4-3de0cd88e9c0_1182x696.png)](https://substack-github-sync.vutrinh2704.workers.dev/)
>
> * *This article + other 200+ deep-dive data engineering articles*
> * *CLI tools to help you learn data engineering skills → [Demo for Spark learning tool](https://substack-github-sync.vutrinh2704.workers.dev/)*
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=196971708)
>
> *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***

[![](https://substackcdn.com/image/fetch/$s_!wqUP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe72d9eb3-fc15-42a4-8997-06f53a3d3f78_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!wqUP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe72d9eb3-fc15-42a4-8997-06f53a3d3f78_2000x1429.png)

---

# Intro

This is a guest post from [Minh Pham](https://www.linkedin.com/in/minhbphamm/), the hardest-working and most enthusiastic data engineer I’ve ever known. Minh will share his learning on data engineering best practices via a multi-part hands-on project. This article is the first part in which he discusses ingestion.

If you enjoy it, please react to the article or share it so we know you like it. Plus, Minh is more motivated to write the next part. As you might know, writing an article is hard, but writing an article to guide a hands-on project is 10x harder, as you have to prepare for a lot of things.

—

Hi everyone, my name is Mark, an Analytics Engineer at [Insurify](https://insurify.com/), graduated from TCU in the summer of 2025, majoring in Computer System Analyst with minors in Math and Fintech.

This is the first in my series where I built end-to-end data pipelines/Infrastructure that follow best practices I learned at Insurify. This is a sophomore-year side project that was rebuilt after learning best practices in analytics engineering at Insurify.

> **Note**: The data we’ll be using is completely unrelated to Insurify's business model.

In this part, we will dive into the extract-load process (ingestion), where we “extract” data from a data source, load it into a simple staging area in S3, and process it from “raw” to “processed” prefixes.

Then load data into a landing area in Snowflake. Also, all infrastructure (AWS S3, IAM role, IAM users) is managed by Terraform. An AWS free trial account, the AWS CLI, and some exposure to Terraform (Infrastructure as Code) are required.

---

# Takeaway

Overall architecture details can be found [here](https://github.com/MarkPhamm/skytrax_reviews_extract_load/blob/main/README.md). This part’s takeaway:

* An overall understanding of how the Extract-Load (ingestion process) works
* Understand the use cases of a `staging` area, and why we need to stage data before loading it to the data warehouse
* High-level understanding of Infrastructure as code, of why we need to manage infrastructure using Terraform
* Airflow in actions, you will see terms like Dag/Task action with actual Python scripts

My junior-year version of this project was from the “non-technical” me, where I crawled 3000 British Airways Reviews and loaded them into an S3 Bucket that’s not even mine. No Cloud Data-Warehouse, No transformation. Scripts run manually on my computer.

3 years later, after joining Insurify, I can’t describe how much I learned. Now, in this project, we will follow “most of” the data engineering best practices. From orchestration, staging, cloud data warehouse, to infrastructure. I hope it will help people upskill and achieve their data engineering goals.

---

# Prerequisite

I would expect you to have some experience with Python - Airflow. Some experience with Docker is preferred, but not required. Experience with Git is crucial for cloning/replicating projects. And also, obviously, we

The main AWS/Snowflake infrastructure is all set up in the Terraform dir. You will need to create an AWS account and set up a terraform-admin profile. Don’t worry if you don’t have one. We will walk through the setup of creating a profile really quickly

For this article, you only need to know that Terraform is a tool for managing infrastructure as code; in this article, they are S3 buckets and IAM roles/users.

---

# Overview

You can clone the repo [here](https://github.com/MarkPhamm/skytrax_reviews_extract_load) to follow along. The tech stacks will be:

* Python: scraper, processing data - Python 3.12, pandas, BeautifulSoup
* Git/Github - CI/CD process, version control
* Airflow on Astronomer (On Docker): Orchestration layer
* S3/IAM role: Landing area, managed with Terraform
* Snowflake: Data warehouse: Database, Schema, and Table, all managed by Terraform

Data source → scraper.py → staging dir (local/s3) - raw → processing.py → staging dir (local/s3) - processed → snowflake\_load.py

[![](https://substackcdn.com/image/fetch/$s_!1t4u!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd15c1e8-3d86-4d38-90c0-4a72c83d3a0a_1538x714.png)](https://substackcdn.com/image/fetch/$s_!1t4u!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd15c1e8-3d86-4d38-90c0-4a72c83d3a0a_1538x714.png)

You must be wondering why there is an additional transformation from “raw” to “processd”? Why not just dump everything into Snowflake and transform with dbt? I believe there are several reasons for this (at Insurify, we implement this too)

* Early data validation: A “raw” to “processd” step helps catch issues before data reaches the DWH.
* Better observability: It gives visibility into incoming partner files before loading into Snowflake.
* Partner delivery workflow: At Insurify, we have multiple data sources, e.g., external partners often send reports directly to the raw directory via SFTP. This can help us validate data quality before it reaches the DWH
* Pre-processing outside dbt: We use Python scripts to clean, standardize, and validate files before ingestion.
* Catch incremental issues sooner: Things like missing columns or schema changes can be detected early.
* Faster alerting: For example, if a required column is missing, we can send a Slack alert immediately.
* Cleaner warehouse inputs: Only validated, structured data gets loaded into Snowflake, which keeps downstream models more reliable.

Finally, we will orchestrate using Airflow on Astronomer, though there’s no production process, we will run Airflow locally with astro dev start. There are 3 main dags:

* dag\_crawl.py
* dag\_process.py
* dag\_snowflake.py

---

> *I invite you to join my paid membership list for only **7$/month** (pay annually) to get access to:*
>
> [![](https://substackcdn.com/image/fetch/$s_!L1VM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ecb5b15-1a2b-4440-a5f4-3de0cd88e9c0_1182x696.png)](https://substack-github-sync.vutrinh2704.workers.dev/)
>
> * *This article + other 200+ deep-dive data engineering articles*
> * *CLI tools to help you learn data engineering skills → [Demo for Spark learning tool](https://substack-github-sync.vutrinh2704.workers.dev/)*
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=196971708)
>
> *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***

---

# Step 1: Clone the repo and set up the virtual env

The repo link is [here](https://github.com/MarkPhamm/skytrax_reviews_extract_load).

Clone this repo and make sure to enter the repo folder throughout this article.

Run this command to initialize a Python virtual environment:

```
uv sync
```

`uv` is a dependency management tool (similar to pip and poetry) that resolves dependencies and downloads all the libraries we need into a dedicated `.venv` folder.

---

# Step 2: Run the `scraper.py`

[![](https://substackcdn.com/image/fetch/$s_!ODJG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d6e3e72-8b82-4b71-a92b-90940b54d9da_336x362.png)](https://substackcdn.com/image/fetch/$s_!ODJG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d6e3e72-8b82-4b71-a92b-90940b54d9da_336x362.png)

We are ready to run everything locally. All the local development docs are available [here](https://github.com/MarkPhamm/skytrax_reviews_extract_load/blob/main/docs/local-dev.md). Copy the example env file and fill in your values (for local-only development, the defaults work as-is):

```
cp .env.example .env
```

## Testing out scraper.py with a small amount of data

Scrape 1 airline, 1 page (~100 rows). Output goes to `landing/raw/`:

```
make scrape-smoke
```

Verify the output:

```
ls landing/raw/
```

You should see YYYY/MM/raw\_data\_YYYYMMDD.csv files

Next, we process a specific date's raw file into a cleaned CSV:

```
make process DATE=2026-03-12
#or
make process-yesterday
```

Output goes to landing/processed/YYYY/MM/clean\_data\_YYYYMMDD.csv.

Then, we scrape all airlines across all pages. It might take a while:

```
make scrape
```

After scrapping everything, you should be able to see all the raw data in the landing/raw dir:

[![](https://substackcdn.com/image/fetch/$s_!FupJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a184ee4-dabf-44e5-a224-a1b92014d8be_738x1074.png)](https://substackcdn.com/image/fetch/$s_!FupJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a184ee4-dabf-44e5-a224-a1b92014d8be_738x1074.png)

After scraping all historical data, we can process all of them using:

```
make process
```

# Step 3: Setting up an AWS account and a Terraform-admin role

[![](https://substackcdn.com/image/fetch/$s_!ZUU-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1ebdc03-1f9f-4bef-a8d8-570ffde4e901_1042x738.png)](https://substackcdn.com/image/fetch/$s_!ZUU-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1ebdc03-1f9f-4bef-a8d8-570ffde4e901_1042x738.png)

1. First, you might need to sign up for an AWS free tier account: regarding this, I’ve already created an end-to-end document you can find here. Don’t worry if they ask for your credit card details, I’ve had the same fear before, but if you’re careful, it’s gonna be all fine ;)

2. Second, you will need to set up an IAM user called terraform-admin. The setup can be found [here](https://github.com/MarkPhamm/AWS/blob/main/docs/02-iam-user-setup.md). This user will have access to AWS CLI only. Remember to copy these 2 somewhere secure:

* Access Key ID (starts with `AKIA...`)
* Secret Access Key (shown only once!)

3. From there, you can set up AWS CLI and Terraform following the instructions [here](https://github.com/MarkPhamm/AWS/blob/main/docs/03-aws-cli-terraform-setup.md). The setup will also give you an ARN (Amazon Resource Name). It’s a unique address for anything in AWS (a user, a bucket, a role, etc.). This setup will live in your ~/.aws/credentials dir.

4. That’s it 🙂. Now the profile is configured, and Terraform will pick it up whenever we want to plan/apply/destroy any resources.

---

# Step 4: Creating a `Snowflake` trial account

[![](https://substackcdn.com/image/fetch/$s_!R99p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e02da2c-521e-4243-8115-130c6edf3034_240x306.png)](https://substackcdn.com/image/fetch/$s_!R99p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e02da2c-521e-4243-8115-130c6edf3034_240x306.png)

This is very straightforward. Snowflake offers a 30-day free trial with $400 in credits. Which is way more than what we need.

1. Go to <https://signup.snowflake.com/>
2. Enter your credential
3. Choose AWS as your cloud service
4. Then verify/create a password, and your cloud DWH is now ready. This is where most of our transformation via `dbt` happens in part 2 (coming soon).

---

# Step 5: Set up AWS IAM, S3

Now that we have our AWS account and terraform-admin profile configured, we can start provisioning all the AWS infrastructure using Terraform. Everything lives in terraform/aws/ - this is where we define our S3 bucket, IAM role, IAM user, and policies. No clicking around the AWS console, everything is code - even though this might be a bit difficult to learn at first, but don’t worry ;) I’mma guide you through it

Most of this section is about controlling IAM (identity and access management) so that our local Airflow can talk to the S3 bucket, and Snowflake can COPY data from the S3 Bucket by creating a STAGE that assumes an IAM role.

Airflow → S3: IAM User (long-lived credentials)

* Terraform creates an IAM User (skytrax-airflow-dev) with an access key pair (Access Key ID + Secret Access Key)
* These keys are baked into the Airflow connection URI in .env
* Airflow uses them directly to call S3 PutObject/GetObject — no role assumption involved

S3 → Snowflake (via Stage): IAM Role (temporary credentials)

* Terraform creates an IAM Role (skytrax-snowflake-s3-dev) with S3 read permissions
* When you create a Snowflake external stage with AWS\_ROLE = '<role\_arn>', Snowflake allocates an IAM user from its own internal AWS account
* That Snowflake-owned IAM user calls sts:AssumeRole on your role to get temporary credentials. Think of it as “I’m user X, let me temporarily act as role Y.”

  1. The caller (Snowflake’s internal IAM user) must have permission to call sts:AssumeRole
  2. The role must have a trust policy that says, “I allow this specific principal to assume me.”
* You must update the role’s trust policy with Snowflake’s IAM user ARN + external ID (chicken-and-egg: two AWS applies needed)
* When COPY INTO runs, Snowflake uses these temporary, auto-rotating credentials to read from S3

## What Terraform

Let me walk through what resources we’re spinning up:

S3 Bucket (skytrax-reviews-landing-<your\_account\_id>) - This is our landing zone. All scraped CSVs (both raw and processed) are uploaded here before being loaded into Snowflake. The bucket name is auto-generated using your AWS account ID, so it’s guaranteed to be globally unique. The bucket comes with:

* Versioning enabled - so we can recover if something goes wrong
* Lifecycle rules - raw and processed files transition to STANDARD\_IA (Infrequent Access) after 30 days to save cost. Old versions expire after 90 days
* Server-side encryption (AES256) - data at rest is encrypted
* Public access fully blocked - no one is accidentally exposing our data

Besides the S3 bucket, there are only 2 problem we need to solve

* Authenticating Airflow to read/write to AWS S3 (user-level-auth)
* Authenticating Snowflake to run COPY command from S3 (role-level auth)

For Airflow → S3 (user-level auth):

1. IAM User (skytrax-airflow-dev) - a programmatic-access-only user for Airflow
2. IAM Access Key - auto-generated access\_key\_id + secret\_access\_key credentials for the user - we’ll use these later when setting up the Airflow AWS connection in .env later
3. IAM Policy (skytrax-airflow-s3-dev) - defines the actual S3 permissions: s3:ListBucket, s3:GetObject, s3:PutObject, s3:DeleteObject, etc. Basically, everything Airflow needs to upload raw files, upload processed files, and clean up old ones
4. IAM User Policy Attachment - attaches the S3 policy directly to the user

For S3 → Snowflake (role-level auth):

1. IAM Role (skytrax-snowflake-s3-dev) - the role Snowflake assumes to read from S3 during COPY INTO. The trust policy is auto-configured to allow your AWS account (and later Snowflake) to assume it
2. IAM Role Policy Attachment - attaches the same S3 policy to the role, so Snowflake gets the same S3 permissions

In total, Terraform creates 11 resources: the S3 bucket (with versioning, lifecycle, encryption, and public access block configs) + the 6 IAM resources above.

## Configure your variables

```
cp terraform/aws/terraform.tfvars.example terraform/aws/terraform.tfvars
```

Then edit `terraform/aws/terraform.tfvars` with your values:

```
aws_region  = "us-east-1"
environment = "dev"
```

That’s it. You don’t need to configure a bucket name or any IAM ARNs. Terraform automatically detects your AWS account ID from the terraform-admin profile and uses it to:

* Name the bucket skytrax-reviews-landing-<your\_account\_id> (guaranteed unique since account IDs are unique)
* Set up the IAM trust policy so your account can assume the Snowflake S3 role

## Terraform plan and apply

Now let’s provision everything. Enter into the terraform directory and run:

```
cd terraform/aws
terraform init
terraform plan
```

“terraform plan” will show you exactly what resources are going to be created - review it and make sure everything looks right. You should see 11 resources being created.

Once you’re happy with the plan:

```
terraform apply
```

Type `yes` when prompted. After it finishes, Terraform will output some important values:

```
Outputs:

bucket_name               = "skytrax-reviews-landing-XXXXXXXXXXXX"
bucket_arn                = "arn:aws:s3:::skytrax-reviews-landing-XXXXXXXXXXXX"
snowflake_s3_role_arn     = "arn:aws:iam::XXXXXXXXXXXX:role/skytrax-snowflake-s3-dev"
airflow_access_key_id     = "AKIAXXXXXXXXXXXXXXXX"
airflow_secret_access_key = <sensitive>
```

> **Note:** airflow\_secret\_access\_key is marked as sensitive, so Terraform won’t display it directly. To retrieve it:

```
terraform output -raw airflow_secret_access_key
```

Save both the `airflow_access_key_id` and `airflow_secret_access_key` somewhere secure - we will need them later.

After running, you can go to the AWS console and verify:

* S3 → you should see your bucket with versioning enabled:

  [![](https://substackcdn.com/image/fetch/$s_!4Xne!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feea297b6-e1b5-4517-9f5b-e03479d679c0_658x378.png)](https://substackcdn.com/image/fetch/$s_!4Xne!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feea297b6-e1b5-4517-9f5b-e03479d679c0_658x378.png)
* IAM → you should see the skytrax-snowflake-s3-dev role and skytrax-airflow-dev user:

  [![](https://substackcdn.com/image/fetch/$s_!ADDP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48b338d0-9368-4695-9cd1-029a3c5140e2_778x294.png)](https://substackcdn.com/image/fetch/$s_!ADDP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48b338d0-9368-4695-9cd1-029a3c5140e2_778x294.png)

  [![](https://substackcdn.com/image/fetch/$s_!UOYB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faaeed62c-08c4-4a46-b339-75313ba293db_1012x370.png)](https://substackcdn.com/image/fetch/$s_!UOYB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faaeed62c-08c4-4a46-b339-75313ba293db_1012x370.png)

## Initial data load to S3

The reason we partition by year/month/date is that, for each date, we only process the day before incrementally. That is, let’s say a DAG with a start\_date of today will have an execution\_date of yesterday and will incrementally process yesterday's data. Some core date definition in Airflow are

* `logical_date` **/** `execution_date` = label for the run (imagine the data it covered)
* `data_interval_start` **/** `data_interval_end` = data window covered
* `start_date` = when it actually began running
* `end_date` = when it actually finished

If the DAG runs every 3 days, we have the following example:

[![](https://substackcdn.com/image/fetch/$s_!w25j!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e016831-f6ad-46c9-87ff-05b3d4ccd044_816x312.png)](https://substackcdn.com/image/fetch/$s_!w25j!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e016831-f6ad-46c9-87ff-05b3d4ccd044_816x312.png)

If you already scraped and processed data locally in Step 2, you can do an initial sync to upload everything from your local `landing/` directory to S3 using the `AWS CLI` for an initial load

```
aws s3 sync landing/ s3://skytrax-reviews-landing-<your_account_id>/ --profile terraform-admin --exclude ".gitkeep"
```

This will upload all your `raw/` and `processed/` CSVs to the matching S3 paths. After this, your S3 bucket should mirror the same directory structure as your local `landing/` dir.

That’s it for the AWS setup. All managed by Terraform - if you ever need to tear everything down, just run `terraform destroy` and it’s all gone. Clean and reproducible.

---

# Step 6: Set up the Staging area between S3 and Snowflake

[![](https://substackcdn.com/image/fetch/$s_!tCB4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3eb948ef-6ed0-4ddd-ab93-9bf2103467d5_1066x352.png)](https://substackcdn.com/image/fetch/$s_!tCB4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3eb948ef-6ed0-4ddd-ab93-9bf2103467d5_1066x352.png)

Now here’s where it gets interesting. We need to connect Snowflake to our S3 bucket so that Snowflake can read data from it. This is done through an **external stage** - basically telling Snowflake “hey, here’s an S3 path and an IAM role you can use to access it.”

The Snowflake Terraform module lives in `terraform/snowflake/` and creates:

* **Database** (`SKYTRAX_REVIEWS_DB`)
* **Schema** (`RAW`)
* **Table** (`AIRLINE_REVIEWS`) - column order matches our processed CSV output
* **External Stage** (`SKYTRAX_S3_STAGE`) - points to our S3 bucket, uses the `skytrax-snowflake-s3-dev` IAM role so Snowflake can assume it and read from S3

## Configure Snowflake variables

First, grab the outputs from the AWS module - you’ll need bucket\_name and snowflake\_s3\_role\_arn:

```
cd terraform/aws
terraform output
```

Then copy and fill in the Snowflake tfvars:

```
cp terraform/snowflake/terraform.tfvars.example terraform/snowflake/terraform.tfvars
```

Edit `terraform/snowflake/terraform.tfvars` with your Snowflake credentials and the AWS outputs:

```
snowflake_org            = "MYORG"
snowflake_account        = "MYACCOUNT"
snowflake_admin_user     = "your_username"
snowflake_admin_password = "your_password"

# from step 5
bucket_name      = "skytrax-reviews-landing-XXXXXXXXXXXX"
snowflake_s3_role_arn = "arn:aws:iam::XXXXXXXXXXXX:role/skytrax-snowflake-s3-dev"
```

You can find your `snowflake_org` and `snowflake_account` from your Snowflake account URL - it’s in the format: https://ORG-ACCOUNT.snowflakecomputing.com

`bucket_name` and `snowflake_s3_role_arn` should be the output you saw from step 5

## Apply the Snowflake module

```
cd terraform/snowflake
terraform init
terraform plan
terraform apply
```

This creates the database, schema, table, and external stage in Snowflake.

## Get the Snowflake IAM user ARN (important!)

Here’s the tricky part. When you create a stage with `AWS_ROLE`, Snowflake doesn’t create anything in *your* AWS account. What actually happens is Snowflake already has its own internal AWS account with its own IAM users. It **assigns one of those internal users to your stage** - so when Snowflake runs `COPY INTO`, that internal user calls `sts:AssumeRole` on your `skytrax-snowflake-s3-dev` role to get temporary credentials, and uses those to read from your S3 bucket.

The problem is: by default, *your role doesn’t trust some random user from Snowflake’s AWS account*. So we need to grab that user’s ARN and add it to the role’s trust policy - basically telling AWS, “hey, this external user from Snowflake is allowed to assume this role.”

Run this in Snowflake (via the Snowflake UI or `snowsql`):

[![](https://substackcdn.com/image/fetch/$s_!ZcHV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68e771d6-fc9b-4f09-859f-85f22bb78c3c_1412x1408.png)](https://substackcdn.com/image/fetch/$s_!ZcHV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68e771d6-fc9b-4f09-859f-85f22bb78c3c_1412x1408.png)

Look for STORAGE\_AWS\_IAM\_USER\_ARN in the output. Copy that value.

Now go back to the AWS module and add the Snowflake ARN to your terraform/aws/terraform.tfvars:

```
aws_region  = "us-east-1"
environment = "dev"

snowflake_iam_user_arn = "YOUR STORAGE_AWS_IAM_USER_ARN"
```

Right now, the `skytrax-snowflake-s3-dev` role’s trust policy only trusts your own AWS account. Snowflake’s internal user lives in a completely different AWS account - so when it tries to call `sts:AssumeRole`, AWS rejects it with “I don’t know you.”

By adding the `snowflake_iam_user_arn` to your `tfvars`, Terraform updates the trust policy to say “I trust both my own account AND this Snowflake user.” That’s the two-pass setup - you can’t do it in one shot because you don’t know Snowflake’s IAM user ARN until after you create the stage.

Re-apply the AWS module:

```
cd terraform/aws
terraform apply
```

# Step 7: Set up Airflow connections with AWS and Snowflake

Before we wire everything up, let’s be clear about the two different authentication flows in this pipeline - because they use different IAM resources and it’s easy to mix them up:

**Workflow 1: Airflow → S3 (user-level auth via access keys)**

* Airflow uploads and downloads files to/from S3 using an **IAM User** (`skytrax-airflow-dev`).
* Terraform creates this user with an access key pair (`access_key_id` + `secret_access_key`). We put those credentials in the Airflow `.env` file as the `AIRFLOW_CONN_AWS_S3_CONNECTION`.
* This is direct, user-level authentication - Airflow sends the access key with every S3 API call. No role assumption involved.

**Workflow 2: S3 → Snowflake (role-level auth via** `sts:AssumeRole`**)**

* Snowflake reads files from S3 during `COPY INTO` using an **IAM Role** (`skytrax-snowflake-s3-dev`). When we created the external stage in Step 6, we gave Snowflake the role ARN. Under the hood,
* Snowflake has its own internal AWS account - it calls `sts:AssumeRole` on our role to get temporary credentials, then uses those to read from our S3 bucket. That’s why we needed the two-pass setup: first create the role, then tell AWS to trust Snowflake’s IAM user in the role’s trust policy.

**Why two different approaches?** The IAM user provides Airflow with long-lived credentials that work in a Docker container without an AWS metadata service. The IAM role gives Snowflake temporary, scoped credentials without us ever sharing secrets - Snowflake never sees an access key, it just assumes the role.

Now let’s set up the actual connections. Airflow connections are configured through environment variables in a `.env` file - no clicking around the Airflow UI needed.

## Install Astro CLI and start Airflow

If you haven’t already, install the [Astro CLI](https://www.astronomer.io/docs/astro/cli/install-cli). Then build the Astronomer Docker image:

```
make dev-setup
```

This builds the Docker image and starts Airflow locally. The Airflow UI will be available at http://localhost:8081

## Create the .env file

We already created a `.env` file in Step 2 for local development. Now we need to update it with our AWS and Snowflake credentials so Airflow can actually talk to S3 and Snowflake.

Open your `.env` file and update it to:

```
STORAGE_MODE=s3
S3_BUCKET=skytrax-reviews-landing-XXXXXXXXXXXX
AIRFLOW_CONN_AWS_S3_CONNECTION=aws://<ACCESS_KEY_ID>:<URL_ENCODED_SECRET>@/?region_name=us-east-1
AIRFLOW_CONN_SNOWFLAKE_DEFAULT='{"conn_type":"snowflake","login":"<SNOWFLAKE_USER>","password":"<SNOWFLAKE_PASSWORD>","schema":"RAW","extra":{"account":"<ORG>-<ACCOUNT>","database":"SKYTRAX_REVIEWS_DB","warehouse":"COMPUTE_WH","role":"SYSADMIN"}}'
```

Let me break down what each variable does:

* `STORAGE_MODE=s3` - tells the pipeline to use S3 instead of local storage. When this was `local`, the DAGs skipped S3/Snowflake entirely. This is intended for local development
* `S3_BUCKET` - your bucket name from `terraform output bucket_name`
* `AIRFLOW_CONN_AWS_S3_CONNECTION` - the AWS connection in URI format. Airflow reads this env var and auto-registers it as a connection with ID `aws_s3_connection`
* `AIRFLOW_CONN_SNOWFLAKE_DEFAULT` - the Snowflake connection in JSON format. Must be wrapped in single quotes. Airflow registers this as `snowflake_default`

Where to get the values

[![](https://substackcdn.com/image/fetch/$s_!ql_h!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84b9f3bc-49c8-41e6-a87c-09c61fbc719e_1024x448.png)](https://substackcdn.com/image/fetch/$s_!ql_h!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84b9f3bc-49c8-41e6-a87c-09c61fbc719e_1024x448.png)

## Test the connection before restarting

Before restarting Airflow, verify your credentials work by running a quick S3 list from your terminal. Use the **raw** (non-URL-encoded) secret key here - this is a direct AWS CLI call, not an Airflow URI:

```
AWS_ACCESS_KEY_ID=<ACCESS_KEY_ID> AWS_SECRET_ACCESS_KEY='<SECRET_KEY>' aws s3 ls s3://<BUCKET_NAME>/ --region us-east-1
```

You should see something like:

```
PRE processed/
PRE raw/
```

If you see your prefixes listed, your credentials are valid. If you get `SignatureDoesNotMatch`, the secret key is wrong - go back to the IAM console and double-check it (and remember: that trailing `%` from `terraform output -raw` is not part of the key).

Once the CLI test passes, you know that any future SignatureDoesNotMatch in Airflow is due to a URL-encoding issue in the `.env`, not a bad key.

## Restart Airflow

After updating `.env`, restart Airflow, so it picks up the new connections:

```
astro dev restart
```

You can verify the connections are registered by going to the Airflow UI → Admin → Connections. You should see `aws_s3_connection` and `snowflake_default`.

---

# Step 8: Set up COPY INTO via Airflow DAG

Now everything is wired up - S3 bucket, Snowflake stage, Airflow connections. Time to run the full pipeline.

## How the DAGs work

The pipeline consists of 3 DAGs chained together via **Airflow Datasets**:

1. `skytrax_crawl` (Extract) - scrapes reviews from [airlinequality.com](http://airlinequality.com/), splits by review date, uploads raw CSVs to S3. Emits the `skytrax://raw` dataset when done

   [![](https://substackcdn.com/image/fetch/$s_!WORG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F089749c4-0684-4223-9f69-5610dfa4b87d_996x594.png)](https://substackcdn.com/image/fetch/$s_!WORG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F089749c4-0684-4223-9f69-5610dfa4b87d_996x594.png)

2. skytrax\_process (Transform) - triggered automatically when new raw data lands. Downloads the raw CSV, runs the cleaning pipeline, and uploads the processed CSV to S3. Emits skytrax://processed

   [![](https://substackcdn.com/image/fetch/$s_!4mU4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b8baa51-9897-4f78-93df-efd2c4c4e844_1000x404.png)](https://substackcdn.com/image/fetch/$s_!4mU4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b8baa51-9897-4f78-93df-efd2c4c4e844_1000x404.png)
3. skytrax\_snowflake (Load) - triggered automatically when processed data is ready. Runs COPY INTO for each review date to load into Snowflake

   [![](https://substackcdn.com/image/fetch/$s_!popj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac357e46-7238-4333-a9c6-2eb283b37a13_952x370.png)](https://substackcdn.com/image/fetch/$s_!popj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac357e46-7238-4333-a9c6-2eb283b37a13_952x370.png)

   The key thing here is that these DAGs are event-driven. You don’t need to schedule them separately - when skytrax\_crawl finishes, it automatically triggers skytrax\_process, which then triggers skytrax\_snowflake.

# The COPY INTO logic

The actual loading happens in include/tasks/load/snowflake\_load.py. For each review date, it runs this SQL template (include/sql/copy\_into.sql):

```
COPY INTO SKYTRAX_REVIEWS_DB.RAW.AIRLINE_REVIEWS
FROM @SKYTRAX_REVIEWS_DB.RAW.SKYTRAX_S3_STAGE/{{ s3_key }}
ON_ERROR = 'CONTINUE'
PURGE    = FALSE;
```

Where `{{ s3_key }}` gets replaced with the actual S3 path like `processed/2026/03/clean_data_20260312.csv`. A few things to note:

* `ON_ERROR = 'CONTINUE'` - keeps loading even if some rows fail, so one bad row doesn’t block the whole file
* `PURGE = FALSE` - doesn’t delete the source file after loading, so you can always re-run
* Snowflake internally tracks which files have been loaded, so running the same `COPY INTO` twice won’t create duplicates

The `skytrax_snowflake` DAG uses **dynamic task mapping** - it creates one `load_date` task per review date. So if the crawler found reviews for 5 different dates, you’ll see 5 parallel load tasks in the Airflow UI.

## Run the full pipeline

### Daily incremental run

The `skytrax_crawl` DAG is scheduled to run daily. It scrapes yesterday’s reviews, and the downstream DAGs trigger automatically via Datasets.

To trigger manually: click the play button on `skytrax_crawl` in the Airflow UI.

### Full initial load

For the first time, you want to load all historical reviews:

1. Go to the `skytrax_crawl` DAG in the Airflow UI
2. Click **Trigger DAG w/ config**
3. Set `full_scrape` to `true`
4. Click **Trigger**

This scrapes all historical reviews going back to 2002. The downstream `skytrax_process` and `skytrax_snowflake` DAGs trigger automatically and load everything into Snowflake.

## Verify the data in Snowflake

Once the pipeline finishes, verify the data landed:

```
SELECT COUNT(*) FROM SKYTRAX_REVIEWS_DB.RAW.AIRLINE_REVIEWS;
-- Should see 160,000+ rows

SELECT * FROM SKYTRAX_REVIEWS_DB.RAW.AIRLINE_REVIEWS LIMIT 10;
```

You can also check S3 to make sure files are there:

```
aws s3 ls s3://skytrax-reviews-landing-<your_account_id>/processed/ --recursive | head -20
```

---

# Outro

And that’s it! You now have a fully working ingestion pipeline - scraping data from the web, staging it in S3, and loading it into Snowflake. All orchestrated by Airflow, all infrastructure managed by Terraform.

If you like this article, please react or share it so we know you enjoy it.

Thank you for reading this far. See you in the next articles.
