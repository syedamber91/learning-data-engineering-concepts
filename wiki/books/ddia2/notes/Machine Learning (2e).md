---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Use Cases
type: subtopic
tags: [ddia2, machine-learning, feature-engineering, pregel, bsp, llm, ray]
sources:
  - raw/ch11.md
---
# Machine Learning
> Feature engineering, training, and batch inference are all batch jobs — and so is most of what happens to text before an LLM ever sees it.

## The Idea
**Data scientists, ML engineers, and AI engineers use batch frameworks to investigate data patterns, transform data, and train models.** Three common uses:
- **Feature engineering.** **Raw data is filtered and transformed into data models can be trained on.** **Predictive models often need numeric data, so engineers must transform other forms — text, discrete values — into the required format.**
- **Model training.** **The training data is the input to the batch process, and the weights of the trained model are the output.**
- **Batch inference.** **A trained model can make predictions in bulk if datasets are large and real-time results are not required** — **including evaluating the model's predictions on a test dataset.**

**Batch frameworks provide tools explicitly for these**: **Apache Spark's MLlib and Apache Flink's FlinkML** come with **feature engineering tools, statistical functions, and classifiers.**

## How It Works
**Graph processing.** **ML applications such as recommendation engines and ranking systems make heavy use of graph processing.** **Many graph algorithms are expressed by traversing one edge at a time, joining one vertex with an adjacent vertex to propagate information, repeating until a condition is met** — until there are no more edges to follow, or a metric converges.

**The bulk synchronous parallel (BSP) model has become popular for batch graph processing**, implemented by **Apache Giraph, Spark's GraphX API, and Flink's Gelly API.** **It is also known as the Pregel model, since Google's Pregel paper popularized the approach.**

**LLM data preparation.** **Batch processing is an integral part of large language model data preparation and training.** **Raw text — the contents of websites — typically resides in a DFS or object store and must be preprocessed to make it suitable for training.** Steps well suited to batch frameworks:
- **Extracting plain text from HTML and fixing malformed text.**
- **Detecting and removing low-quality, irrelevant, and duplicate documents.**
- **Tokenizing text (splitting into words) and converting it into embeddings, or numeric representations of each word.**

**Frameworks such as Kubeflow, Flyte, and Ray are purpose-built for such workloads** — **OpenAI uses Ray as part of its ChatGPT training process.** **They have built-in integrations for LLM and AI libraries such as PyTorch, TensorFlow, and XGBoost**, and **offer built-in support for feature engineering, model training, batch inference, and fine-tuning** (adjusting a foundational model for specific use cases).

## Trade-offs & Pitfalls
- **Data scientists often experiment in interactive notebooks such as Jupyter or Hex.** **Notebooks are made up of cells — small chunks of Markdown, Python, or SQL — executed sequentially to produce spreadsheets, graphs, or data.** **Many notebooks use batch processing via DataFrame APIs or query such systems using SQL.**
- The pipeline shape is worth noticing: **every stage before training is a data transformation problem, not a modelling problem** — which is exactly why batch processing frameworks, not ML frameworks, do most of the work.

## Examples & Systems
Spark MLlib, Flink FlinkML; Apache Giraph, GraphX, Gelly (BSP/Pregel); Kubeflow, Flyte, Ray; PyTorch, TensorFlow, XGBoost; Jupyter and Hex notebooks.

## Since the 1st Edition
The 1st edition covered graph processing and the Pregel/BSP model under "Beyond MapReduce," and mentioned machine learning only in passing. **The 2nd edition folds graph processing into a broader machine-learning use case and adds the entire LLM data-preparation section** — HTML extraction, deduplication, tokenization and embeddings, with **Ray, Kubeflow, and Flyte named and OpenAI's use of Ray cited.** None of that existed in 2017.

## Related
- up: [[Batch Use Cases (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Vector Embeddings (2e)]] — what the tokenization step produces
- [[DataFrames (2e)]] — the API this work is mostly written in
- [[Graph-Like Data Models (2e)]] — the data model behind BSP
- 1st edition: [[Graphs and Iterative Processing]] — the closest predecessor
