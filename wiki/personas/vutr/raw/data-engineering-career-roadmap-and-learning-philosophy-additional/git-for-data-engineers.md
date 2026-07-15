---
title: "Git for Data Engineers"
channel: vutr
author: "Vu Trinh"
published: 2025-07-08
url: https://vutr.substack.com/p/git-for-data-engineers
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark"]
tags: [https, auto, fetch, substackcdn, image, good]
---

# Git for Data Engineers

*Just don't share code with your teammates via Google Drive like I did.*

> Source: [Open post](https://vutr.substack.com/p/git-for-data-engineers)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=167413589)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!E7s4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c736561-d6d7-4676-8caa-0b1e2cb3ac88_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!E7s4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c736561-d6d7-4676-8caa-0b1e2cb3ac88_2000x1429.png)

---

## Intro

During my final year at university, I collaborated with a friend on a capstone project—a simple Python application. We needed a way to share what we’ve done. Guess what, we shared Python scripts via Google Drive.

Unsurprisingly, this caused us a lot of trouble managing the code, as it lacked version control and the ability to isolate each other’s work. If we had chosen Git in the first place, we wouldn't be suffering like that.

Seven years passed, and Git is now a part of my job. But here is my confession: I don't truly understand how it works behind the scenes. I decided to sit down and relearn this. This time, it's not only about some Git commands, but also about what happens under the hood.

---

## Centralized vs distributed version control system

Before learning Git, it would be helpful to understand the differences between centralized and distributed version control systems.

A version control system (VCS) tracks changes to files over time, facilitating team collaboration and coordination. Sharing via a shared Drive will soon become a nightmare, as we can only overwrite the files without any version tracking. Naming a file differently with a new version could work, but it is highly error-prone.

People developed a Centralized Version Control System (CVCS) to deal with this problem. The CVCS has a server that manages all the versioned files. The client can create local copies of the files they want to work with. When done, they update the changes to the central server.

[![](https://substackcdn.com/image/fetch/$s_!Y5oU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F170f5100-f754-40fd-abd0-6983783da4e8_508x502.png)](https://substackcdn.com/image/fetch/$s_!Y5oU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F170f5100-f754-40fd-abd0-6983783da4e8_508x502.png)

However, it has disadvantages. If the server fails, the whole codebase will be gone. Additionally, most operations in a CVCS require a constant connection to the central server. This is problematic for developers working with an unreliable internet connection.

That’s why a distributed version control system (DVCS) was developed.

[![](https://substackcdn.com/image/fetch/$s_!1A95!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa702f957-d751-43df-95a1-8747d7e0ef50_444x618.png)](https://substackcdn.com/image/fetch/$s_!1A95!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa702f957-d751-43df-95a1-8747d7e0ef50_444x618.png)

It provides every developer with a complete copy of the entire repository, including the whole history. This eliminates the single point of failure inherent in CVCS. Operations like commits and branching are lightning-fast and entirely local (as each client keeps a local repository), solving the performance and offline work limitations of CVCS.

Git is an [open-source](https://git-scm.com/about/free-and-open-source) DVCS developed by the Linux development community in 2005

---

## Git overview

Compared to other VCS, Git sees the data as snapshots rather than delta changes. This provides powerful branching capability by leveraging lightweight pointers. We will learn more about commits and branches in the following sections.

[![](https://substackcdn.com/image/fetch/$s_!kOjW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd379e439-f899-48f6-ae23-516284a30cd7_568x202.png)](https://substackcdn.com/image/fetch/$s_!kOjW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd379e439-f899-48f6-ae23-516284a30cd7_568x202.png)

To ensure integrity, Git checksums everything. This helps Git check file changes efficiently. Git uses SHA-1 hash for the checksum; the hash function inputs are the file/directory contents, and the result is a 40-character string with hexadecimal characters (0–9 and a–f)

[![](https://substackcdn.com/image/fetch/$s_!zvtr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c082f82-ff5d-498c-8977-aeb98dc25593_688x174.png)](https://substackcdn.com/image/fetch/$s_!zvtr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c082f82-ff5d-498c-8977-aeb98dc25593_688x174.png)

Due to the nature of a DVCS, most Git operations can be performed locally, as each client will have a local repo on your computer. Users persist the changes locally. Only when they need to collaborate do they interact with the remote repo via the internet.

We will learn about the local and remote repo in the next section.

---

## The local repo

In local, Git manages your files in 3 sections:

[![](https://substackcdn.com/image/fetch/$s_!CgKK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02a8250e-1c96-4dfe-8e49-20f11fe4cfc5_656x272.png)](https://substackcdn.com/image/fetch/$s_!CgKK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02a8250e-1c96-4dfe-8e49-20f11fe4cfc5_656x272.png)

* **Working directory**: This is where we can see and edit the actual files.
* **Staging area**: It is a file inside a .git directory that holds the information of what will be included in the next commit.
* **The local repository** (.git dir): This is where Git stores the history of your project as a series of commit objects locally.

A typical workflow looks like this: you make changes to files, then you choose what to commit by staging them; when everything is ready, you commit your changes to the local repository.

In the working directory, a file could be in one of the two states:

[![](https://substackcdn.com/image/fetch/$s_!n-I5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a2c34a3-59fd-4140-9f38-672f5dfc7aab_770x428.png)](https://substackcdn.com/image/fetch/$s_!n-I5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a2c34a3-59fd-4140-9f38-672f5dfc7aab_770x428.png)

* **Untracked:** These are files in your working directory that were not in the last commit and are not in the staging area. Git is not familiar with these files. This is the state of any brand-new file.
* **Tracked:** These are files that Git knows about. They were part of the last commit, and Git is actively tracking them. Tracked files can exist in one of the following sub-states: **unmodified, modified, staged,** or **committed**.

**Committed** means your changes are persisted in the repository. **Staged** means your files are included in the stage area. **Modified** means Git detects that your files have changed compared to the latest commit, but they are not staged or committed. **Unmodified** means your files remain unchanged compared to the last commit.

---

## The remote repo

While it's true that every developer has a complete local copy of the repository in a DVCS, it would be a mess if they connected directly to each other's laptops to share the updates.

[![](https://substackcdn.com/image/fetch/$s_!Gzlx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e1c9c68-118e-4726-9b01-5c59e14981a3_538x418.png)](https://substackcdn.com/image/fetch/$s_!Gzlx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e1c9c68-118e-4726-9b01-5c59e14981a3_538x418.png)

With a remote repository, everyone synchronizes their work with this central hub.

[![](https://substackcdn.com/image/fetch/$s_!CqO7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F042510ec-c39b-4931-986d-b0904bcc7ea9_548x452.png)](https://substackcdn.com/image/fetch/$s_!CqO7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F042510ec-c39b-4931-986d-b0904bcc7ea9_548x452.png)

The three sections above are on our local laptop. The remote repository is another version of your project that is located "elsewhere"—on platforms like GitHub, GitLab, or Bitbucket.

To share your changes, you can “push” your committed changes from your local repository to the remote repository. In the reverse direction, you can retrieve any new changes (commits/branches) from the remote repository into your local repository. The typical workflow now includes one step: you interact with the remote repository.

---

## Commit

We heard that changes will be committed to the repository. So, what is a commit?

A commit is a snapshot of the entire project at a specific point in time. It's not just a record of what changed; it's a complete picture of every file and folder in the repository exactly as they were when we made the commit. A commit is identified by its SHA-1 hashed identifier.

[![](https://substackcdn.com/image/fetch/$s_!OfCf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc27869d-d516-4511-b0e6-56b49519119b_754x312.png)](https://substackcdn.com/image/fetch/$s_!OfCf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc27869d-d516-4511-b0e6-56b49519119b_754x312.png)

This snapshot is created from the files in the staging area. The commit actions record new versions for these staged files in the local repository's history. If files don’t have changes, Git only needs to store the links to the files in the previous commits.

Besides the snapshot, a commit also has the metadata:

* The name and email of the one who made the commit.
* A unique identifier that is calculated from the SHA-1 hash.
* A timestamp
* A commit message
* A pointer to the parent. A regular commit has one parent, and a merge commit could have more than one parent.

[![](https://substackcdn.com/image/fetch/$s_!f40z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5558e0f-c0ed-440d-b1e7-65a0b618b88f_780x294.png)](https://substackcdn.com/image/fetch/$s_!f40z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5558e0f-c0ed-440d-b1e7-65a0b618b88f_780x294.png)

---

## Branch

Git branches allow for parallel development.

As mentioned, a commit has a pointer to its parent commit(s). A Git branch is simply a movable pointer to a commit. When creating the repository for the first time, a default branch will be created.

Creating a new branch from an existing branch only creates a new pointer that points to the latest commit of the existing branch. As a result, the branch creation process in Git is extremely lightweight.

[![](https://substackcdn.com/image/fetch/$s_!TsB5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F941cdcd5-1fd8-4536-a0ae-c1ceae140564_1364x404.png)](https://substackcdn.com/image/fetch/$s_!TsB5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F941cdcd5-1fd8-4536-a0ae-c1ceae140564_1364x404.png)

Git keeps a special pointer called `HEAD` (it points to the current branch pointer) to identify the current commit you’re working on. Also, when we make changes or create new commits, Git uses `HEAD` to know where those new commits should be added.

[![](https://substackcdn.com/image/fetch/$s_!mp8g!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafd74502-7132-408b-8a10-7fc15f9adea0_1212x328.png)](https://substackcdn.com/image/fetch/$s_!mp8g!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafd74502-7132-408b-8a10-7fc15f9adea0_1212x328.png)

---

## Summary before moving on

We’ve learned that Git is a distributed version control system, where each client can have their repo on their laptop. Git tracks your file changes locally in three sections: the working directory, the staging area, and the local repository.

A commit is a snapshot of the entire project at a specific point in time. A commit has a pointer that points to its parent commit. A branch is simply a movable pointer to a commit. We can share your work or get updates from others by interacting with the remote repository.

Next, we will delve into some Git commands to gain a deeper understanding of what happens behind the scenes. Imagine a scenario where a team is working on a project called Boring1.

---

## Git clone

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=167413589)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

Clark created a repository on GitHub called Boring1 with a default branch named `main` and an empty README file. Then, Clark clones it to his laptop.

> git clone <remote-repo-url>

Clark will have a folder named Boring1 at local. The folder will have a sub-folder called **.git**, which is Clark’s local repository.

[![](https://substackcdn.com/image/fetch/$s_!-37E!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28bc5f02-7613-43fe-b3a1-aacdc9ea2ef4_308x228.png)](https://substackcdn.com/image/fetch/$s_!-37E!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28bc5f02-7613-43fe-b3a1-aacdc9ea2ef4_308x228.png)

Behind the scenes, there is a `main` branch pointer that points to a commit that created the README.md file. The HEAD pointer is pointing to the `main` pointer.

[![](https://substackcdn.com/image/fetch/$s_!U3N7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1de992a0-629b-44ce-aaf6-b2eefb63417e_648x382.png)](https://substackcdn.com/image/fetch/$s_!U3N7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1de992a0-629b-44ce-aaf6-b2eefb63417e_648x382.png)

> *There is another way Clark can create a project. He could create a folder named "Boring1" on his laptop first and run `git init` inside it.*

## Git log

Clark can also check the commit history by running:

> git log

If no parameter is provided, Clark will see the commit history of the current branch. Clark can check the history of a different branch by adding the <branch-name> parameter.

## Git branch

Clark wants to add a feature (add a file `file\_1.py`). To ensure that he doesn’t mess up the main branch, Clark created a branch called `feat/feature\_1`

> git branch <branch\_name>

Under the hood, there is a new branch pointer called `feat/feature\_1`. This pointer also points to the same commit as the main branch pointer.

[![](https://substackcdn.com/image/fetch/$s_!pdpn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd97f48ab-a017-4853-b5fe-d175930c9e66_512x354.png)](https://substackcdn.com/image/fetch/$s_!pdpn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd97f48ab-a017-4853-b5fe-d175930c9e66_512x354.png)

## Git switch

However, Clark only creates the new branch. He is still on the `main` branch. He needs to switch to `feat/feature\_1`.

> git switch <branch\_name>

Behind the scenes, the HEAD pointer is now pointing to the `feat/feature\_1` pointer.

[![](https://substackcdn.com/image/fetch/$s_!sp4s!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbcc3c774-743a-4298-b51b-edc02dcf64c5_546x384.png)](https://substackcdn.com/image/fetch/$s_!sp4s!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbcc3c774-743a-4298-b51b-edc02dcf64c5_546x384.png)

## Git checkout

Clark learns that he can switch to a different branch using `git checkout`. Compared to `git switch`, `git checkout` is older and more versatile.

* Clark can switch to a branch by making the HEAD pointer point to the desired branch.

  > git checkout <branch-name>
* Clark can also create a new branch and move the HEAD to the new branch in a single command:

  > git checkout -b <branch-name>
* Or, more advanced, Clark can move the HEAD to a specific commit, instead of the branch’s latest commit;

  > git checkout <commit-hash>

Confession: I always use `git checkout` 😉

## Git status

After switching on `feat/feature\_1`. Clark creates a new file called `file\_1.py`

Clark ran git status to check the state of the working directory and the staging area.

> git status

Clark sees this:

[![](https://substackcdn.com/image/fetch/$s_!JBlu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd91200d-5ec5-4212-b56e-67efc95d7717_1256x322.png)](https://substackcdn.com/image/fetch/$s_!JBlu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd91200d-5ec5-4212-b56e-67efc95d7717_1256x322.png)

Git sees that Clark created the `file\_1.py` file. However, it’s currently in `untracked` status because Git doesn’t recognize this file in the last commit.

[![](https://substackcdn.com/image/fetch/$s_!58yp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6ff57b0-5c7f-4d0b-9f82-233576fc9e47_724x282.png)](https://substackcdn.com/image/fetch/$s_!58yp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6ff57b0-5c7f-4d0b-9f82-233576fc9e47_724x282.png)

## Git add

Clark wants to include `file\_1.py` in the upcoming commit. Clark runs `git add file\_1.py` to move this file to the staging area.

> git add <files/dirs to be added>

Clark can also run `git add .` to add all the changes in the current directory (in this case, the `file\_1.py`) to the staging area.

Run `git status` again, the file is tracked and staged:

[![](https://substackcdn.com/image/fetch/$s_!Tk6k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffffd3688-be92-497a-922c-8229ccf90c39_610x202.png)](https://substackcdn.com/image/fetch/$s_!Tk6k!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffffd3688-be92-497a-922c-8229ccf90c39_610x202.png)

[![](https://substackcdn.com/image/fetch/$s_!mOJh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee76c178-096d-4f75-94e2-e641a077644d_696x304.png)](https://substackcdn.com/image/fetch/$s_!mOJh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee76c178-096d-4f75-94e2-e641a077644d_696x304.png)

## Git commit

Then, Clark committed this change to the local repo:

> git commit -m <message>

The file is now in `committed` state and persisted in the local repository.

[![](https://substackcdn.com/image/fetch/$s_!k2ju!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69dbcd77-a004-4767-9885-ea816ecbea35_784x356.png)](https://substackcdn.com/image/fetch/$s_!k2ju!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69dbcd77-a004-4767-9885-ea816ecbea35_784x356.png)

Behind the scenes, a new commit object is created. Its pointer points to the previous commit. The branch pointer `feat/feature\_1` points to the latest commit.

[![](https://substackcdn.com/image/fetch/$s_!l5uN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6ef4092-d275-40b3-b093-6dda3f6931f5_692x348.png)](https://substackcdn.com/image/fetch/$s_!l5uN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6ef4092-d275-40b3-b093-6dda3f6931f5_692x348.png)

## Git push

Clark wants to update this change to the remote repo; he ran:

> git push

[![](https://substackcdn.com/image/fetch/$s_!BYiU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31bd9122-aacc-4afe-a648-7174fa7ccf00_432x222.png)](https://substackcdn.com/image/fetch/$s_!BYiU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31bd9122-aacc-4afe-a648-7174fa7ccf00_432x222.png)

In the first push, Clark needs to run `**git push --set-upstream origin feat/feature\_1**` to set the remote-tracking branch for `feat/feature\_1`

A remote-tracking branch is a **local pointer** to the state of a remote branch. Unlike a regular branch pointer, we can’t move it. Git moves this pointer for us when we interact with the remote repo.

It informs Clark of the current status of the remote `feat/feature\_1` since the last update. In this case, it was an empty one as Clark only created `feat/feature\_1` locally.

Remote-tracking branch’s name has the pattern `<remote>/<branch-name>`. Where <branch-name> is the associated local branch’s name, and `<remote>` has `origin` as the default.

[![](https://substackcdn.com/image/fetch/$s_!Osai!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4aae2f9c-c2a4-4cd5-b7cb-0bdefa9e2598_806x638.png)](https://substackcdn.com/image/fetch/$s_!Osai!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4aae2f9c-c2a4-4cd5-b7cb-0bdefa9e2598_806x638.png)

When Clark does the `git push`, Git updates the remote-tracking pointer and retrieves the changes from Clark’s laptop (`file\_1.py`)

## Git merge

After doing the new feature, Clark wants to merge the changes from `feat/feature\_1` to `main`

Clark switches back to `main`:

> git checkout <branch-name>
>
> In this case, branch-name = main

, and merge `feat/feature\_1` to `main`:

> git merge <branch-name>
>
> In this case, branch-name = feat/feature\_1.
>
> If the <branch-name> is omitted, Git will try to merge the associated remote tracking branch to the working branch.

This will merge changes from `feat/feature\_1` to `main`. In this scenario, when we are working on the `feat/feature\_1`, there have been **no additional commits** on the main since then. Git simply moves the `main` pointer to the latest commit of `feat/feature\_1`. This is called **fast forward merge**.

[![](https://substackcdn.com/image/fetch/$s_!xlQm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f897615-9f21-425c-a4b4-e8be52960fc4_816x352.png)](https://substackcdn.com/image/fetch/$s_!xlQm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f897615-9f21-425c-a4b4-e8be52960fc4_816x352.png)

However, in a different scenario, a new commit on `main` occurs during the time we have been working with `feat/feature\_1`, we say `main` and `feat/feature\_1` **are diverged**.

[![](https://substackcdn.com/image/fetch/$s_!QXf3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3c04892-4511-465d-bdf7-99afbf55c9b9_544x314.png)](https://substackcdn.com/image/fetch/$s_!QXf3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3c04892-4511-465d-bdf7-99afbf55c9b9_544x314.png)

Git will execute the **three-way merge**. It will create a new commit that combines work from two branches. The new commit has two parents: the `main` latest commit and the `feat/feature\_1` latest commit.

[![](https://substackcdn.com/image/fetch/$s_!sMAF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F34d98186-ec32-47a1-a20b-ee89e020dfa0_702x284.png)](https://substackcdn.com/image/fetch/$s_!sMAF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F34d98186-ec32-47a1-a20b-ee89e020dfa0_702x284.png)

After the main is merged into the local repository. Clark can update the remote `main` by `git push`.

**Note 1**: In a real project, most merges to the production branch will be carried out through merge requests on a platform like GitHub or GitLab. It facilitates the team collaboration process with a nice UI that shows what changes are going to be merged. When Clark clicks the `merge` button on the UI, things will be the same as we run `git merge`

**Note 2**: Additionally, in a real project, not every merge command will succeed; conflicts will arise when changes to the same content occur in both branches. It is our responsibility to resolve these conflicts.

## Git fetch

Back to the current Boring1 project. After merging `feat/feature\_1` to `main` and pushing it to the remote `main`, the local and remote versions of `main` are in sync.

[![](https://substackcdn.com/image/fetch/$s_!fmSV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23b4406b-e64a-4dc1-a10d-a190eb7d3389_700x552.png)](https://substackcdn.com/image/fetch/$s_!fmSV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23b4406b-e64a-4dc1-a10d-a190eb7d3389_700x552.png)

However, at a given time in the future, Bruce, Clark’s teammate, creates a merge request and adds a new commit to `main` on the remote repo. Clark’s local `main` is outdated compared to the remote `main`.

[![](https://substackcdn.com/image/fetch/$s_!Ws8F!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F024b15bd-3b8f-423e-ab87-b4484745db93_824x636.png)](https://substackcdn.com/image/fetch/$s_!Ws8F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F024b15bd-3b8f-423e-ab87-b4484745db93_824x636.png)

Clark can get the remote update by running

> git fetch
>
> Clark can add `<branch-name>` param for `git fetch` to fetch changes from a different remote branch.
>
> If this Clark doesn’t provide any parameters for this command, git will fetch from the associated remote tracking branch; in this case, it is `origin/main`

[![](https://substackcdn.com/image/fetch/$s_!AgiR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6874b2f6-737e-47be-8e8b-9bbe4aae9a76_688x614.png)](https://substackcdn.com/image/fetch/$s_!AgiR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6874b2f6-737e-47be-8e8b-9bbe4aae9a76_688x614.png)

Git checks if there is an update from the remote repository; if so, it downloads new data from the remote repository and updates the remote tracking branch, `origin/main`. Clark’s local `main` is untouched.

To merge updates to the local `main`, Clark can run:

> git merge

…, which merges changes from the remote tracking branch, `origin/main`

[![](https://substackcdn.com/image/fetch/$s_!DfNr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5194b0d2-957e-4e4d-b0a5-03dd6a499543_686x380.png)](https://substackcdn.com/image/fetch/$s_!DfNr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5194b0d2-957e-4e4d-b0a5-03dd6a499543_686x380.png)

## Git pull

This is a more aggressive version of the `git fetch`.

> git pull
>
> Clark can add `origin + <branch-name>` to pull from a different remote branch. For example: `git pull origin main`
>
> If this Clark doesn’t provide any parameters for this command, git will pull from the associated remote tracking branch; in this case, it is `origin/main`

Behind the scenes, `git pull` performs fetching changes, similar to `git fetch`; however, it automatically merges these changes into the local `main` branch.

[![](https://substackcdn.com/image/fetch/$s_!HSjR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb7e7c68-f568-4751-88f9-6c728c7c2888_702x600.png)](https://substackcdn.com/image/fetch/$s_!HSjR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb7e7c68-f568-4751-88f9-6c728c7c2888_702x600.png)

## Git revert

Now, the current local `main` has three commits: the first that added README.md, the next two added `file\_1.py` and `file2.py`

[![](https://substackcdn.com/image/fetch/$s_!Jo8w!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdc36c48-1ad7-4f05-9c8f-470468b8c25e_634x264.png)](https://substackcdn.com/image/fetch/$s_!Jo8w!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdc36c48-1ad7-4f05-9c8f-470468b8c25e_634x264.png)

Clark wants to create a new feature, so he checks out to a new branch from the local `main` called `feat/feature\_3`.

[![](https://substackcdn.com/image/fetch/$s_!sNCI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93a1dd00-6635-4107-a412-29d531570404_858x324.png)](https://substackcdn.com/image/fetch/$s_!sNCI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93a1dd00-6635-4107-a412-29d531570404_858x324.png)

On `feat/feature\_3`, he created `file\_3.py` and committed it to the local repo. He also added another commit right after that to create `file\_4.py`.

[![](https://substackcdn.com/image/fetch/$s_!I-J3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb613ae90-704a-4f1c-8625-9dc6e1a0be09_1046x330.png)](https://substackcdn.com/image/fetch/$s_!I-J3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb613ae90-704a-4f1c-8625-9dc6e1a0be09_1046x330.png)

However, Clark soon realizes that the commit that adds `file\_3.py` is a mistake, and he wants to undo it. He can run the following command

> git revert <commit>

Git will record the changes from this commit and create a new commit that does the ***opposite (remove file\_3.py)***

[![](https://substackcdn.com/image/fetch/$s_!TFwt!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F452f4f65-1163-4af2-8145-3ffcba4d5f2c_1588x490.png)](https://substackcdn.com/image/fetch/$s_!TFwt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F452f4f65-1163-4af2-8145-3ffcba4d5f2c_1588x490.png)

Thus, this new commit will remove the `file\_3.py`. The cool thing about `git revert` is that it maintains the commit history.

## Git reset

Clark can also remove the commit that adds file 3, with `git reset`. However, this action requires more caution than `git revert`, as it will modify the commit history.

> git-revert <commit>

Git will move the HEAD pointer to the desired commit and delete all commits after it from the commit history. Because the commit that adds `file\_3.py` was a mistake, Clark wants to revert to the commit that adds `file\_2.py`.

This command can be run in different modes:

* --soft:

  [![](https://substackcdn.com/image/fetch/$s_!tQP1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c96e961-8724-41a9-8977-82ede83caa0a_1018x818.png)](https://substackcdn.com/image/fetch/$s_!tQP1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c96e961-8724-41a9-8977-82ede83caa0a_1018x818.png)

  + Git moves the HEAD pointer back to the commit that adds `file\_2.py`.
  + Commits that add `file\_3.py` and `file\_4.py` are clear from the commit history.
  + All changes from these commits **are in the staging area**.
  + The changes (`file\_3.py` and `file\_4.py`) still present in the working dir.
* --mixed (default):

  [![](https://substackcdn.com/image/fetch/$s_!mYdJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ed7e3f7-99bb-41e4-b511-9d45a0dd9107_910x712.png)](https://substackcdn.com/image/fetch/$s_!mYdJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ed7e3f7-99bb-41e4-b511-9d45a0dd9107_910x712.png)

  + Git moves the HEAD pointer back to the commit that adds `file\_2.py`.
  + Commits that add `file\_3.py` and `file\_4.py` are clear from the commit history.
  + All changes from these **are no longer staged**
  + The changes (`file\_3.py` and `file\_4.py`) are still present in the working dir
* --hard (be careful):

  [![](https://substackcdn.com/image/fetch/$s_!YQd9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08cf4dd1-a4bc-42f9-82f3-78b23f6dea67_900x716.png)](https://substackcdn.com/image/fetch/$s_!YQd9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08cf4dd1-a4bc-42f9-82f3-78b23f6dea67_900x716.png)

  + Git moves the HEAD pointer back to the commit that adds `file\_2.py`.
  + Commits that add `file\_3.py` and `file\_4.py` are clear from the commit history.
  + All changes from these **are no longer staged**
  + The changes are also **no longer in the working directory**.

Due to the modification of the commit history, the commit that adds `file\_4.py` will be affected. This differs from `git revert`, as it preserves the commit history, leaving the commit that adds `file\_4.py` untouched.

## Git cherry-pick

For easier to follow, let’s imagine that Clark doesn’t see the `file\_3.py` is the mistake, the commit history still has five commits:

[![](https://substackcdn.com/image/fetch/$s_!I-J3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb613ae90-704a-4f1c-8625-9dc6e1a0be09_1046x330.png)](https://substackcdn.com/image/fetch/$s_!I-J3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb613ae90-704a-4f1c-8625-9dc6e1a0be09_1046x330.png)

At the same time, Bruce has created a new branch `feat/feature\_from\_bruce` and made a new commit that creates a `file\_5.py

[![](https://substackcdn.com/image/fetch/$s_!p_za!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdec6ba4e-f0be-4937-962a-44e11f51814f_1236x400.png)](https://substackcdn.com/image/fetch/$s_!p_za!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdec6ba4e-f0be-4937-962a-44e11f51814f_1236x400.png)

Clark needs the `file\_5.py` in the `feat/feature\_3` to continue developing. Clark can do this with

> git cherry-pick <commit>

This command enables Clark to select a specific commit from a branch and apply it to the current working branch. Clark runs `git log feat/feature\_from\_bruce` to retrieve the ID of the commit that adds `file\_5.py`.

[![](https://substackcdn.com/image/fetch/$s_!NVLS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5a0e9bd-941e-4879-b1b8-62fe6c6452d2_1450x856.png)](https://substackcdn.com/image/fetch/$s_!NVLS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5a0e9bd-941e-4879-b1b8-62fe6c6452d2_1450x856.png)

Then, Clark runs `git cherry-pick <id-of-commit that-adds-file\_5.py>`. Behind the scenes, Git will create a new commit that incorporates the changes from this chosen commit with the same commit message.

## Git stash

From the beginning, we’ve learned that the only way to clean the working directory is by committing the changes to the local repo.

However, Git has a command that lets Clark save current working changes in a temporary location without committing them by running:

> git stash save <optional message>

[![](https://substackcdn.com/image/fetch/$s_!Yhe8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54a2e0ab-720f-4e70-a135-c61c40355ee6_1010x654.png)](https://substackcdn.com/image/fetch/$s_!Yhe8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54a2e0ab-720f-4e70-a135-c61c40355ee6_1010x654.png)

This will save the current modified and staged files in a temporary location. **Untracked files are not included**. Clark can later reapply the changes by running

> git stash apply <optional-index>

If the index is not provided, Git will apply the latest stash.

---

## Outro

Thank you for reading this far.

In this article, we explore the difference between centralized and distributed version control systems, Git overview, the tree man sections: working directory, staging area, local repo, and then we move to remote repo, what the commit and branch are, then we explore how common Git commands work under the hood.

If you would like to discuss further, please feel free to leave a comment.

Now, see you in my next article.

P.S. 1: There are undoubtedly many more Git commands available; however, I believe the fundamentals presented in this article are sufficient for us to understand what a given Git command does under the hood.

---

## Reference

[1] [Official Git Book](https://git-scm.com/book/en/v2)
