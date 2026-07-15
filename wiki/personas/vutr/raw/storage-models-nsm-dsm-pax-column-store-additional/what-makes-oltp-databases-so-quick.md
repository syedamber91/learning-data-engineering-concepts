---
title: "What Makes OLTP Databases So Quick at Finding Your Data?"
channel: vutr
author: "Vu Trinh"
published: 2025-10-09
url: https://vutr.substack.com/p/what-makes-oltp-databases-so-quick
paid: false
topics: ["Data Engineering", "Apache Airflow"]
tags: [https, auto, node, tree, substackcdn, image]
---

# What Makes OLTP Databases So Quick at Finding Your Data?

*Things you need to know about the most used data structure for optimizing query performance in SQL OLTP database, the B-Tree (more specifically, B+Tree)*

> Source: [Open post](https://vutr.substack.com/p/what-makes-oltp-databases-so-quick)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]]

---

> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!34PV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2520b76-3146-4acf-bd21-886e47668ebd_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!34PV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2520b76-3146-4acf-bd21-886e47668ebd_2000x1428.png)

---

## Intro

As a data engineer, I did not spend a lot of time working with an OLTP database, such as PostgreSQL. I’m aware that to make data operations fast in a database, there must be techniques to boost the performance of the typical workload that the database supports. For OLAP systems, the ultimate goal is to prune the data as much as possible.

For OLTP systems, the goal is to find a record as fast as possible.

But how do they do that?

In this article, we will delve into the most popular technique for optimizing query performance in databases such as PostgreSQL and MySQL: the B-Tree. We first learn the basics of the tree data structure in memory and utilize that knowledge to build up our understanding of the B-Tree.

## The tree

In computer science, a tree models a hierarchical structure. Data is arranged in **nodes** that are linked hierarchically. The following terminologies define any tree structure:

