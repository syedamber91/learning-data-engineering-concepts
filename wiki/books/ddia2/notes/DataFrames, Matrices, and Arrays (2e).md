---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
type: topic
tags: [ddia2, dataframes, pandas, matrices, one-hot-encoding, array-databases]
sources:
  - raw/ch03.md
---
# DataFrames, Matrices, and Arrays
The models so far are generally used for both transaction processing and analytics. There are also models you will meet in analytical or scientific contexts that rarely feature in OLTP systems: **DataFrames** and multidimensional arrays of numbers such as matrices.

The DataFrame model is supported by the **R** language, the **Pandas** library for Python, **Apache Spark**, **ArcticDB**, **Dask**, and others. DataFrames are popular for preparing data to train ML models, and are also widely used for data exploration, statistical analysis, and visualisation.

At first glance a DataFrame resembles a relational table or a spreadsheet. It supports relational-like operators performing bulk operations: applying a function to all rows, filtering rows on a condition, grouping by some columns and aggregating others, and joining one DataFrame with another on a key — what a relational database calls a join is typically called a **merge** on DataFrames.

## Key Takeaways
- **The interaction style is different.** Instead of a declarative query language like SQL, a DataFrame is generally manipulated through **a series of commands that modify its structure and content**. That matches the typical data-scientist workflow of incrementally "wrangling" data into a form that answers the question being asked — usually on a private copy of the dataset, often on a local machine, though the end result may be shared.
- **The operations go far beyond relational.** DataFrame APIs offer a wide variety of operations relational databases don't have, and the model is often used in ways very different from typical relational data modelling.
- **The characteristic move is relational → matrix.** The book's example: a relational table of users' movie ratings (1 to 5) becomes a matrix with one column per movie and one row per user — like a spreadsheet pivot table. The matrix is **sparse** (no data for many user-movie combinations), which is fine. It may have many thousands of columns and would fit badly in a relational database, but DataFrames and sparse-array libraries such as **NumPy** handle it easily.
- **Getting non-numbers into a matrix.** A matrix can contain only numbers. Dates can be scaled to floating-point numbers in a suitable range. Columns taking one of a small fixed set of values — a movie's genre — typically use **one-hot encoding**: create a column per possible value ("comedy," "drama," "horror"), then put a 1 in the column matching that row's genre and 0 in the others. This generalises easily to movies fitting several genres.
- **Why it matters.** Once data is a matrix of numbers it is amenable to **linear algebra operations**, which form the basis of many ML algorithms — the ratings matrix could be part of a movie recommendation system. DataFrames are flexible enough to let data be gradually evolved from relational form into matrix form, giving the data scientist control over the representation best suited to the analysis or model training.
- **Array databases** such as **TileDB** specialise in storing large multidimensional arrays of numbers, most commonly for scientific datasets: geospatial measurements (raster data on a regularly spaced grid), medical imaging, or astronomical telescope observations. DataFrames are also used in finance for **time-series data** such as asset prices and trades over time. Because of their popularity with data scientists, DataFrames have been added to batch processing frameworks such as **Spark and Flink** too.

## Since the 1st Edition
Entirely new. The 1st edition had no treatment of DataFrames, matrices, one-hot encoding, or array databases — the data-science and ML side of data modelling was essentially absent. Its inclusion here reflects the same shift that produced the data-lake material in Chapter 1: data scientists became a first-class audience for a data-systems book.

## Related
- chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[Graph-Like Data Models (2e)]] — adjacency matrices as the graph/matrix bridge
- [[DataFrames (2e)]] — DataFrames as a batch-processing model, in Chapter 11
- [[Machine Learning (2e)]] — the batch use case these feed
- [[Data Warehousing (2e)]] — the data-lake argument for why data scientists left SQL