[![](https://substackcdn.com/image/fetch/$s_!WjXv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0b5dbe9-4316-4902-b8dc-ed3f54978949_776x382.png)](https://substackcdn.com/image/fetch/$s_!WjXv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0b5dbe9-4316-4902-b8dc-ed3f54978949_776x382.png)

* **Node:** A unit that potentially stores two things: data and pointers (leaf nodes don’t have pointers) to other nodes.
* **Root:** The tree’s topmost node, and it doesn’t have any parent. The tree will bloom from here.
* **Leaf nodes:** The ones that don’t have any children.
* **Internal Nodes:** These connect the Root and Leaves. They have at least one child.
* **Parent, Child, Subling:** If a node A points to two nodes B and C. A is the parent of B and C, while B and C are A’s children. Nodes with the same parent are called siblings

  [![](https://substackcdn.com/image/fetch/$s_!XXZ0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07039717-4242-488e-b165-7f0835f0accb_362x372.png)](https://substackcdn.com/image/fetch/$s_!XXZ0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07039717-4242-488e-b165-7f0835f0accb_362x372.png)
* **Height:** The tree’s **height** is the longest path from the root to any leaf node.
* **Subtree**: Any node in a tree can be considered the **root of a subtree**. All the nodes below it, including its children, grandchildren, and so on, form a smaller tree.

  [![](https://substackcdn.com/image/fetch/$s_!TJY1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbc9ed2e-0e69-4f9f-a38c-97647d9a88c7_870x568.png)](https://substackcdn.com/image/fetch/$s_!TJY1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbc9ed2e-0e69-4f9f-a38c-97647d9a88c7_870x568.png)
* **Depth:** The **depth** of a specific node is the path’s length from the root to that node. That said, the root node is at depth 0.

## The binary tree

Data structures are designed to facilitate the storage and retrieval of data in a manner that suits specific use cases. The **Binary Search Tree (BST)** is a specialized form that provides the binary search property.

For those unfamiliar with binary search, it is an algorithm that compares the searched value to the middle element of the ordered array. Because the data is sorted, the system can eliminate half of the search space. The process is then continued recursively with the remaining half until the system finds the searched value.

For example, given the sorted array [1,2,6,7,8,9,10]. When searching for the value 10, the system first compared it with the middle (7) and saw that the target value is greater than 7, so it can safely skip the left half because it knows for sure that those values will be less than 7, so it is impossible for the 10 to exist in the left half.

[![](https://substackcdn.com/image/fetch/$s_!W2uP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F45164353-0f4e-4382-b9a2-71bae6112fcd_588x330.png)](https://substackcdn.com/image/fetch/$s_!W2uP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F45164353-0f4e-4382-b9a2-71bae6112fcd_588x330.png)

Consequently, the search process has an average-case time complexity of O(logn). The importance here is that the array must be sorted.

Back to the BST, it offers the binary search property by these constraints:

* Each node has at most two children

  [![](https://substackcdn.com/image/fetch/$s_!DL3X!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6940c0b8-a5ac-4c4c-9279-fe7c6ab5d451_578x340.png)](https://substackcdn.com/image/fetch/$s_!DL3X!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6940c0b8-a5ac-4c4c-9279-fe7c6ab5d451_578x340.png)

* All nodes in the left subtree of a node are less than that node.

  [![](https://substackcdn.com/image/fetch/$s_!i8I5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b3b38c8-ab24-4624-8510-7094c5b1700f_768x484.png)](https://substackcdn.com/image/fetch/$s_!i8I5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b3b38c8-ab24-4624-8510-7094c5b1700f_768x484.png)
* All nodes in the right subtree of a node are greater than that node.

This strict ordering enables the system to perform a search algorithm similar to the one on a sorted array described above.

Instead of starting in the middle in the case of a sorted array, one begins with the root of the tree, compares the searched value with the current node's value, and recursively moves down into the left subtree if the target is smaller or the right subtree if it is larger. This process continues until the key is found (or it finally finds that the value is not in the tree).

[![](https://substackcdn.com/image/fetch/$s_!QVjF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc584b73f-9baf-41b9-915d-516ce848a2be_1010x634.png)](https://substackcdn.com/image/fetch/$s_!QVjF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc584b73f-9baf-41b9-915d-516ce848a2be_1010x634.png)

I used to wonder why we don’t just use the array structure for the binary search property. The answer is simple: an array can provide that property for read operations, but adding or removing data still has O(n) complexity.

[![](https://substackcdn.com/image/fetch/$s_!kKIP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff99a9563-5389-4c1d-bdb8-acef3f6ebf69_740x290.png)](https://substackcdn.com/image/fetch/$s_!kKIP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff99a9563-5389-4c1d-bdb8-acef3f6ebf69_740x290.png)

That is because an array requires shifting the data to ensure it is stored continuously in memory when we add or remove an array’s item at the beginning or middle of the array.

BST offers the property of the binary search for both data read and write operations. The trade-off is that managing the BST is more complicated, specifically in ensuring that adding or removing data still adheres to the BST constraints.

---

[![](https://substackcdn.com/image/fetch/$s_!up3R!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F45c0412c-1746-4614-85e9-b496fa229a48_600x200.png)](https://www.astronomer.io/events/webinars/airflow-3-1-release-video/?utm_source=vu-trinh&utm_medium=paidmedia&utm_campaign=webinar-airflow-3-1-10-25)

**This article is sponsored by Astronomer.** Airflow 3.1 is here, building on the milestone 3.0 release with powerful new features that broaden Airflow’s use cases and make everyday workflows simpler and more efficient for users.

Join Astronomer on **[October 22 at 11am EST/4pm BST](https://www.astronomer.io/events/webinars/airflow-3-1-release-video/?utm_source=vu-trinh&utm_medium=paidmedia&utm_campaign=webinar-airflow-3-1-10-25)** for a live walkthrough of features you won’t want to miss, like human-in-the-loop controls, an expanded plugins interface for React, and UI improvements.

[Register Now](https://www.astronomer.io/events/webinars/airflow-3-1-release-video/?utm_source=vu-trinh&utm_medium=paidmedia&utm_campaign=webinar-airflow-3-1-10-25)

---

### Balance

However, following the constraints does not entirely guarantee the O(logn) for operations; another important factor is that the tree must be balanced. In an ideally balanced tree, where the left and right subtrees of every node have roughly the same number of nodes, this allows search, insertion, and deletion operations to have an average-case time complexity of O(log n), as each comparison effectively halves the remaining search space.

[![](https://substackcdn.com/image/fetch/$s_!HRGG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb02ff766-ce0f-4f00-90e4-120764b4be98_480x566.png)](https://substackcdn.com/image/fetch/$s_!HRGG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb02ff766-ce0f-4f00-90e4-120764b4be98_480x566.png)

Just imagine a tree with a root with the value of 10. The left subtree contains only one value (9), whereas the right subtree comprises more than 20 values (ranging from 11 to 30). Consequently, searching for a value greater than 10 necessitates the system to traverse nearly every record in the tree. The benefit of a binary search property is gone.

There are some BST implementations that can be self-balanced, such as the [AVL tree](https://en.wikipedia.org/wiki/AVL_tree#:~:text=November%202021),done%20to%20restore%20this%20property.) or the [Red-black tree](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree). For the scope of this article, I won’t delve too much into the details of these implementations.

Just keep this in mind when we move on to explore the B-Tree, as balancing is the key to optimizing the tree’s performance.

## A binary tree doesn’t work well on disk.

The binary search property for both read and write operations is an attractive feature for many applications, including databases, particularly relational databases such as PostgreSQL, where most of the workload involves reading and writing a single record as quickly as possible.

[![](https://substackcdn.com/image/fetch/$s_!Zjgo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70933a9a-3431-43f1-bcff-755272575975_324x230.png)](https://substackcdn.com/image/fetch/$s_!Zjgo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70933a9a-3431-43f1-bcff-755272575975_324x230.png)

However, BST is designed to work on memory. Following the pointer to a node’s location is fast, given that memory is fast at random access.

Random access on disk is another story.

The transition from in-memory data structures to those designed for hard disk drives (HDDs) or solid-state drives (SSDs) requires a fundamental paradigm shift.

The main challenge is the latency gap between main memory and disk. RAM access is measured in nanoseconds, whereas a seek operation on an HDD can take milliseconds—a difference of four to five orders of magnitude. Even with modern SSDs, which eliminate mechanical seek times, the latency is still measured in microseconds, making disk access much slower than RAM access.

Thus, the goal here is to **minimize the number of disk I/O operations**.

In addition, disks operate on a block-oriented basis. When reading or writing to disk, it involves transferring data in fixed-size chunks called blocks (e.g., 4 KB, 8 KB, or 16 KB). An efficient data structure built on disk must therefore align itself with this access pattern, aiming to extract the maximum possible value from each page it reads from the disk.

Now you can see why BST on disk is a problem here.

[![](https://substackcdn.com/image/fetch/$s_!RgRk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14361b08-bf0e-41c7-a23b-05a6c6a948e5_598x546.png)](https://substackcdn.com/image/fetch/$s_!RgRk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14361b08-bf0e-41c7-a23b-05a6c6a948e5_598x546.png)

Each node stores a single value and two pointers to its children, given a balanced BST with a height of 20. To find an item, we would have to traverse down the tree, following one pointer at a time. This could mean **up to 20 separate disk reads**, as each node might be in a different, non-contiguous block on the disk.

[![](https://substackcdn.com/image/fetch/$s_!Lnur!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feed353ce-cd84-44b7-b173-153f1fd061a3_550x292.png)](https://substackcdn.com/image/fetch/$s_!Lnur!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feed353ce-cd84-44b7-b173-153f1fd061a3_550x292.png)

In addition, because a node contains only a small amount of data (data and two pointers, totaling a few dozen bytes), representing a node using an entire disk block wastes the storage and I/O bandwidth.

## B-Tree

Given that most relational databases store data on disk, they need an improvement over the BST. Here comes the B-Tree.

[![](https://substackcdn.com/image/fetch/$s_!ECML!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27acd693-2aab-4540-9215-3e1b7b3fa394_478x262.png)](https://substackcdn.com/image/fetch/$s_!ECML!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27acd693-2aab-4540-9215-3e1b7b3fa394_478x262.png)

It was introduced in the 1970s and has become ubiquitous since then. It is a self-balancing search tree that generalizes the BST by allowing each node to contain many keys and have many children. A node now stores more data, which aligns with the disk block-based layout, ensuring that each I/O operation is as productive as possible.

B-Tree splits the database into fixed-size pages. One page is read or written at a time. The page size (e.g., [PostgreSQL page size is 8 KB](https://www.postgresql.org/docs/current/storage-page-layout.html#STORAGE-PAGE-LAYOUT)) must align with the disk block size to ensure disk access performance.

> ***Note**: I will use `page` and `node` interchangeably from there to refer to a node in the B-Tree.*

## Anatomy

In the classic B-Tree implementation, the data can be stored in non-leaf nodes. In the variant B+ Tree, only the leaf nodes hold the data.

[![](https://substackcdn.com/image/fetch/$s_!bAmi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faff45092-ce4e-4b38-96cf-457b7f93eb66_962x322.png)](https://substackcdn.com/image/fetch/$s_!bAmi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faff45092-ce4e-4b38-96cf-457b7f93eb66_962x322.png)

This enables all data operations to focus solely on the leaf nodes. B+ Tree has been widely adopted and is usually referred to as the B-Tree. The remainder of this article describes the implementation of the B+ Tree, where data is stored exclusively in the leaves.

There is an essential factor in B+Trees called the tree fall-out, called **M**, which indicates the maximum number of children that a page can point to. Every node will have the maximum **N** keys, where **N = M -1**. Also, a node must have at least **N/2** keys to ensure that nodes are at least half-full, avoiding wasted space and maintaining an efficient structure.

Like a general tree, a B+ Tree also has:

[![](https://substackcdn.com/image/fetch/$s_!N52E!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9f56faf-abec-43ad-9e74-5ccb04f5dae0_1132x436.png)](https://substackcdn.com/image/fetch/$s_!N52E!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9f56faf-abec-43ad-9e74-5ccb04f5dae0_1132x436.png)

* A root node: every data operation must start here.

  [![](https://substackcdn.com/image/fetch/$s_!u5si!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd86e07c1-531c-42d2-a460-4753293b4b07_360x222.png)](https://substackcdn.com/image/fetch/$s_!u5si!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd86e07c1-531c-42d2-a460-4753293b4b07_360x222.png)
* Leaf nodes store the pointer to actual data. In more detail, they store key-value pairs; the keys are the index column values, and the values are pointers to actual data.
* Internal nodes link the root and leaves together.

For non-leaf (root and internal) nodes, they store:

[![](https://substackcdn.com/image/fetch/$s_!s9Xx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbcd3be4e-31eb-491e-8f9a-7752d70a1564_1026x306.png)](https://substackcdn.com/image/fetch/$s_!s9Xx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbcd3be4e-31eb-491e-8f9a-7752d70a1564_1026x306.png)

* The keys, which are the index column values. A non-leaf node will have a continuous range of sorted keys (sorting to enable binary searching).
* The pointers that point to other nodes.
* The number of pointers is equal to the number of keys + 1.
* The pointer will point to a subtree that has keys in the range of [ key\_left, key\_right)

[![](https://substackcdn.com/image/fetch/$s_!S3hf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b63ff6a-c03a-40d3-a6e7-67766ac38aeb_976x186.png)](https://substackcdn.com/image/fetch/$s_!S3hf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b63ff6a-c03a-40d3-a6e7-67766ac38aeb_976x186.png)

The data operations boil down to finding the required data node. Reading and updating data are similar processes. In more detail, the process looks like this:

[![](https://substackcdn.com/image/fetch/$s_!pEQs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23a1b8bd-bd1b-47f2-89be-4339e84bc157_790x462.png)](https://substackcdn.com/image/fetch/$s_!pEQs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23a1b8bd-bd1b-47f2-89be-4339e84bc157_790x462.png)

* A query with a filter on the index column, it could be a point look-up or range filter (=, <, >, between), such as fetching a customer by their ID. (This query is ubiquitous in OLTP workload)
* A search operation begins at the root node of the tree.
* The database compares the search value against the keys stored in the node to determine which child pointer to follow.
* This process is repeated, descending one level at a time, until it reaches the leaf node that has the required data.

## The node is full

As we discussed, inserting involves searching for the required leaf node by visiting the root and then following the descendant pointers. The system can then insert the new key if the node has available space. However, a challenge arises when a node is full; an inserter key causes it to exceed the maximum number of keys, N. This behavior is usually referred to as overflow.

To solve this:

* A new node is created with the maximum capacity of N.
* Data from the position (N/2) + 1 in the overflow node will be moved to the newly created node.

Then, the system adds the associated key and pointer in the parent node. This behavior depends on whether the overflow node is the leaf node or not:

* If it is a leaf node, the first key from the new node will be copied to the parent node.

  [![](https://substackcdn.com/image/fetch/$s_!XV_p!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8586367-086a-451a-8001-38f779d5247c_1340x504.png)](https://substackcdn.com/image/fetch/$s_!XV_p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8586367-086a-451a-8001-38f779d5247c_1340x504.png)
* If it is a non-leaf node, the first key from the new node **will be moved** to the parent node.

[![](https://substackcdn.com/image/fetch/$s_!oLuN!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc931f19-6a03-4ab4-b3e9-53144f97e9ec_1144x396.png)](https://substackcdn.com/image/fetch/$s_!oLuN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc931f19-6a03-4ab4-b3e9-53144f97e9ec_1144x396.png)

In the case of the leaf node, by copying this key up to the parent, that key now serves as a navigational guide. The parent says, "Anything less than the key goes to my left child, and anything greater than or equal to the key goes to my right child."

In the case of the internal node, moving this key up to the parent acts as a partition. It no longer needs to exist at the child level, as its sole purpose was to divide the keys that are now in two separate nodes. Since there are no data pointers at this level, moving the key doesn't risk losing access to any data.

If the parent nodes also overflow, they must be split as well. This split operation may need to happen recursively all the way to the root.

## The node is underutilized

There are cases, in contrast to the overflow, called underflow, where a node contains the number of keys that is less than the minimum key limitation (N/2). This can happen when the user deletes data. The process of dealing with this situation is quite the opposite of how the system resolves the overflow.

The idea is straightforward: if two adjacent nodes with the same parent (sibling nodes) and their total keys fit into a single node, they should be merged:

* If it is a leaf node, it is merged with the adjacent sibling. All key-pointer pairs from one node are moved into the other. The result is a single leaf node containing all the keys from both. The key in the parent internal node that separates these two leaves is **deleted.**

  [![](https://substackcdn.com/image/fetch/$s_!zCDO!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffd43a41-2b0e-4ffa-b392-c7209b22eb51_1214x472.png)](https://substackcdn.com/image/fetch/$s_!zCDO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffd43a41-2b0e-4ffa-b392-c7209b22eb51_1214x472.png)
* If it is a non-leaf node, it is also merged with the adjacent sibling. The system must first pull down the separator key from itsparent node**.** This key joins the keys of the two nodes being merged. The keys and all child pointers from the underflowed node, its sibling, and the pulled-down parent key are all combined into a single new internal node.

[![](https://substackcdn.com/image/fetch/$s_!thJq!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fba94ab29-3fa7-4064-8761-de3352d1fc60_1488x508.png)](https://substackcdn.com/image/fetch/$s_!thJq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fba94ab29-3fa7-4064-8761-de3352d1fc60_1488x508.png)

Like the overflow case, the process to solve the underflow might need to happen all the way to the root.

## Make it reliable

Essentially, the write operations in the B-Tree overwrite the disk pages with the new data. Some operations also involve working with more than one page on disk at once (e.g., splitting a page). Two split pages are written, plus potentially more than one parent node will also be updated. What if just one of those pages has been written because of an issue that occurred during the process?

To provide durability, B-Tree implementations universally employ **Write-Ahead Logging (WAL).** It is an append-only file. The system must write any B-tree modification to this file before it can be applied to the pages. When the database is restored after a crash, this log is used to recover the B-tree to a consistent state.

## Outro

In this article, we revisit the basics of tree data structures, focusing on the binary search tree (BST) with the binary search property. We then explore that this property is appealing to many applications, including relational databases. Next, we examine why the BST is not suitable for disk layout. The rest of the article delves into the B-Tree implementation (to be more precise, it is the B+Tree), from its anatomy to how it redistributes the nodes (splitting and merging)

Although the B-Tree is excellent for data reading, writing operations require more work to ensure the structure of the tree. In the future, we will see an alternative implementation that focuses more on the write side. An exciting thing is that this solution is more commonly seen in the OLAP world; it is the LSM tree.

See you in my next article.

## Reference

*[1] Martin Kleppmann, [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) (2017)*

*[2] Alex Petrov, [Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.amazon.com/Database-Internals-Deep-Distributed-Systems/dp/1492040347) (2019)*

*[3] CS186, Berkeley, [B+Tree note](https://cs186berkeley.net/resources/static/notes/n04-B+Trees.pdf), (2023)*
